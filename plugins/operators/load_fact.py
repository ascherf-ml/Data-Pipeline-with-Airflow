from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    insert_sql = """
        INSERT INTO {}
        {}
        ;
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query = "",
                 table="",
                 append_only = False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table = table
        self.append_only = append_only


    def execute(self, context):
        """
        connecting to redshift with the PostgresHook and the redshift_conn_id
        deleting former data in the tables
        inserting the data into the fact table with sql_queries.py
        """
        redshift_hook = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        if not self.append_only:
            self.log.info("Delete {} fact table".format(self.table))
            redshift_hook.run("DELETE FROM {}".format(self.table))

        formatted_sql = LoadFactOperator.insert_sql.format(
            self.table,
            self.sql_query
        )
        redshift_hook.run(formatted_sql)
