import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def load_data(path):
    df = pd.read_excel(path)
    # Convert the Check-out Date column to datetime if it's not already in datetime format
    df['Check-out Date'] = pd.to_datetime(df['Check-out Date'], errors='coerce')
    return df

def filter_data(df, **filters):
    for key, value in filters.items():
        if value:
            if key == 'Check-out Date' and isinstance(value, tuple):
                # Filter data based on date range
                start_date, end_date = value
                df = df[(df['Check-out Date'] >= start_date) & (df['Check-out Date'] <= end_date)]
            else:
                df = df[df[key] == value]
    return df

def plot_histogram(df, column, title):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def plot_categorical_distribution(df, column, title):
    plt.figure(figsize=(10, 6))
    sns.countplot(y=column, data=df, order=df[column].value_counts().index)
    plt.title(title)
    plt.xlabel('Count')
    plt.ylabel(column)
    plt.show()

def analyze_data(df, filters):
    filter_description = " and ".join([f"{key}={value}" for key, value in filters.items() if value])
    title_suffix = f" with {filter_description}" if filter_description else ""
    
    plot_histogram(df, 'How likely are you to recommend us to a friend or colleague?', f'Likelihood to Recommend{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Staff Attitude', f'Staff Attitude Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Check-in Process', f'Check-in Process Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Room Service', f'Room Service Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Room Cleanliness', f'Room Cleanliness Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Food Quality', f'Food Quality Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Variety of Food', f'Variety of Food Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Broadband & TV', f'Broadband & TV Feedback{title_suffix}')
    plot_categorical_distribution(df, 'Feedback.Gym', f'Gym Feedback{title_suffix}')

def get_date_filter():
    print("Do you want to filter by date range? (yes/no)")
    response = input().strip().lower()
    if response == 'yes':
        # User provides date range
        start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)
            return ('Check-out Date', (start_date, end_date))
        except ValueError:
            print("Invalid date format. Please try again.")
            return None
    elif response == 'no':
        # Default to no date filter
        return None
    else:
        print("Invalid response. Please try again.")
        return get_date_filter()

def get_last_month_filter():
    print("Do you want to filter by the last month? (yes/no)")
    response = input().strip().lower()
    if response == 'yes':
        # Get the first and last date of last month
        today = datetime.today()
        first_day_last_month = today.replace(day=1) - timedelta(days=1)
        first_day_last_month = first_day_last_month.replace(day=1)
        last_day_last_month = first_day_last_month.replace(day=1) + pd.offsets.MonthEnd(1)
        return ('Check-out Date', (first_day_last_month, last_day_last_month))
    elif response == 'no':
        return None
    else:
        print("Invalid response. Please try again.")
        return get_last_month_filter()

# Define input path for the generated data file
input_path = 'output_new.xlsx'

# Load the data
df = load_data(input_path)

# Get user input for filtering
print("Please enter your criteria (leave blank for no filter):")
criteria = {
    "Gender": input("Enter Gender (Man/Women): ").strip() or None,
    "Purpose of Visit": input("Enter Purpose of Visit (Business/Vacation/Function): ").strip() or None,
    "Rate your overall experience in our hotel": input("Enter Overall Experience Rating (1-5): ").strip() or None,
    "Feedback.Staff Attitude": input("Enter Feedback for Staff Attitude (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Check-in Process": input("Enter Feedback for Check-in Process (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Room Service": input("Enter Feedback for Room Service (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Room Cleanliness": input("Enter Feedback for Room Cleanliness (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Food Quality": input("Enter Feedback for Food Quality (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Variety of Food": input("Enter Feedback for Variety of Food (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Broadband & TV": input("Enter Feedback for Broadband & TV (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
    "Feedback.Gym": input("Enter Feedback for Gym (Excellent/Very Good/Good/Average/Poor): ").strip() or None,
}

# Convert numeric inputs to the appropriate type
for key in ["Rate your overall experience in our hotel"]:
    if criteria[key]:
        criteria[key] = int(criteria[key])

# Get date-based filtering criteria
date_filter = get_date_filter()
if not date_filter:
    date_filter = get_last_month_filter()

# If a date filter was applied, add it to the criteria
if date_filter:
    criteria[date_filter[0]] = date_filter[1]

# Filter data based on user input
filtered_df = filter_data(df, **criteria)

# Analyze the filtered data
if not filtered_df.empty:
    analyze_data(filtered_df, criteria)
else:
    print("No data matches the given criteria.")