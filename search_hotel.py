import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data from the Judging Factor file
data_file = 'judging_factor.xlsx'
df = pd.read_excel(data_file)

# Function to show options for city and area selection
def get_city_area_options():
    cities = df["City"].unique()
    areas = df["Area"].unique()
    
    print("\nAvailable Cities:")
    for idx, city in enumerate(cities, 1):
        print(f"{idx}. {city}")
    
    # Validate city selection input
    while True:
        try:
            city_choice = int(input("\nSelect a city by number: "))
            if city_choice < 1 or city_choice > len(cities):
                raise ValueError
            city = cities[city_choice - 1]
            break
        except ValueError:
            print(f"Invalid input! Please select a number between 1 and {len(cities)}.")

    print(f"\nAvailable Areas in {city}:")
    areas_in_city = df[df["City"] == city]["Area"].unique()
    for idx, area in enumerate(areas_in_city, 1):
        print(f"{idx}. {area}")
    
    # Validate area selection input
    while True:
        try:
            area_choice = int(input("\nSelect an area by number: "))
            if area_choice < 1 or area_choice > len(areas_in_city):
                raise ValueError
            area = areas_in_city[area_choice - 1]
            break
        except ValueError:
            print(f"Invalid input! Please select a number between 1 and {len(areas_in_city)}.")

    return city, area

# Function to assign darker, yet soft colors based on Judging Factor using percentiles
def get_color(rating, low_percentile, high_percentile):
    # Darker shades of green, yellow, and red
    if rating >= high_percentile:
        return '#388E3C'  # Dark Green (Excellent)
    elif rating <= low_percentile:
        return '#D32F2F'  # Dark Red (Poor)
    else:
        return '#FBC02D'  # Golden Yellow (Average)

# Search function
def search_hotel():
    print("Welcome to the Hotel Finder!")

    # Get available city and area options
    city, area = get_city_area_options()

    # Filter by city and area
    filtered_df = df[(df["City"].str.lower() == city.lower()) & 
                     (df["Area"].str.lower() == area.lower())]

    if filtered_df.empty:
        print(f"No hotels found in {area}, {city}.")
        return

    print(f"\nHotels available in {area}, {city}:")
    print(filtered_df[["Hotel Name", "Judging_Factor"]].drop_duplicates())

    # Set Seaborn style for a more refined look
    sns.set(style="whitegrid")

    # Calculate the 33rd and 66th percentiles for dynamic color coding
    low_percentile = np.percentile(filtered_df["Judging_Factor"], 33)
    high_percentile = np.percentile(filtered_df["Judging_Factor"], 66)

    # Create a figure for the plot
    plt.figure(figsize=(12, 8))

    # Sort by Judging Factor for better visualization
    sorted_df = filtered_df.sort_values("Judging_Factor", ascending=True)

    # Generate color for each hotel based on Judging Factor and percentiles
    colors = sorted_df["Judging_Factor"].apply(lambda x: get_color(x, low_percentile, high_percentile))

    # Create a vertical bar plot
    bars = plt.bar(sorted_df["Hotel Name"], sorted_df["Judging_Factor"], color=colors)

    # Set title and labels
    plt.title(f"Judging Factor for Hotels in {area}, {city}", fontsize=16, weight='bold')
    plt.xlabel('Hotel Name', fontsize=14)
    plt.ylabel('Judging Factor', fontsize=14)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # Add gridlines for clarity
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add a color legend
    from matplotlib.patches import Patch
    legend_labels = [Patch(color='#388E3C', label='Excellent'),
                     Patch(color='#FBC02D', label='Average'),
                     Patch(color='#D32F2F', label='Poor')]
    plt.legend(handles=legend_labels, loc='upper right')

    # Improve layout for better spacing and readability
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Display Best and Least Rated Hotels
    best_rated_hotel = filtered_df.loc[filtered_df["Judging_Factor"].idxmax()]
    least_rated_hotel = filtered_df.loc[filtered_df["Judging_Factor"].idxmin()]

    print("\nBest Rated Hotel in the Area:")
    print(f"Hotel Name: {best_rated_hotel['Hotel Name']}, Judging Factor: {best_rated_hotel['Judging_Factor']}")

    print("\nLeast Rated Hotel in the Area:")
    print(f"Hotel Name: {least_rated_hotel['Hotel Name']}, Judging Factor: {least_rated_hotel['Judging_Factor']}")

    # Display Most and Least Visited Hotels (using 'Number_of_Visitors')
    most_visited_hotel = filtered_df.loc[filtered_df["Number_of_Visitors"].idxmax()] if 'Number_of_Visitors' in filtered_df else None
    least_visited_hotel = filtered_df.loc[filtered_df["Number_of_Visitors"].idxmin()] if 'Number_of_Visitors' in filtered_df else None

    if most_visited_hotel is not None:
        print("\nMost Visited Hotel in the Area:")
        print(f"Hotel Name: {most_visited_hotel['Hotel Name']}, Visits: {most_visited_hotel['Number_of_Visitors']}")
    
    if least_visited_hotel is not None:
        print("\nLeast Visited Hotel in the Area:")
        print(f"Hotel Name: {least_visited_hotel['Hotel Name']}, Visits: {least_visited_hotel['Number_of_Visitors']}")

    print("\nThank you for using the Hotel Finder!")

# Run the search
if __name__ == "__main__":
    search_hotel()
