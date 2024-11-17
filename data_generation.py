import random
from faker import Faker
import pandas as pd

fake = Faker()

def generate_record(hotels, areas, cities):
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
        "Hotel Name": random.choice(hotels),
        "Area": random.choice(areas),
        "City": random.choice(cities),
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
    hotels = [f"Hotel {i}" for i in range(1, 21)]  # 20 unique hotel names
    areas = [f"Area {i}" for i in range(1, 8)]  # 7 areas
    cities = [f"City {i}" for i in range(1, 11)]  # 10 cities

    data = []
    for i in range(num_records):
        record = generate_record(hotels, areas, cities)
        record["Id"] = i + 1
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

# Generate data
df = generate_data(3000)

# Save to Excel
output_path = 'D:/Projects/College/Generator/output_new.xlsx'
df.to_excel(output_path, index=False)
print(f"Data successfully written to {output_path}")
