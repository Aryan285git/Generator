import random
from faker import Faker
import pandas as pd

fake = Faker()

# Define sample cities and areas
cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
]
areas = [
    ["Andheri", "Borivali", "Malad", "Dadar", "Kurla"],
    ["Connaught Place", "Chandni Chowk", "Saket", "Karol Bagh", "Dwarka"],
    ["Whitefield", "Koramangala", "MG Road", "Indiranagar", "Jayanagar"],
    ["Banjara Hills", "Gachibowli", "Kukatpally", "Secunderabad", "Hitech City"],
    ["Adyar", "T. Nagar", "Velachery", "Anna Nagar", "Kodambakkam"],
    ["Park Street", "Salt Lake", "Howrah", "Esplanade", "Tollygunge"],
    ["Koregaon Park", "Baner", "Kothrud", "Hinjawadi", "Shivaji Nagar"],
    ["Navrangpura", "Paldi", "Vastrapur", "Satellite", "Maninagar"],
    ["C-Scheme", "Malviya Nagar", "Vaishali Nagar", "Amer", "Tonk Road"],
    ["Hazratganj", "Gomti Nagar", "Aliganj", "Indira Nagar", "Aminabad"]
]

# Generate a list of hotel names for each area
def generate_hotel_names():
    hotel_names = []
    for i in range(1, random.randint(10, 15)):  # Create 10-15 unique hotels per area
        hotel_names.append(f"Hotel {fake.unique.word().capitalize()}{i}")
    return hotel_names

# Generate a single record
def generate_record(hotel_name, area, city, customer_id):
    record = {
        "Id": customer_id,
        "Hotel Name": hotel_name,
        "Area": area,
        "City": city,
        "Start time": fake.date_time_this_year(),
        "Completion time": fake.date_time_this_year(),
        "Email": fake.email(),
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
        "How likely are you to recommend us to a friend or colleague?": random.randint(1, 10),
    }
    return record

# Generate data for multiple visits
def generate_data():
    data = []
    customer_id = 1
    for city, city_areas in zip(cities, areas):
        for area in city_areas:
            hotel_names = generate_hotel_names()
            for _ in range(random.randint(50, 80)):  # Number of visits per area
                hotel_name = random.choice(hotel_names)  # Randomly assign a hotel
                record = generate_record(hotel_name, area, city, customer_id)
                data.append(record)
                customer_id += 1
    return pd.DataFrame(data)

# Generate data and save to file
df = generate_data()

output_path = 'output_new.xlsx'
df.to_excel(output_path, index=False)

print(f"Data successfully written to {output_path}")
