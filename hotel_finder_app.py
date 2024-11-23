import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Load data from the Judging Factor file
data_file = 'D:/Projects/College/Generator/judging_factor.xlsx'
df = pd.read_excel(data_file)

# Function to show options for city and area selection
def get_city_area_options():
    cities = df["City"].unique()
    areas = df["Area"].unique()

    city_choice = st.selectbox("Select City", cities)
    areas_in_city = df[df["City"] == city_choice]["Area"].unique()
    area_choice = st.selectbox(f"Select Area in {city_choice}", areas_in_city)

    return city_choice, area_choice

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
    st.title("Hotel Finder")

    # Get available city and area options from the user
    city, area = get_city_area_options()

    # Filter by city and area
    filtered_df = df[(df["City"].str.lower() == city.lower()) & 
                     (df["Area"].str.lower() == area.lower())]

    if filtered_df.empty:
        st.write(f"No hotels found in {area}, {city}.")
        return

    st.write(f"\nHotels available in {area}, {city}:")
    st.write(filtered_df[["Hotel Name", "Judging_Factor", "Number_of_Visitors"]].drop_duplicates())

    # Set Seaborn style for a more refined look
    sns.set(style="whitegrid")

    # Calculate the 33rd and 66th percentiles for dynamic color coding
    low_percentile = np.percentile(filtered_df["Judging_Factor"], 33)
    high_percentile = np.percentile(filtered_df["Judging_Factor"], 66)

    # Create a figure for the plot
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Sort by Judging Factor for better visualization
    sorted_df = filtered_df.sort_values("Judging_Factor", ascending=True)

    # Generate color for each hotel based on Judging Factor and percentiles
    colors = sorted_df["Judging_Factor"].apply(lambda x: get_color(x, low_percentile, high_percentile))

    # Create a vertical bar plot for Judging Factor
    ax1.bar(sorted_df["Hotel Name"], sorted_df["Judging_Factor"], color=colors, label='Judging Factor')

    # Set title and labels for Judging Factor plot
    ax1.set_title(f"Judging Factor and Number of Visitors for Hotels in {area}, {city}", fontsize=16, weight='bold')
    ax1.set_xlabel('Hotel Name', fontsize=14)
    ax1.set_ylabel('Judging Factor', fontsize=14)
    ax1.set_xticklabels(sorted_df["Hotel Name"], rotation=90)

    # Create second y-axis for Number of Visitors
    ax2 = ax1.twinx()
    ax2.plot(sorted_df["Hotel Name"], sorted_df["Number_of_Visitors"], color='blue', marker='o', label='Number of Visitors')

    # Set y-axis labels for Number of Visitors
    ax2.set_ylabel('Number of Visitors', fontsize=14)
    
    # Add gridlines and improve layout for better spacing
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(fig)

    # Display Best and Least Rated Hotels
    best_rated_hotel = filtered_df.loc[filtered_df["Judging_Factor"].idxmax()]
    least_rated_hotel = filtered_df.loc[filtered_df["Judging_Factor"].idxmin()]

    st.markdown("### Best Rated Hotel in the Area:")
    st.markdown(f"**Hotel Name**: {best_rated_hotel['Hotel Name']}")
    st.markdown(f"**Judging Factor**: {best_rated_hotel['Judging_Factor']:.2f}")
    st.markdown(f"<p style='color:green;'>⭐ Excellent Rating</p>", unsafe_allow_html=True)

    st.markdown("### Least Rated Hotel in the Area:")
    st.markdown(f"**Hotel Name**: {least_rated_hotel['Hotel Name']}")
    st.markdown(f"**Judging Factor**: {least_rated_hotel['Judging_Factor']:.2f}")
    st.markdown(f"<p style='color:red;'>⚠️ Poor Rating</p>", unsafe_allow_html=True)

    # Display Most and Least Visited Hotels (using 'Number_of_Visitors')
    most_visited_hotel = filtered_df.loc[filtered_df["Number_of_Visitors"].idxmax()] if 'Number_of_Visitors' in filtered_df else None
    least_visited_hotel = filtered_df.loc[filtered_df["Number_of_Visitors"].idxmin()] if 'Number_of_Visitors' in filtered_df else None

    if most_visited_hotel is not None:
        st.markdown("### Most Visited Hotel in the Area:")
        st.markdown(f"**Hotel Name**: {most_visited_hotel['Hotel Name']}")
        st.markdown(f"**Number of Visits**: {most_visited_hotel['Number_of_Visitors']}")
        st.markdown(f"<p style='color:blue;'>🏆 Most Popular</p>", unsafe_allow_html=True)
    
    if least_visited_hotel is not None:
        st.markdown("### Least Visited Hotel in the Area:")
        st.markdown(f"**Hotel Name**: {least_visited_hotel['Hotel Name']}")
        st.markdown(f"**Number of Visits**: {least_visited_hotel['Number_of_Visitors']}")
        st.markdown(f"<p style='color:orange;'>❌ Least Popular</p>", unsafe_allow_html=True)

    st.markdown("### Thank you for using the Hotel Finder!")

# Run the search function in Streamlit
if __name__ == "__main__":
    search_hotel()
