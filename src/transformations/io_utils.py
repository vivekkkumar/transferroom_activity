from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def load_data(spark: SparkSession, data_path: str,
              profile_path: str, data_schema, profile_schema, format="TSV"):
    """
    :param spark: SparkSession
    :param data_path: path of user_data
    :param profile_path: path of the user profile data
    :param data_schema: path of user_data schema
    :param profile_schema: path of the user profile schema
    :param format: csv, parquet
    :return:
    """
    if format == "TSV":
        data_df = spark.read.csv(data_path, sep='\t', schema=data_schema, header=False)
        # can repartition based on executors and size of the input data
        profile_df = spark.read.csv(profile_path, sep='\t', schema=profile_schema, header=False)
        return data_df, profile_df


def save_as_csv(df: DataFrame, path):
    df.write.csv(path, header=True)

