from load_data import create_table, load_tas_into_job, upload_file
from run_rules import run_rules
from time import sleep
import psycopg2

meta_c = psycopg2.connect("dbname='validator' user='testUser' host='localhost' password='testPwd'").cursor()

print "Press any key to cancel."
try:
	while(True):
		meta_c.execute("SELECT * FROM jobs WHERE status='file_uploaded' LIMIT 1")
		for job in meta_c.fetchall():
			job_id, file_path, status = job
			print 'processing job %d' % job_id
			result = create_table(job_id, 'appropriations')
			load_tas_into_job(job_id)
			run_rules(job_id, 'appropriations')
		sleep(0.2)
except KeyboardInterrupt:
	print "Process cancelled by user."