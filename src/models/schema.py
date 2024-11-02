from pyspark.sql.types import StructType, StructField, StringType, TimestampType

sample_schema = StructType([
    StructField("userid", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("musicbrainz_artist_id", StringType(), True),
    StructField("artist_name", StringType(), True),
    StructField("musicbrainz_track_id", StringType(), True),
    StructField("track_name", StringType(), True)
])
