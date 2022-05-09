import time
import pandas as pd
import numpy as np
import time
from os import system
from IPython.display import display
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Kindly enter the city you would like to see data for Chicago, New York City, or Washington: ").lower()
    while city not in CITY_DATA:
        print("Oops.. Invalid city name. Please try again")
        city=input().lower()


    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','may','june','all']
    month = input("Kindly enter the month you would like to see data from January to June or enter All for no month filter: ").lower()
    while month not in months:
        print("Oops.. Invalid month. Please try again")
        month=input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    day = input("Kindly enter the day you would like to see data from Monday to Sunday or enter ALL for no day filter: ").lower()
    while day not in days:
        print("Oops.. Invalid day. Please try again")
        day=input().lower()


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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month

    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    months = ['January','February','March','April','May','June']
    print("most common month: ", months[most_common_month-1])




    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    most_common_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print("Most common day of week: ", days[most_common_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print("Most common start hour: ",common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: {}, occurrence count: {}".format(df['Start Station'].mode()[0], df['Start Station'].value_counts()[0]))

    # display most commonly used end station
    print("Most commonly used end station: {}, occurrence count: {}".format( df['End Station'].mode()[0], df['Start Station'].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip\n", df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: ",time.strftime("%H:%M:%S",time.gmtime(df['Trip Duration'].sum())))

    # display mean travel time
    print("Mean Travel Time: ",time.strftime("%H:%M:%S",time.gmtime(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        print('Most Common year of Birth:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Function to clear the screen to improve user experience
        system('clear')
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #To prompt the user whether they would like want to see the raw data
        enter = ['yes','no']
        user_input = input('Would you like to see more data? Enter yes or no.\n')

        while user_input.lower() not in enter:
            user_input = input('Please Enter Yes or No:\n')
            user_input = user_input.lower()
        n = 0
        while True :
            if user_input.lower() == 'yes':
                display(df.iloc[n : n + 5])
                n += 5
                user_input = input('\nWould you like to see more data? Enter yes or no.\n')
                while user_input.lower() not in enter:
                    user_input = input('Please Enter Yes or No:\n')
                    user_input = user_input.lower()
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
