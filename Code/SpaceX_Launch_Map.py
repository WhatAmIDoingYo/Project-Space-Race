import folium
import pandas as pd
import requests
import io
import math
from folium.plugins import MarkerCluster, MousePosition
from folium.features import DivIcon

# Function to calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0
    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Download and read the spacex_launch_geo.csv
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
response = requests.get(url)
spacex_df = pd.read_csv(io.BytesIO(response.content))

# Select relevant columns: Launch Site, Lat, Long, class
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]

# Create launch_sites_df with unique launch sites and their coordinates
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# Task 1: Mark all launch sites on a map
# Initialize the map centered at NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Add a circle and marker for each launch site
for index, site in launch_sites_df.iterrows():
    coordinate = [site['Lat'], site['Long']]
    # Add circle
    circle = folium.Circle(coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup(site['Launch Site']))
    # Add marker with label
    marker = folium.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site['Launch Site'],
        )
    )
    site_map.add_child(circle)
    site_map.add_child(marker)

# Task 2: Mark success/failed launches for each site on the map
# Create a marker_color column based on class (1 = green, 0 = red)
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# Create a MarkerCluster object
marker_cluster = MarkerCluster()

# Add marker_cluster to the map
site_map.add_child(marker_cluster)

# Add markers for each launch record
for index, record in spacex_df.iterrows():
    coordinate = [record['Lat'], record['Long']]
    marker = folium.Marker(
        coordinate,
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

# Task 3: Calculate distances from a launch site to proximities
# Example: Calculate distances from CCAFS SLC-40 (28.563197, -80.576820) to proximity points
launch_site = [28.563197, -80.576820]  # CCAFS SLC-40 coordinates
proximities = [
    {'name': 'City (Cape Canaveral)', 'coord': [28.40163, -80.60426], 'distance': None},
    {'name': 'Railway', 'coord': [28.57205, -80.58527], 'distance': None},
    {'name': 'Highway', 'coord': [28.56321, -80.57088], 'distance': None},
    {'name': 'Coastline', 'coord': [28.56367, -80.57163], 'distance': None}
]

# Calculate distances and add markers and lines
for proximity in proximities:
    prox_coord = proximity['coord']
    # Calculate distance
    distance = calculate_distance(launch_site[0], launch_site[1], prox_coord[0], prox_coord[1])
    proximity['distance'] = distance
    # Add marker for proximity
    marker = folium.Marker(
        prox_coord,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s KM</b></div>' % f"{distance:.2f}",
        )
    )
    site_map.add_child(marker)
    # Add line from launch site to proximity
    line = folium.PolyLine(locations=[launch_site, prox_coord], weight=1, color='#3388ff')
    site_map.add_child(line)

# Add MousePosition plugin to display coordinates on hover
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=5,
    prefix='Lat:'
)
site_map.add_child(mouse_position)

# Save the map to an HTML file
site_map.save('spacex_launch_map.html')

# Print proximity distances for reference
print("Task 3 - Distances from CCAFS SLC-40 to proximities:")
for proximity in proximities:
    print(f"{proximity['name']}: {proximity['distance']:.2f} KM")