from load_data import create_table, load_tas_into_job, upload_file, clean_database
from run_rules import run_rules


job_id = upload_file('testData/appropriationsValid.csv')['job_id']
result = create_table(job_id, 'appropriations')
load_tas_into_job(job_id)
run_rules(job_id, 'appropriations')
print "Dropping database..."
clean_database(job_id)

