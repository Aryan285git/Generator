import random
from faker import Faker
import pandas as pd

fake = Faker()

def generate_record():
    record = {
        "Id": None,
        "Start time": fake.date_time_this_year(),
        "Completion time": fake.date_time_this_year(),
        "Email": "anonymous",
        "Name": fake.first_name(),
        "Full Name": fake.name(),
        "Gender": random.choice(["Man", "Women"]),
        "Date of Birth": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "Check-out Date": fake.date_this_year(),
        "Purpose of Visit": random.choice(["Business", "Vacation", "Function"]),
        "How did you discover us?": random.choice(["Hotel Booking Site", "Internet Advertisement", "Word of Mouth", "Organization"]),
        "Feedback.Staff Attitude": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Check-in Process": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Room Service": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Room Cleanliness": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Food Quality": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Variety of Food": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Broadband & TV": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Feedback.Gym": random.choice(["Excellent", "Very Good", "Good", "Average", "Poor"]),
        "Rate your overall experience in our hotel": random.randint(1, 5),
        "How likely are you to recommend us to a friend or colleague?": random.randint(1, 10)
    }
    return record

def generate_data(num_records):
    data = []
    for i in range(num_records):
        record = generate_record()
        record["Id"] = i + 1
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

df = generate_data(3000)

# Load the template
template_path = 'D:/Projects/College/Generator/template.xlsx'
output_path = 'D:/Projects/College/Generator/output.xlsx'

# Append data to the template
with pd.ExcelWriter(template_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
    # Write data starting from the first empty row
    book = pd.read_excel(template_path, sheet_name='Sheet1', engine='openpyxl')
    startrow = book.shape[0]
    df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=startrow)

print(f"Data successfully written to {output_path}")