import csv
import sqlite3
from random import randint


try:
	meta_conn = sqlite3.connect('validator.db')
	meta_conn.execute("""CREATE TABLE jobs ( 
					job_id int, 
					status varchar(255))""")
except:
	print 'using existing jobs table...'

def create_table(file_path):
	try:
		f = open(file_path, 'rb')
		reader = csv.reader(f)
		header = reader.next()
		job_id = randint(0, 10**5)
		conn = sqlite3.connect('job_%d.db' % job_id)
		c = conn.cursor()
		sql = 'CREATE TABLE raw_data (row_num bigint, %s)' % (', '.join(['col_%d varchar(255)' % i for i in range(len(header))]))
		c.execute(sql)

		sql = 'CREATE TABLE raw_header (raw_col_name varchar(255), col_name varchar(255))'
		c.execute(sql)
		for i in range(len(header)):
			sql = 'INSERT INTO raw_header VALUES(\'col_%d\', \'%s\')' % (i, header[i])
			conn.execute(sql)

		row_num = 0
		for row in reader:
			sql = 'INSERT INTO raw_data VALUES (%d, \'%s\')' % (row_num, '\', \''.join(row))
			c.execute(sql)
			row_num += 1

		conn.commit()
		conn.close()

		meta_c = meta_conn.cursor()
		meta_c.execute('INSERT INTO jobs VALUES (%d, \'raw_data_loaded\')' % job_id)
		meta_conn.commit()

		return {'status': 'success', 'message': 'Raw data loaded.', 'job_id': job_id, 'data_row_count': row_num}
	except Exception as e:
		return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
	print create_table('testData/appropValid.csv')

