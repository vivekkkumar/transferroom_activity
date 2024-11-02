from pyspark.sql import SparkSession

from src.resources.io_utils import load_data, save_as_csv
from src.transformations.transformation_methods import transform_method1

from src.models.schema import sample_schema


def main(user_data_path, profile_path, file_output_path):
    spark = SparkSession.builder.appName("LastFM top 210 tracks").getOrCreate()

    # load the data

    # transformation functions
    transform_method1

    # save the results
    spark.stop()


if __name__ == "__main__":
    # call the main method through DAG or other scheduling system
    main()