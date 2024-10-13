import random
from faker import Faker
import pandas as pd
from openpyxl import load_workbook

fake = Faker()

def generate_record():
    record = {
        "Id": None,
        "Start time": fake.date_time_this_year(),
        "Completion time": fake.date_time_this_year(),
        "Email": "anonymous",
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

def adjust_column_widths(path):
    wb = load_workbook(path)
    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    wb.save(path)

# Generate data
df = generate_data(3000)

# Define output path for a new file
output_path = 'D:/Projects/College/Generator/output_new.xlsx'

# Write data to a new Excel file
df.to_excel(output_path, index=False)

# Adjust column widths in the Excel file
adjust_column_widths(output_path)

print(f"Data successfully written to {output_path}")
