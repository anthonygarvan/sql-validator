# Validator

Example of validation of schemas / data integrity with SQL rules. 

### REQUIREMENTS:
postgres / pyscopg2

### USAGE:
```shell
$ python test.py
```

## What is this thing
This is a demo application for running a set of business rules against a specific schema (an appropriations schema in development for the DATA Act). It is designed to demonstrate some cool features of using SQL as a langauge for defining business rules:
- SQL rules are easy to write and understand, no need to reinvent the wheel.
- SQL tables can be used to define the basic schema, thus forcing rule authors to thing in specific terms from the beginning 
- A sandbox is created for each job in the form of an new database, this provides excellent isolation and avoids naming collisions
- PERFORMANCE: Writing rules in SQL means you do not need to transfer data back and forth between the database and application layers, which is a huge bottleneck in performance for large data volumes.  

## Theory
ANSI-SQL is a great language for writing rules, because most common data types operators are already built into the language, and it is already widely known and easily learned. Advanced users can even run the validations in place on their existing database systems or even csv file (with textql for example). It is also great because it scales to any data volume- traditional RDBMS systems are already heavily optimized, and for very large datasets there are massively parallel systems such as amazon Redshift and Spark-Sql. So, for those of you writing rules out there, don't invent some domain specific language - just use SQL!

To turn SQL into a rules engine, just think of a SELECT statement as selecting the set of invalid rows from a dataset. Those SQL statements can be organized to run in parallel for increased performance. 

For additional power, you can organize rules into rule sets, where each rule set is executed in a hard-coded manner. For example, you could have a rule set to validate each record, then another rule set for aggregations that only runs once all the records are valid. This lets you take advantage of parallelism while also respecting dependencies. 

## Example Output
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
Running rule 12: SELECT * from appropriations app LEFT JOIN tas ON app.AllocationTransferRecipientAgencyId="ATA" WHERE "ATA" IS NULL
==> Found 20 invalid rows.
```