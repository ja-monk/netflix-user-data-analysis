import pandas as pd
import numpy as np
import re

def format_data(viewing_records):
    # convert data types, start time to datetime & duration to timedelta, both overall column and each value
    viewing_records.loc[:, 'Start Time'] = pd.to_datetime(viewing_records['Start Time'].astype(str).str.strip(), errors='coerce')
    viewing_records.loc[:, 'Duration'] = pd.to_timedelta(viewing_records['Duration'].astype(str).str.strip(), errors='coerce')

    viewing_records['Start Time'] = viewing_records['Start Time'].astype('datetime64[ns]')
    viewing_records['Duration'] = viewing_records['Duration'].astype('timedelta64[ns]')
    
    # add column for weekday & hour taken from Start Time column
    viewing_records['weekday'] = viewing_records.loc[:, 'Start Time'].dt.day_name() # days of week by name
    viewing_records['hour'] = viewing_records.loc[:, 'Start Time'].dt.hour
    
    # remove false positives, show watched less than 2 mins
    viewing_records = viewing_records[(viewing_records['Duration'] > pd.to_timedelta('0 days 00:02:00'))]

    return viewing_records

def get_users(viewing_data: pd.DataFrame) -> np.ndarray:
    users = viewing_data["Profile Name"].unique()
    return users

# function to find if the media is a series
def is_season(title):
    look_for = ["Season", ":"]
    if all(substring in title for substring in look_for):
        return True
    elif re.search(r"Episode \d+", title):
        return True
    return False

def get_media_for_user(viewing_data: pd.DataFrame, user: str) -> np.ndarray:
    # create df containing only rows for the specific user
    media_watched = viewing_data[viewing_data["Profile Name"] == user]
    # remove trailers, filter by all Titles containing trailer, apply pandas logical not ~ (like !)
    # also filter title with '_', 'clip' or 'teaser' as netflix 'hooks' contain this in title 
    media_watched = media_watched[~media_watched["Title"].str.contains(r"trailer|_|clip|teaser", case=False)]    

    # if media is series, strip season info from title so it can be aggregated  
    formated_titles = media_watched["Title"].apply(lambda a: a.split(":", 1)[0] if is_season(a) else a).unique()

    return formated_titles

# function returns df containing all rows from the orignal df that contain some string
def filter_df_column_contains_string(df, column, string):
    # df[column].str.contains(string, case=False) returns a 1x1 boolean df based on if the column contains the
    # given string. Filtering the dataframe based on this removes all rows where this condition was not met
    filtered_df = df[df[column].str.contains(string, case=False)]
    return filtered_df

