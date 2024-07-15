# gps-toll-based-system-simulation-using-python
### Overview
The GPS Toll System is a modern toll collection solution that uses GPS data to track vehicle movements and calculate toll fees based on distance, vehicle type, peak hours, and frequent user discounts. This project includes real-time vehicle tracking, dynamic toll calculation, emergency monitoring, and a command-line interface for easy interaction.

### Features
* Real-time GPS tracking: Tracks vehicle locations and displays them on an interactive map.
* Dynamic toll calculation: Calculates toll fees based on distance, vehicle type, peak hours, and discounts.
* Emergency monitoring: Alerts if a vehicle is stationary for too long.
* Simulation: Uses simpy to simulate vehicle movements and interactions.
* Command-line interface: Allows users to interact with the system easily.
* Transaction logging: Records all transactions and provides a history log.

### Requirements
* Python 3.12 or any version in general python 3.x
* Libraries needed to be installed : requests, folium, datetime, math, simpy, pandas, geopandas, shapely, geopy, selenium, webdriver_manager, matplotlib
# Commands to install all these libraries:
* pip install requests
* pip install simpy
* and similarly install other necessary libraries with the same format
(or)
* #Create a requirements.txt file and list all the necessary libraries in that file in the below format:
*
echo "requests
folium
datetime
simpy
pandas
geopandas
shapely
geopy
selenium
webdriver_manager
matplotlib" > requirements.txt
*
* ##command to install all the libraries in the requirement.txt file
* pip install -r requirements.txt

## to run all these commands ensure you create your own environment terminal 
* and create a folder called admin under users in the path of your python application
* and save the typed python program file inside the admin folder with any file name
## steps to create your environment terminal
* open terminal of your python version
* press windows symbol+R
* in the popping window give name and 'cmd' and save. This opens your environment terminal.
* next give the command 'cd'
* eg.C:\Users\Admin>cd
   * C:\Users\Admin...
* after installing all the necessary libraries run the file name
* eg.C:\Users\Admin>python gps_locator.py  //here the file name is gps_locator
* now your terminal is ready to run the program to obtain the output.



## Installation
* Clone the repository: code- git clone https://github.com/yourusername/gps-toll-system.git
cd gps-toll-system
* Install dependencies: code- pip install -r requirements.txt
# Run the main script: code- python gps_toll_system.py
# Interact with the command-line interface:
* Add vehicles
* Simulate passages
* View transaction history
* View current location on map
* Query the number of vehicles on the toll road
* Check speed limits

### imported libraries used for different functionalities:
* -[requests: to make HTTP requests.]
* -[folium: for generating maps.]
* -[datetime: for handling date and time.]
* -[time: for handling time-related tasks.]
* -[math: for mathematical calculations.]
* -[simpy: for event-driven simulation.]
* -[random: for generating random numbers.]
* -[pandas: for data manipulation and analysis.]
* -[geopandas: for geospatial data handling.]
* -[shapely.geometry: for handling geometric objects.]
* -[geopy.distance: for calculating geodesic distances.]
-[selenium and webdriver_manager: for automating web browser actions.]
-[matplotlib.pyplot: for plotting graphs.]

### Function: locationCoordinates
* function fetches the current coordinates using the IP address.
* requests.get('https://ipinfo.io'): makes an HTTP GET request to fetch location data.
* The response is parsed to extract latitude, longitude, city, and state.
* If an error occurs, it prints the error and returns None.

### Function: gps_locator
* This function creates an HTML file with a map showing the current location.
* It initializes a folium.Map object centered at (0, 0) with zoom level 2.
* It calls locationCoordinates to get the current location.
* If the location is valid, it adds a marker on the map.
* The map is saved as an HTML file named with the current date.
* If any error occurs, it prints the error and returns None.
### Function: haversine
 * This function calculates the great-circle distance between two points on the Earth using the Haversine formula.
* The latitude and longitude are converted to radians.
* It computes the differences in latitude and longitude.
* It applies the Haversine formula to compute the distance in kilometers.

  ### Class: Vehicle
*  The Vehicle class represents a vehicle in the simulation.
* The __init__ method initializes the vehicle with its type, license plate, start and end coordinates, and the simulation environment.
* The move method simulates the vehicle's movement by calculating the travel time and updating the vehicle's location once the travel time has passed.

### Class: TollSystem
* The TollSystem class handles toll operations and vehicle management.
* The __init__ method initializes the system with toll rates, multipliers, discount thresholds, transactions, vehicles, toll zones, and emergency threshold.
* The create_toll_zones method defines toll zones as polygons.
* The calculate_toll method calculates the toll fee based on the vehicle type, distance, peak hour, and frequent user status.
* The simulate_passage method simulates a



   ## Contributing
* Contributions are welcome! Please create an issue or submit a pull request with any improvements.

 

  ## Report

* Download the full project report [here](https://drive.google.com/file/d/14BLVPoxszy1Y2yyVz72wPpGHOc8g1Alr/view?usp=drivesdk).

* developed by Margaret Sheela. c
For support or inquiries, please contact [margaretsheelac.ec2022@vemanait.edu.in].
