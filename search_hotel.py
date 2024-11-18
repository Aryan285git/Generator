import pandas as pd
import matplotlib.pyplot as plt

# Load data from the Judging Factor file
data_file = 'D:/Projects/College/Generator/judging_factor.xlsx'
df = pd.read_excel(data_file)

# Search function
def search_hotel():
    print("Welcome to the Hotel Finder!")
    city = input("Enter the city you'd like to search in: ").strip()
    area = input("Enter the area you'd like to search in: ").strip()

    # Filter by city and area
    filtered_df = df[(df["City"].str.lower() == city.lower()) & 
                     (df["Area"].str.lower() == area.lower())]

    if filtered_df.empty:
        print(f"No hotels found in {area}, {city}.")
        return

    print(f"\nHotels available in {area}, {city}:")
    print(filtered_df[["Hotel Name", "Judging Factor"]].drop_duplicates())

    # Plot the Judging Factor for all available hotels
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_df["Hotel Name"], filtered_df["Judging Factor"], color='skyblue')
    plt.xlabel('Hotel Name')
    plt.ylabel('Judging Factor')
    plt.title(f'Judging Factor for Hotels in {area}, {city}')
    plt.xticks(rotation=90)  # Rotate hotel names for better visibility
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()

    print("\nThank you for using the Hotel Finder!")

# Run the search
if __name__ == "__main__":
    search_hotel()
