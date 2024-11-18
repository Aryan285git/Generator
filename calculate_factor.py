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

# Normalize experience columns to a 5-point scale (if on a 10-point scale)
df["Rate your overall experience in our hotel"] = df["Rate your overall experience in our hotel"] / 2
df["How likely are you to recommend us to a friend or colleague?"] = df["How likely are you to recommend us to a friend or colleague?"] / 2

# Calculate Judging Factor for each visit
df["Judging Factor"] = (
    df[feedback_columns].sum(axis=1) +  # Sum feedback scores (weight 1)
    2 * df[experience_columns].sum(axis=1)  # Add experience scores with weight 2
)

# Group by 'Hotel Name' and calculate the average Judging Factor for each hotel
df_grouped = df.groupby(['Hotel Name', 'City', 'Area'], as_index=False)['Judging Factor'].mean()

# Select only the required columns
df_simplified = df_grouped[["Hotel Name", "City", "Area", "Judging Factor"]]

# Save the simplified dataset with average Judging Factor
output_file = 'D:/Projects/College/Generator/judging_factor.xlsx'
df_simplified.to_excel(output_file, index=False)

print(f"Simplified Judging Factor file with averages successfully created: {output_file}")
