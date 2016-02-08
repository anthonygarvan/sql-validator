import csv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from random import randint
import os


meta_conn = psycopg2.connect("dbname='validator' user='testUser' host='localhost' password='testPwd'")
meta_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
meta_c = meta_conn.cursor()

def upload_file(file_path):
	# this doesn't actually upload a file, it's just a placeholder demonstrating a reasonable architecture.
	job_id = randint(0, 10**5)
	meta_c.execute("INSERT INTO jobs (job_id, file_path, status) VALUES ('%d', '%s', '%s')" % (job_id, file_path, 'file_uploaded'))
	return {'job_id': job_id}

def create_table(job_id, schema_name):
	#try:
		meta_c = meta_conn.cursor()
		meta_c.execute("SELECT file_path from jobs WHERE job_id=%d" % job_id)
		file_path = meta_c.fetchall()[0][0]

		f = open(file_path, 'rb')
		reader = csv.reader(f)
		header = reader.next()
		
		meta_conn.cursor().execute('CREATE DATABASE job_%d;' % job_id)
		conn = psycopg2.connect("dbname='job_%d' user='testUser' host='localhost' password='testPwd'" % job_id)
		c = conn.cursor()
		c.execute(open('schemas/%s.sql' % schema_name).read())

		row_num = 0
		for row in reader:
			row = [entry if entry is not '' else 'NULL' for entry in row]
			sql = "INSERT INTO %s (%s) VALUES ('%s')" % (schema_name, ', '.join(header), "', '".join(row))
			c.execute(sql)
			row_num += 1

		conn.commit()
		conn.close()

		meta_c = meta_conn.cursor()
		meta_c.execute("UPDATE jobs SET status='table_created' WHERE job_id=%d" % job_id)

		return {'status': 'success', 'message': 'Raw data loaded.', 'job_id': job_id, 'data_row_count': row_num}
	#except Exception as e:
	#	return {'status': 'error', 'message': str(e)}

def load_tas_into_job(job_id):
	os.system('pg_dump --username=testUser -t tas validator | psql job_%d > postgres.log' % job_id)
	meta_c.execute("UPDATE jobs SET status='loading_tas' WHERE job_id='%d';" % job_id)

def create_jobs_table():
	meta_c = meta_conn.cursor()
	try:
		meta_c.execute('DROP TABLE jobs;')
	except:
		pass
	meta_c.execute("""CREATE TABLE jobs ( 
					job_id int,
					file_path varchar(255), 
					status varchar(255))""")

def load_tas_into_validator(job_id, file_name):
	# this schema should be hard-coded since it is static, I just didn't want to go through each column.

	c = meta_conn.cursor()
	try:
		c.execute('DROP TABLE tas;')
	except:
		print 'tas table not present.'
	reader = csv.reader(open(file_name, 'rb'), quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
	# skip first row
	reader.next()

	#then get header
	header = reader.next()

	# create table
	int_cols = ['ATA', 'MAIN']
	sql = 'CREATE TABLE tas (%s)' % ', ' \
			.join(['"%s" varchar(255)' % col_name if col_name not in int_cols else '"%s" INT NULL' % col_name for col_name in header])
	c.execute(sql)

	rows_inserted = 0
	for row in reader:
		row = ["'%s'" % entry.replace('\'', '\'\'') if entry is not '' else 'NULL' for entry in row]
		sql = 'INSERT INTO tas ("%s") VALUES (%s)' % ('", "'.join(header), ', '.join(row))
		c.execute(sql)
		rows_inserted += 1

	return {'tas_rows_inserted': rows_inserted}

def clean_database(job_id):
	c = meta_conn.cursor()
	c.execute('DROP DATABASE job_%d' % job_id)

def clean_databases():
	c = meta_conn.cursor()
	c.execute('SELECT datname FROM pg_database WHERE datistemplate = false;')

	for row in c.fetchall():
		if row[0].startswith('job'):
			print 'dropping %s' % row[0]
			c.execute('DROP DATABASE %s' % row[0])

	c.execute('DROP TABLE jobs;')


if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		flag = sys.argv[1]

		if flag == '--initialize':
			clean_databases()
			create_jobs_table()
			load_tas_into_validator(1, 'testData/all_tas_betc.csv')
	else:		
		upload_file('testData/appropriationsValid.csv')
		print 'file uploaded'
	