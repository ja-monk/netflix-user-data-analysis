import sys
import pandas as pd
from env import viewing_activity_path
import src.data_analysis
import src.user_input

def main():
    # read csv file into pandas dataframe, r for raw string e.g. \ isnt escaping
    viewing_records = pd.read_csv(viewing_activity_path)
    # format & clean data
    viewing_records = src.data_analysis.format_data(viewing_records)
    
    # take user input for user and title of show/film
    user = src.user_input.select_user(viewing_records)
    title = src.user_input.select_media(user, viewing_records)

    # filter df to get only data for the given user
    user_df = src.data_analysis.filter_df_column_contains_string(viewing_records, 'Profile Name', user)
    # filter user data to get only data for given title for that user
    user_show_df = src.data_analysis.filter_df_column_contains_string(user_df, 'Title', title)

    # categorise
    user_show_df = src.data_analysis.categorise_days_hours(user_show_df)

    print(user_show_df.head)

    return 0

if __name__ == '__main__':
    sys.exit(main())
