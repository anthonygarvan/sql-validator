import sqlite3
import csv
from os import path

def load_schema(file_path, job_id):
	try:
		conn = sqlite3.connect('job_%d.db' % job_id)
		conn.execute("""CREATE TABLE schemas (
						schema_name varchar(255), 
						fieldname varchar(255), 
						required boolean,
						data_type varchar(20),
						field_length int NULL)""")
	except:
		print 'using existing schemas table...'
	
	schema_name = path.splitext(path.split(file_path)[1])[0]
	f = open(file_path, 'rb')
	reader = csv.reader(f)

	#skip header row
	reader.next()

	#load the data
	c = conn.cursor()
	c.execute('DELETE FROM schemas WHERE schema_name=\'%s\'' % schema_name)
	row_num = 0
	for row in reader:
		field_length = row[3] if row[3] else 'NULL'
		sql = 'INSERT INTO schemas VALUES (\'%s\',\'%s\', \'%s\', \'%s\', \'%s\')' % (schema_name, row[0], row[1], row[2], field_length)
		c.execute(sql)
		row_num += 1
	conn.commit()
	conn.close()

	print '%s schema with %d rows loaded into database job_%d' % (schema_name, row_num, job_id)


if __name__ == '__main__':
	load_schema('testData/appropriations.csv', 92153)