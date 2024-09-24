import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    valid_city = False
    while not valid_city:
        city = input("Which city's data would you like to explore?").lower()
        if city in CITY_DATA:
            valid_city = True
        else:
            print("Please choose to explore data from chicago, new york city or washington")

    valid_month = False
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    while not valid_month:
       month = input("If you'd like to explore a specific month's data from January until June, input it here.  If not, write 'all'").capitalize()
       if month in months or month == 'All':
           valid_month = True
       else:
            print("Please choose a month between January and June or write 'all'")

    valid_day = False
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while not valid_day:
        day = input("If you'd like to explore data from a specific day of the week, input it                    here.  If not, write 'all'").lower()
        if day in days or day == 'all':
                  valid_day = True
        else:
            print("Please input a valid day of the week or type 'all'")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = df['Start Time'].to_datetime()
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name
    
    months = ['Zero', 'January', 'February', 'March', 'April', 'May', 'June']
    if month != 'all':
        df = df[df['Month'] == months.index(month)]
    if day != 'all':
        df = df[df['Day'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel broken down by
    month, day of the week and hour of the day."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['Month'].count_values()[0]
    month_dict = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June'}
    print(f"The most common month is {month_dict[str(common_month)]}")

    common_day = df['Month'].count_values()[0]
    print(f'The most common day for trips is {common_day.capitalize()}')

    common_hour = df['Start Time'].count_values()[0]
    print(f"The most common hour for trips is {str(common_hour)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start = df['Start Station'].count_values()[0]
    print(f'The most common start station is {common_start}')

    common_end = df['End Station'].count_values()[0]
    print(f'The most common end station is {common_end}')

    df['terminals'] = df["Start Station"] + ', ' + df["End Station"]
    common_trip = df['terminals'].count_vales()[0]
    print(f'The most common start/end combo is {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip = df['Trip Duration'].sum()
    print(f'The total amount of time spent on trips was {str(total_trip)} seconds')

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'The average trip lenght was {str(mean_travel)} seconds')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. Gender and Birth Year information is provided
    when available in the dataset."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    users = df['User Type'].value_counts()
    print(f'There are {users[0]} {users.index[0]}s and {users[1]} {users.index[1]}s')

    gender_count = df['Gender'].value_counts()
    print(f'There are {gender_count[0]} {gender_count.index[0]} users and {gender_count[1]} {gender_count.index[1]} users')

    earliest_year = df['Birth Year'].min()
    most_recent = df['Birth Year'].max()
    most_common = df['Birth Year'].mode()
          
    print(f"The oldest user was born in {str(earliest_year)}, the youngest user was born in {str(most_recent)} and the most common birth year among users is {str(most_common)}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def row_presenter(data_df):
    """Provides a generator to present 5 rows of dataframe at a time"""
    start = 0
    for i in range(start, len(data_df)):
          yield data_df[start:start + 5]
          start += 5
          

def data_explore(dataframe):
    """Initial function to give the user the chance to explore data before running statistical analysis"""
    for rows in row_presenter(dataframe):
          if rows.empty:
            print("No more rows")
            break
          print(rows)
          continue_input = input("Would you like to see 5 more rows (y/n)?")
          if continue_input.lower() == 'n':
              break
    return True
          
def main():
    while True:                  
        city, month, day = get_filters()
        df = load_data(city, month, day)
          
        data_explore(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()