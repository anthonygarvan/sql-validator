# sql-validator

## What is this thing
This is a demo application for a business rules engine based on SQL rather than a domain specific language. It is designed to demonstrate some cool features of using SQL as a langauge for defining business rules:
- TRANSPARENCY: SQL rules are easy to write and understand, and very googlable. With a custom rules language, those wishing to understand the rule need to grok not only the rule itself but also your source code.
- ECONOMICS: Reduces feature development time. All the things a DSL would need to build out are already built into SQL: no need to reinvent the wheel.
- PRECISION: SQL tables can be used to define the basic schema, thus forcing rule authors to thing in specific terms from the beginning. For example, thinking pythonically may lead you to define a "float" datatype to represent a currency value, when really a decimal is more appropriate. 
- PERFORMANCE: Writing rules in SQL means you do not need to transfer data back and forth between the database and application layers, which is a huge bottleneck in performance for large data volumes. Once the data is in, all the processing happens on one box.   
- SCALABILITY: With advances in massively parallel processing systems like Amazon Redshift and Spark-SQL, you can be confident that your rules will always run in a time-boxed way for any data size, in case you grow out of your traditional relational database's already considerable performance. 
- PORTABILITY: You're business rules are (nearly) independent of your tech stack. You can rewrite you app without rewriting your business rules.

## Example Output
Here's an example output from the rules engine when processing a valid appropriations file:
```shell
Running rule 0: SELECT * FROM appropriations WHERE AllocationTransferRecipientAgencyId < 0
==> Found 0 invalid rows.
Running rule 1: SELECT * FROM appropriations WHERE AllocationTransferRecipientAgencyId > 999
==> Found 0 invalid rows.
Running rule 2: SELECT * FROM appropriations WHERE AppropriationAccountResponsibleAgencyId < 0
==> Found 0 invalid rows.
Running rule 3: SELECT * FROM appropriations WHERE AppropriationAccountResponsibleAgencyId > 999
==> Found 0 invalid rows.
Running rule 4: SELECT * FROM appropriations WHERE ObligationAvailabilityPeriodStartFiscalYear < 0
==> Found 0 invalid rows.
Running rule 5: SELECT * FROM appropriations WHERE ObligationAvailabilityPeriodStartFiscalYear > 2100 OR ObligationAvailabilityPeriodStartFiscalYear < 1900
==> Found 0 invalid rows.
Running rule 6: SELECT * FROM appropriations WHERE ObligationAvailabilityPeriodEndFiscalYear > 2100 OR ObligationAvailabilityPeriodEndFiscalYear < 1900
==> Found 0 invalid rows.
Running rule 7: SELECT * FROM appropriations WHERE AppropriationMainAccountCode < 0
==> Found 0 invalid rows.
Running rule 8: SELECT * FROM appropriations WHERE AppropriationMainAccountCode > 999
==> Found 0 invalid rows.
Running rule 9: SELECT * FROM appropriations WHERE AppropriationSubAccountCode < 0
==> Found 0 invalid rows.
Running rule 10: SELECT * FROM appropriations WHERE AppropriationSubAccountCode > 999
==> Found 0 invalid rows.
Running rule 11: SELECT * FROM appropriations WHERE ObligationUnlimitedAvailabilityPeriodIndicator NOT IN ('X', 'F', 'A', 'NULL')
==> Found 0 invalid rows.
Running rule 12: SELECT * from appropriations app LEFT JOIN tas ON app.AppropriationMainAccountCode="MAIN" WHERE "MAIN" IS NULL
==> Found 0 invalid rows.
```
More detailed error reporting could be easily added, both at the ingest stage (as data is being loaded from the csv to the table) and the rule execution stage.

### Requirements:
- [postgres](http://www.postgresql.org/download/)
- [pyscopg2](http://initd.org/psycopg/docs/install.html)

### Setup
You'll need to install postgres and run
```sql
CREATE DATABASE validator
```
I also currently have the username and password hard-coded to `testUser` and `testPwd`. You'll need to create that username and password or change the code.

The validation database is the master database which serves as a source of truth for the TAS dataset and also provided management of jobs for worker nodes through the `jobs` table. To get it set up you'll need to run:

```shell
$ python load_data.py --initialize
```
It can take a few minutes to upload all the data.

### Usage:
To run a valid appropriations file through the rule set, use:
```shell
$ python test.py
```

This repo also demonstrates an architecture for easy parallelization using worker nodes rather than threading, using a shared database table as a simple queue. This is prefered over threading since workers can be distributed easily across many nodes.
To see that in use, open up one terminal tab and start the worker node with:
```shell
$ python worker.py
```
Then, to simulate a new file coming in for processing, run:
```shell
$ python load_data.py
```
The results will appear in tab with worker.py running.
