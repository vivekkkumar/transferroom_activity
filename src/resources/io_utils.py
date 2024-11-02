from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def load_data(spark: SparkSession, data_path: str,
              profile_path: str, data_schema, profile_schema, format="TSV"):
    pass


def save_as_csv(df: DataFrame, path):
    pass

