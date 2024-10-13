import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(path):
    df = pd.read_excel(path)
    return df

def basic_statistics(df):
    print("Basic Statistics:")
    print(df.describe())

def distribution_of_categorical(df):
    print("Distribution of Categorical Variables:")
    for column in df.select_dtypes(include=['object']).columns:
        print(f"\n{column}:\n", df[column].value_counts())

def plot_histogram(df, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def plot_categorical_distribution(df, column):
    plt.figure(figsize=(10, 6))
    sns.countplot(y=column, data=df, order=df[column].value_counts().index)
    plt.title(f'Distribution of {column}')
    plt.xlabel('Count')
    plt.ylabel(column)
    plt.show()

def analyze_data(df):
    basic_statistics(df)
    distribution_of_categorical(df)
    plot_histogram(df, 'Rate your overall experience in our hotel')
    plot_histogram(df, 'How likely are you to recommend us to a friend or colleague?')
    plot_categorical_distribution(df, 'Gender')
    plot_categorical_distribution(df, 'Purpose of Visit')

# Define input path for the generated data file
input_path = 'D:/Projects/College/Generator/output_new.xlsx'

# Load the data
df = load_data(input_path)

# Analyze the loaded data
analyze_data(df)
