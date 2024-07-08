from pyspark.sql.functions import unix_timestamp, lag, col, count, when, sum as pyspark_sum
from pyspark.sql.window import Window

def calculate_time_diff(data_df):
    """
    :param data_df: dataframe
    :return: dataframe
    """

    window_spec = Window.partitionBy("userid").orderBy("timestamp")
    data_df = data_df.withColumn("prev_timestamp", lag("timestamp").over(window_spec))
    data_df = data_df.withColumn("time_diff", unix_timestamp("timestamp") - unix_timestamp("prev_timestamp"))
    return data_df

def define_sessions(data_df, seconds_for_sessions = 1200):
    """
    :param data_df: dataframe
    :param seconds_for_sessions: seconds to define a session
    :return: dataframe
    """
    window_spec = Window.partitionBy("userid").orderBy("timestamp")
    data_df = data_df.withColumn("session_id",
                                 pyspark_sum(when(col("time_diff") > seconds_for_sessions, 1)
                                             .otherwise(0)).over(window_spec))
    # pyspark_sum is alternative to sql like syntax which was informed to be avoided.
    # expr("sum(case when time_diff > 1200 then 1 else 0 end) over (partition by userid order by timestamp)")
    return data_df

def calculate_session_length(data_df):
    """
        :param data_df: dataframe
        :return: dataframe
    """

    session_length = data_df.groupBy("userid", "session_id").agg(count("track_name").alias("track_count"))
    return session_length

def get_top_sessions(session_length, top_n):
    """

    :param session_length: dataframe
    :param top_n: int - limit of the songs
    :return: dataframe
    """
    top_sessions = session_length.orderBy(col("track_count").desc()).limit(top_n)
    return top_sessions

def get_top_songs(top_sessions, data_df, top_n):
    """

    :param top_sessions: int
    :param data_df: dataframe
    :param top_n: int
    :return:
    """
    top_sessions_tracks = top_sessions.join(data_df, ["userid", "session_id"], "inner")
    top_songs = top_sessions_tracks.groupBy("track_name").agg(count("track_name").alias("play_count"))
    top_10_songs = top_songs.orderBy(col("play_count").desc()).limit(top_n)
    return top_10_songs