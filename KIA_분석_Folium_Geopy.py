import pandas as pd
import folium
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import matplotlib.pyplot as plt

# Load the provided CSV file
file_path = r'C:\Mtest\개인연습\팀플\야구\KIA_데이터.csv'  # Use raw string to avoid escape issues
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
data.head()

# Coordinates for each team/stadium
locations = {
    "광주": (35.160124, 126.852121), 
    "수원": (37.2978428909635, 127.011348102567),  
    "창원": (35.2219848625101, 128.579580117268), 
    "인천": (37.4980879456876, 126.867026290623), 
    "잠실": (37.5112525852452, 127.072863377526), 
    "부산": (35.19403166, 129.06151836), 
    "대구": (35.8411289243023, 128.6812363722680), 
    "고척": (37.4980879456876, 126.867026290623), 
    "대전": (36.3173370007388, 127.428013823451)
}

# Extract unique stadiums and years for mapping
stadiums = data[['구장', '연도']].drop_duplicates()

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get coordinates of stadiums
def get_coordinates(location):
    try:
        return geolocator.geocode(location)
    except GeocoderTimedOut:
        return None

# Create a base Folium map centered around South Korea
map_korea = folium.Map(location=[35.9078, 127.7669], zoom_start=7)

# Dictionary to store stadiums with coordinates
stadium_coords = {}

# Get coordinates for each unique stadium
for index, row in stadiums.iterrows():
    location = row['구장']
    if location not in stadium_coords and location in locations:
        # Use predefined locations if available
        coord = locations[location]
        stadium_coords[location] = coord
        folium.Marker(coord, popup=location).add_to(map_korea)

# Connect team travel paths
prev_location = None
for index, row in data.iterrows():
    stadium = row['구장']
    if stadium in stadium_coords:
        coord = stadium_coords[stadium]
        if prev_location:
            folium.PolyLine([prev_location, coord], color="blue", weight=2.5, opacity=0.8).add_to(map_korea)
        prev_location = coord

# Save the map
map_save_path = 'C:\Mtest\개인연습\팀플\야구\kia_travel_route.html'
map_korea.save(map_save_path)

# Return the path to the generated map file
print(f"Map saved to: {map_save_path}")

# Group the data by year to observe cumulative win rate and distance traveled
grouped_data = data.groupby('연도').agg({
    '누적승률': 'last',
    '누적이동거리': 'sum'
}).reset_index()

# Plotting the relationship between cumulative travel distance and win rate
plt.figure(figsize=(10, 6))
plt.scatter(grouped_data['누적이동거리'], grouped_data['누적승률'], color='blue', s=100, edgecolor='black', alpha=0.7)
plt.plot(grouped_data['누적이동거리'], grouped_data['누적승률'], color='green', linestyle='--')

plt.title('Correlation Between Cumulative Travel Distance and Win Rate by Year')
plt.xlabel('Cumulative Travel Distance (km)')
plt.ylabel('Cumulative Win Rate')
plt.grid(True)
plt.show()
