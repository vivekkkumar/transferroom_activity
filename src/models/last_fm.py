from pyspark.sql.types import StructType, StructField, StringType, TimestampType

user_music_activity_schema = StructType([
    StructField("userid", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("musicbrainz_artist_id", StringType(), True),
    StructField("artist_name", StringType(), True),
    StructField("musicbrainz_track_id", StringType(), True),
    StructField("track_name", StringType(), True)
])

user_profile_schema = StructType([
    StructField("userid", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("age", StringType(), True),  # to handle empty values
    StructField("country", StringType(), True),
    StructField("signup", StringType(), True)
])
