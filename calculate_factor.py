import pandas as pd

# Load the dataset
data_file = 'D:/Projects/College/Generator/output_new.xlsx'
df = pd.read_excel(data_file)

# Define the feedback columns
feedback_columns = [
    "Feedback.Staff Attitude", "Feedback.Check-in Process", 
    "Feedback.Room Service", "Feedback.Room Cleanliness", 
    "Feedback.Food Quality", "Feedback.Variety of Food", 
    "Feedback.Broadband & TV", "Feedback.Gym"
]

# Define experience columns
experience_columns = [
    "Rate your overall experience in our hotel",
    "How likely are you to recommend us to a friend or colleague?"
]

# Map qualitative feedback to a numerical scale
feedback_mapping = {
    "Excellent": 5,
    "Very Good": 4,
    "Good": 3,
    "Average": 2,
    "Poor": 1
}

# Apply mapping to feedback columns
for column in feedback_columns:
    df[column] = df[column].map(feedback_mapping)

# Normalize experience columns to a 5-point scale (if already on a different scale)
df["Rate your overall experience in our hotel"] = df["Rate your overall experience in our hotel"] / df["Rate your overall experience in our hotel"].max() * 5
df["How likely are you to recommend us to a friend or colleague?"] = df["How likely are you to recommend us to a friend or colleague?"] / df["How likely are you to recommend us to a friend or colleague?"].max() * 5

# Calculate Judging Factor for each visit
df["Judging Factor"] = (
    df[feedback_columns].sum(axis=1) +  # Sum feedback scores (weight 1)
    2 * df[experience_columns].sum(axis=1)  # Add experience scores with weight 2
)

# Group by 'Hotel Name', 'City', and 'Area' to calculate metrics
df_grouped = df.groupby(['Hotel Name', 'City', 'Area'], as_index=False).agg(
    Judging_Factor=('Judging Factor', 'mean'),  # Average Judging Factor
    Number_of_Visitors=('Hotel Name', 'count')  # Count of visits
)

# Save the simplified dataset with average Judging Factor and visitor count
output_file = 'judging_factor.xlsx'
df_grouped.to_excel(output_file, index=False)

print(f"Simplified Judging Factor file with averages and visitor counts successfully created: {output_file}")
