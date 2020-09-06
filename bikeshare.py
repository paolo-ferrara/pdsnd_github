import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = list(CITY_DATA.keys())
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    print("-"*40)
    print("Data available for the following cities:")
    print("[1] Chicago")
    print("[2] New York City")
    print("[3] Washington")
    print("-"*40)
    
    # DONE: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_idx = int(input("Please enter a number between 1 and 3 to select a city, 0 to exit: "))
            if (city_idx == 0):
                sys.exit(0)
            elif (city_idx > 3):
                print("Not a valid choice, please try again")
            else:
                city = cities[city_idx - 1]
                break
        except ValueError as e:
            print("Not a valid choice, please try again")
    
    # DONE: get user input for month
    while True:
        month = str(input("Insert a valid month from january to june, or 'all' to retrieve data for all months: ")).lower()
        if (month in months) or month == 'all':
            break
        else:
            print("No a valid month, please try again")

    # DONE: get user input for day
    while True:
        day = str(input("Insert a day of the week or 'all' to retrieve data for all days: ")).lower()
        if (day in days or day == 'all'):
            break
        else:
            print("No a valid day, please try again")
        
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
    
    # changing data type for 'Start Time' column and creating new columns for hour, month and day_of_week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   
    df['Hour'] = df['Start Time'].dt.hour
    df['Month'] = df['Start Time'].dt.month
    df['Day_Of_Week'] = df['Start Time'].dt.weekday_name
    
    # filtering on selected month and day of week if not 'all'
    if (month != 'all'):
        month_idx = months.index(month) + 1
        df = df[df['Month'] == month_idx]
    if (day != 'all'):
        df = df[df['Day_Of_Week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # DONE: display the most common month
    month_idx = df['Month'].mode()[0]
    print("Most common month : {}".format(months[month_idx-1].title()))
    
    # DONE: display the most common day of week
    print("Most common day of week : {}".format(df['Day_Of_Week'].mode()[0]))
    
    # DONE: display the most common start hour
    print("Most common start hour: {}".format(df['Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # DONE: display most commonly used start station
    print("Most commonly used start station : {} ".format(df['Start Station'].mode()[0]))
    # DONE: display most commonly used end station
    print("Most commonly used end station : {}".format(df['End Station'].mode()[0]))
    # DONE: display most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + ' - ' + df['End Station']
    print("Most common trip : {}".format(df['Start-End Station'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # DONE: display total travel time
    print("Total travel time : {}".format(df['Trip Duration'].sum()))

    # DONE: display mean travel time
    print("Mean travel time : {}".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # DONE: Display counts of user types
    print("Count of user types : {}\n".format(df['User Type'].value_counts()))
    
    # DONE: Display counts of gender
    if ['Gender'] in list(df.columns):
        print("Count of gender : {}\n".format(df['Gender'].value_counts()))

    # DONE: Display earliest, most recent, and most common year of birth
    if ['Birth Year'] in list(df.columns):
        print("Earliest year of birth : {}".format(df['Birth Year'].min()))
        print("Most recent year of birth : {}".format(df['Birth Year'].max()))
        print("Most common year of birth : {}".format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        counter = 1
        
        while True:
            show_raw = input('\n Would you like to see raw data? Enter yes or no.\n')
            if (show_raw.lower() != 'yes'):
                break
            df1 = df.iloc[counter*5-4:counter*5].to_dict(orient='records')
            for item in df1:
                print(item)
            counter += 1

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
