# Validator

Example of validation of schemas / data integrity with SQL rules. 

### REQUIREMENTS:
postgres / pyscopg2

### USAGE:
```shell
$ python test.py
```

## What is this thing
This is a demo application for a business rules engine based on SQL rather than a domain specific language. It is designed to demonstrate some cool features of using SQL as a langauge for defining business rules:
- SQL rules are easy to write and understand. 
- All the things a DSL would need to build out are already built into SQL: no need to reinvent the wheel.
- SQL tables can be used to define the basic schema, thus forcing rule authors to thing in specific terms from the beginning. For example, thinking pythonically may lead you to define a "float" datatype to represent a currency value, when really a decimal is more appropriate. 
- PERFORMANCE: Writing rules in SQL means you do not need to transfer data back and forth between the database and application layers, which is a huge bottleneck in performance for large data volumes. Once the data is in, all the processing happens on one box.   
- SCALABILITY: With advances in massively parallel processing systems like Amazon Redshift and Spark-SQL, you can be confident that your rules will always run in a time-boxed way for any data size, in case you grow out of your traditional relational database's already considerable performance. 

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