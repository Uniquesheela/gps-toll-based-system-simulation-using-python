import requests
import folium
import datetime
import time
import math
import simpy
import random
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt

# This method will return our actual coordinates using our IP address
def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data.get('loc')
        if loc:
            lat, long = map(float, loc.split(','))
            city = data.get('city', 'Unknown')
            state = data.get('region', 'Unknown')
            return lat, long, city, state
        else:
            raise ValueError("Location coordinates not found in API response.")
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None, None, None, None

# This method will fetch our coordinates and create an HTML file of the map
def gps_locator():
    obj = folium.Map(location=[0, 0], zoom_start=2)
    try:
        lat, long, city, state = locationCoordinates()
        if lat is None or long is None:
            raise ValueError("Unable to fetch coordinates.")
        
        print(f"You Are in {city},{state}")
        print(f"Your latitude = {lat} and longitude = {long}")
        folium.Marker([lat, long], popup='Current Location').add_to(obj)
        
        today_date = datetime.datetime.now().date()
        fileName = f"Location_{today_date}.html"
        obj.save(fileName)
        return fileName
    except Exception as e:
        print(f"Error creating map: {e}")
        return None
# Haversine function to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_of_earth_km = 6371.0
    distance = radius_of_earth_km * c

    return distance

class Vehicle:
    def __init__(self, env, vehicle_type, license_plate, start_lat, start_lon, end_lat, end_lon):
        self.env = env
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.current_lat = start_lat
        self.current_lon = start_lon
        self.route = [(start_lat, start_lon), (end_lat, end_lon)]
        self.start_time = self.env.now
        self.speed = 60  # Assuming average speed of 60 km/h

    def move(self):
        distance = geodesic((self.start_lat, self.start_lon), (self.end_lat, self.end_lon)).km
        travel_time = distance / self.speed * 60  # converting to minutes
        yield self.env.timeout(travel_time)
        self.current_lat, self.current_lon = self.end_lat, self.end_lon
        print(f'{self.license_plate} reached destination at {self.env.now}')

class TollSystem:
    def __init__(self, env):
        self.env = env
        self.toll_rates = {
            'car': 0.05 * 75,    # rate per kilometer for cars in rupees
            'truck': 0.1 * 75,   # rate per kilometer for trucks in rupees
            'motorcycle': 0.03 * 75  # rate per kilometer for motorcycles in rupees
        }
        self.peak_hour_multiplier = 1.2  # 20% increase during peak hours
        self.discount_threshold = 1000 * 75   # threshold for frequent user discount in rupees
        self.discount_percentage = 0.1   # 10% discount for frequent users
        self.transactions = []
        self.vehicles = []
        self.toll_zones = self.create_toll_zones()
        self.emergency_threshold = 10  # in minutes

    def create_toll_zones(self):
        # Define toll zones as polygons
        toll_zones = [
            Polygon([(12.9, 77.5), (13.0, 77.5), (13.0, 77.6), (12.9, 77.6)]),
            Polygon([(12.8, 77.4), (12.9, 77.4), (12.9, 77.5), (12.8, 77.5)])
        ]
        return toll_zones

    def calculate_toll(self, vehicle, distance, is_peak_hour=False, is_frequent_user=False):
        if vehicle.vehicle_type in self.toll_rates:
            rate_per_km = self.toll_rates[vehicle.vehicle_type]
            if is_peak_hour:
                rate_per_km *= self.peak_hour_multiplier
            toll_fee = rate_per_km * distance

            if is_frequent_user and toll_fee > self.discount_threshold:
                toll_fee *= (1 - self.discount_percentage)

            return toll_fee
        else:
            raise ValueError("Unsupported vehicle type")

    def simulate_passage(self, vehicle, is_peak_hour=False, is_frequent_user=False):
        distance = haversine(vehicle.start_lat, vehicle.start_lon, vehicle.end_lat, vehicle.end_lon)
        toll_fee = self.calculate_toll(vehicle, distance, is_peak_hour, is_frequent_user)
        transaction = {
            'vehicle': vehicle,
            'distance': distance,
            'toll_fee': toll_fee,
            'timestamp': datetime.datetime.now()
        }
        self.transactions.append(transaction)
        return toll_fee

    def add_vehicle(self, vehicle_type, license_plate, start_lat, start_lon, end_lat, end_lon):
        new_vehicle = Vehicle(self.env, vehicle_type, license_plate, start_lat, start_lon, end_lat, end_lon)
        self.vehicles.append(new_vehicle)
        return new_vehicle

    def get_transaction_history(self):
        return self.transactions

    def get_vehicles(self):
        return self.vehicles

    def emergency_check(self):
        for vehicle in self.vehicles:
            if self.env.now - vehicle.start_time > self.emergency_threshold:
                print(f'Emergency! Vehicle {vehicle.license_plate} has been stationary for too long.')

def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return lat, long, city, state
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None, None, None, None

def gps_locator():
    obj = folium.Map(location=[0, 0], zoom_start=2)
    try:
        lat, long, city, state = locationCoordinates()
        if lat is None or long is None:
            raise ValueError("Unable to fetch coordinates.")
        
        print(f"You Are in {city},{state}")
        print(f"Your latitude = {lat} and longitude = {long}")
        folium.Marker([lat, long], popup='Current Location').add_to(obj)
        
        today_date = datetime.datetime.now().date()
        fileName = f"Location_{today_date}.html"
        obj.save(fileName)
        return fileName
    except Exception as e:
        print(f"Error creating map: {e}")
        return None

# CLI Interface
def main():
    env = simpy.Environment()
    system = TollSystem(env)

    while True:
        print("\n===== GPS Toll System =====")
        print("1. Add Vehicle")
        print("2. Simulate Passage")
        print("3. View Transaction History")
        print("4. View Current Location")
        print("5. Query Number of Vehicles on Toll Road")
        print("6. Check Speed Limit")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            vehicle_type = input("Enter vehicle type (car/truck/motorcycle): ")
            license_plate = input("Enter license plate number: ")
            start_lat = float(input("Enter start point latitude: "))
            start_lon = float(input("Enter start point longitude: "))
            end_lat = float(input("Enter end point latitude: "))
            end_lon = float(input("Enter end point longitude: "))
            vehicle = system.add_vehicle(vehicle_type, license_plate, start_lat, start_lon, end_lat, end_lon)
            env.process(vehicle.move())
            print(f"Vehicle {vehicle.vehicle_type} ({vehicle.license_plate}) added successfully.")

        elif choice == '2':
            vehicles = system.get_vehicles()
            if not vehicles:
                print("No vehicles added yet. Please add a vehicle first.")
                continue

            print("Available vehicles:")
            for idx, vehicle in enumerate(vehicles):
                print(f"{idx + 1}. {vehicle.vehicle_type} ({vehicle.license_plate})")

            vehicle_index = int(input("Select a vehicle to simulate passage: ")) - 1
            vehicle = vehicles[vehicle_index]
            is_peak_hour = input("Is it peak hour? (yes/no): ").lower() == 'yes'
            is_frequent_user = input("Is the vehicle a frequent user? (yes/no): ").lower() == 'yes'

            toll_fee = system.simulate_passage(vehicle, is_peak_hour, is_frequent_user)
            print(f"Simulated passage completed. Toll fee: ₹{toll_fee:.2f}")

        elif choice == '3':
            transactions = system.get_transaction_history()
            print("\nTransaction History:")
            for transaction in transactions:
                print(f"{transaction['timestamp']}: Vehicle {transaction['vehicle'].license_plate} ({transaction['vehicle'].vehicle_type}): Distance {transaction['distance']:.2f} km, Toll fee ₹{transaction['toll_fee']:.2f}")

        elif choice == '4':
            page = gps_locator()
            if page:
                print("\nOpening File.............")
                try:
                    driver = webdriver.Chrome(ChromeDriverManager().install())
                    driver.get(f"file:///{page}")
                    time.sleep(4)
                    driver.quit()
                    print("\nBrowser Closed..............")
                except Exception as e:
                    print(f"Error opening browser: {e}")
            else:
                print("Failed to create map.")

        elif choice == '5':
            num_vehicles = len(system.get_vehicles())
            print(f"Number of vehicles on toll road: {num_vehicles}")

        elif choice == '6':
            vehicles = system.get_vehicles()
            for vehicle in vehicles:
                distance = haversine(vehicle.start_lat, vehicle.start_lon, vehicle.end_lat, vehicle.end_lon)
                time_taken = env.now - vehicle.start_time
                if time_taken > 0:  # Ensure time_taken is not zero
                    speed = distance / (time_taken / 60)
                    print(f"Vehicle {vehicle.license_plate} is moving at {speed:.2f} km/h")
                else:
                    print(f"Vehicle {vehicle.license_plate} has just been added, speed calculation not possible yet.")

        elif choice == '7':
            print("Exiting GPS Toll System. Thank you!")
            break

        else:
            print("Invalid choice. Please enter a valid option (1-7).")

if __name__ == "__main__":
    main()
