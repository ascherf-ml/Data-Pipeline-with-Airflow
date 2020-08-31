# Data-Pipeline-with-Airflow

# Project Description
From "Udacity Data Engineer Nanodegree":

A [hypothetical] music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring the data engineering team into the project and expect us to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Structure
This project contains the following files:

```
README.md
dags:
- pipe_stage3.py
- create_tables.sql

plugins:
- helpers:
  - sql_queries.py

- operators:
  - create_tables.py
  - create_tables.sql
  - data_quality.py
  - load_dimension.py
  - load_fact.py
  - stage_redshift.py
```

## Main ETL
`pipe_stage3.py`

![Dag example](https://github.com/ascherf-ml/Data-Pipeline-with-Airflow/blob/master/example-dag.png)



# Execution

1. Create Amazon Redshift database.

2. Run `create_tables.sql` to create the tables.

3. Run `etl_task.py` to process the entire datasets.
