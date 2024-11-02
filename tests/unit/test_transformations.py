import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from src.transformations.transformation_methods import transform_method1


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("testing_the_code").getOrCreate()

def test_trasnformations(spark):
    pass
