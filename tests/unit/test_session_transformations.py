import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from src.transformations.session_methods import \
    define_sessions, calculate_session_length, get_top_sessions, get_top_songs


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("testing_the_code").getOrCreate()

def test_define_sessions(spark):
    test_data = [("user1", "2024-01-01 00:00:00", "1", "beatles", "1", "yesterday", None, None),
            ("user1", "2024-01-01 00:15:00", "2", "coldplay", "2", "doctor", "2024-01-01 00:00:00", 900)]

    '''In test we are hardcoding the schema, but ideally we can create more models to track schema changes 
    in transformation as well'''

    schema = ["userid", "timestamp", "musicbrainz_artist_id", "artist_name", "musicbrainz_track_id",
              "track_name", "prev_timestamp", "time_diff"]
    df = spark.createDataFrame(test_data, schema=schema)
    df = define_sessions(df)
    assert df.filter(col("session_id").isNull()).count() == 0

def test_calculate_session_length(spark):
    data = [("user1", 1, "track1"),
            ("user1", 1, "track2"),
            ("user2", 2, "track3")]
    schema = ["userid", "session_id", "track_name"]
    df = spark.createDataFrame(data, schema=schema)
    session_length = calculate_session_length(df)
    assert session_length.filter(col("track_count") == 2).count() == 1

def test_get_top_sessions(spark):
    data = [("user1", 1, 2),
            ("user2", 2, 1)]
    schema = ["userid", "session_id", "track_count"]
    df = spark.createDataFrame(data, schema=schema)
    top_sessions = get_top_sessions(df, 1)
    assert top_sessions.count() == 1
    assert top_sessions.collect()[0]["userid"] == "user1"

def test_get_top_songs(spark):
    session_data = [("user1", 1, 2)]
    session_schema = ["userid", "session_id", "track_count"]
    sessions_df = spark.createDataFrame(session_data, schema=session_schema)

    data = [("user1", "2020-01-01 00:00:00", "id1", "artist1", "id1", "track1", 1),
            ("user1", "2020-01-01 00:15:00", "id2", "artist2", "id2", "track2", 1)]

    schema = ["userid", "timestamp", "musicbrainz_artist_id", "artist_name", "musicbrainz_track_id", "track_name",
              "session_id"]
    df = spark.createDataFrame(data, schema=schema)

    top_songs = get_top_songs(sessions_df, df, 1)
    assert top_songs.count() == 1
    assert top_songs.collect()[0]["track_name"] == "track2"