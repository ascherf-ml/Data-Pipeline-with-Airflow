from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from operators.create_tables import CreateTableOperator
from helpers.sql_queries import SqlQueries


default_args = {
    'owner': 'alex',
    'start_date': datetime(2020, 8, 27),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
    'schedule_interval': '@hourly'
}


dag = DAG('pipe_stage3',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          max_active_runs=3
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_in_redshift = CreateTableOperator(
"""
connecting to redshift
running the CreateTableOperator operator with create_tables.sql
"""
    task_id = 'create_tables_in_redshift',
    redshift_conn_id = 'redshift',
    dag = dag
)

stage_events_to_redshift = StageToRedshiftOperator(
"""
connecting to S3
connecting to redshift
running the StageToRedshiftOperator operator
"""
    task_id="stage_events_to_redshift",
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json="s3://udacity-dend/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
"""
connecting to S3
connecting to redshift
running the StageToRedshiftOperator operator
"""
    task_id="stage_songs_to_redshift",
    dag=dag,
    table="staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="song_data/A/A/A",
    json="auto"
)

load_songplays_table = LoadFactOperator(
"""
connecting to redshift
running the LoadFactOperator operator with sql_queries.py
"""
    task_id='Load_songplays_fact_table',
    redshift_conn_id = 'redshift',
    table="songplays",
    sql_query = SqlQueries.songplay_table_insert,
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
"""
connecting to redshift
running the LoadDimensionOperator operator with sql_queries.py
"""
    task_id='Load_user_dim_table',
    redshift_conn_id = 'redshift',
    table="users",
    sql_query = SqlQueries.user_table_insert,
    dag=dag
)

load_song_dimension_table = LoadDimensionOperator(
"""
connecting to redshift
running the LoadDimensionOperator operator with sql_queries.py
"""
    task_id='Load_song_dim_table',
    redshift_conn_id = 'redshift',
    table="songs",
    sql_query = SqlQueries.song_table_insert,
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
"""
connecting to redshift
running the LoadDimensionOperator operator with sql_queries.py
"""
    task_id='Load_artist_dim_table',
    redshift_conn_id = 'redshift',
    table="artists",
    sql_query = SqlQueries.artist_table_insert,
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
"""
connecting to redshift
running the LoadDimensionOperator operator with sql_queries.py
"""
    task_id='Load_time_dim_table',
    redshift_conn_id = 'redshift',
    table="time",
    sql_query = SqlQueries.time_table_insert,
    dag=dag
)

run_quality_checks = DataQualityOperator(
"""
connecting to redshift
running the DataQualityOperator operator
"""
    task_id='run_data_quality_checks',
    redshift_conn_id="redshift",
    table="time",
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

"""
Order of dags; starting with the start_operator and ending with the end_operator
"""
start_operator >> create_tables_in_redshift
create_tables_in_redshift >> [stage_songs_to_redshift, stage_events_to_redshift] >> load_songplays_table

load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks >> end_operator
