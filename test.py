from load_data import create_table, load_tas_into_job
from run_rules import run_rules

result = create_table('testData/appropriationsValid.csv', 'appropriations')
load_tas_into_job(result['job_id'])
run_rules(result['job_id'], 'appropriations')
