from pyspark.sql import SparkSession

from src.transformations.io_utils import load_data, save_as_csv
from src.transformations.session_methods import calculate_session_length, \
    define_sessions, calculate_time_diff, get_top_sessions, get_top_songs

from src.models.last_fm import user_music_activity_schema, user_profile_schema


def main(user_data_path, profile_path, file_output_path):
    spark = SparkSession.builder.appName("LastFM top 210 tracks").getOrCreate()

    # load the data
    user_music_activity, profile_df = load_data(spark, user_data_path, profile_path, user_music_activity_schema,
                                                user_profile_schema)

    # transformation functions
    user_music_activity_with_time_diff = calculate_time_diff(user_music_activity)
    user_music_activity_with_session = define_sessions(user_music_activity_with_time_diff)
    session_length = calculate_session_length(user_music_activity_with_session)
    top_sessions = get_top_sessions(session_length, 50)
    top_10_songs = get_top_songs(top_sessions, user_music_activity_with_session, 10)

    # save the results
    save_as_csv(top_10_songs, file_output_path)
    spark.stop()


if __name__ == "__main__":
    # hard coding these values for this script, later can be extended to use sys.argv to get command line params
    user_data_path = "path/userid-timestamp-artid-artname-traid-traname.tsv"
    profile_path = "path/userid-profile.tsv"
    file_output_path = "src/resources/output/top_10_songs.csv"

    main(user_data_path, profile_path, file_output_path)