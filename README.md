# Data-Pipeline-with-Airflow

# Project Description
From "Udacity Data Engineer Nanodegree":

A [hypothetical] music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring the data engineering team into the project and expect us to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Project Structure
This project contains the following files:

```sh
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

![Dag example](https://github.com/ascherf-ml/Data-Pipeline-with-Airflow/blob/master/example-dag.png)
"Example Dag Picture from udacity.com"

`pipe_stage3.py`

Consists of 7 stages with multiple dags:

- Stage 1: Begin Execution

- Stage 2: Creating empty tables in redshift with `CreateTableOperator`

- Stage 3: Loading data from S3 with `StageToRedshiftOperator`
  - loading **events** from event data (JSON-files) stored on S3 and storing the data in a table on AWS-redshift
  - loading **songs** from song data (JSON-files) stored on S3 and storing the data in a table on AWS-redshift

- Stage 4: Creating `songplays` fact table based on song and event data with `LoadFactOperator`

- Stage 5: Creating dimensional tables additional to `songplays` with `LoadDimensionOperator`
  - `users`: user information
  - `songs`: song information
  - `artists`: artist information
  - `time`: datetime of songplays


- Stage 6: Data quality check
  - checking if the data was successfully handled with `DataQualityOperator`


- Stage 7: Stop Execution




# Execution

1. Create Amazon Redshift database.

2. Run `pipe_stage3.py` to process the entire datasets.
