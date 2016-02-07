import csv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from random import randint
import os

try:
	meta_conn = psycopg2.connect("dbname='validator' user='testUser' host='localhost' password='testPwd'")
	meta_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	meta_conn.cursor().execute("""CREATE TABLE jobs ( 
					job_id int, 
					status varchar(255))""")
except:
	print 'using existing jobs table...'

def create_table(file_path, schema_name):
	try:
		f = open(file_path, 'rb')
		reader = csv.reader(f)
		header = reader.next()
		job_id = randint(0, 10**5)
		meta_conn.cursor().execute('CREATE DATABASE job_%d;' % job_id)
		conn = psycopg2.connect("dbname='job_%d' user='testUser' host='localhost' password='testPwd'" % job_id)
		c = conn.cursor()
		c.execute(open('schemas/%s.sql' % schema_name).read())

		row_num = 0
		for row in reader:
			row = [entry if entry is not '' else 'NULL' for entry in row]
			sql = 'INSERT INTO %s (%s) VALUES (\'%s\')' % (schema_name, ', '.join(header), '\', \''.join(row))
			c.execute(sql)
			row_num += 1

		conn.commit()
		conn.close()

		meta_c = meta_conn.cursor()
		meta_c.execute('INSERT INTO jobs VALUES (%d, \'data_loaded\')' % job_id)
		#meta_conn.commit()

		return {'status': 'success', 'message': 'Raw data loaded.', 'job_id': job_id, 'data_row_count': row_num}
	except Exception as e:
		return {'status': 'error', 'message': str(e)}

def load_tas_into_job(job_id):
	os.system('pg_dump --username=testUser -t tas validator | psql job_%d' % job_id)

def load_tas_into_validator(job_id, file_name):
	c = meta_conn.cursor()
	c.execute('DROP TABLE tas;')
	reader = csv.reader(open(file_name, 'rb'), quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True)
	# skip first row
	reader.next()

	#then get header
	header = reader.next()

	# create table
	int_cols = ['ATA']
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

def clean_databases():
	c = meta_conn.cursor()
	c.execute('SELECT datname FROM pg_database WHERE datistemplate = false;')

	for row in c.fetchall():
		if row[0].startswith('job'):
			print 'dropping %s' % row[0]
			c.execute('DROP DATABASE %s' % row[0])


if __name__ == '__main__':
	#print create_table('testData/appropriationsValid.csv', 'appropriations')
	clean_databases()
	#load_tas_into_validator(1, 'testData/all_tas_betc.csv')
