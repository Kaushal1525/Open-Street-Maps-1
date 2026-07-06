# Interactive OSRM Multi-Profile Route Planner

## Overview

This project is an interactive route planning application developed using Python, Leaflet.js, and the Open Source Routing Machine (OSRM). It enables users to calculate and compare routes for multiple transportation modes, including driving, cycling, walking, and an estimated railway route.

Users can interactively select a start and destination point by clicking on the map or launch the application directly with geographic coordinates through the command line. The application computes the shortest routes using the public OSRM routing service and visualizes them on an interactive web map.

In addition to route visualization, the application compares travel distance and estimated travel time across different transportation modes, making it useful for navigation research, intelligent transportation systems, and autonomous vehicle route planning.

---

# Features

* Interactive map-based route selection
* Multi-profile route planning
* Driving route calculation
* Cycling route calculation
* Walking route calculation
* Railway travel time estimation
* Interactive Leaflet web map
* Automatic route comparison
* Route distance calculation
* Travel time estimation
* Automatic map generation
* Command-line coordinate support

---

# Technologies Used

* Python 3
* Leaflet.js
* Open Source Routing Machine (OSRM)
* HTML
* JavaScript

---

# Project Structure

```text
OSRM-MultiProfile-Router/
│
├── osrm1.py
├── osrm1_map.html
├── README.md
└── requirements.txt
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/Kaushal1525/OSRM-MultiProfile-Router.git
```

## Navigate to the project directory

```bash
cd OSRM-MultiProfile-Router
```

No external Python libraries are required.

---

# Running the Project

### Interactive Mode

Run the application:

```bash
python osrm1.py
```

The program generates:

```text
osrm1_map.html
```

Open the generated HTML file in your web browser.

---

### Automatic Route Generation

You can also generate a route directly using coordinates:

```bash
python osrm1.py start_lat start_lon end_lat end_lon
```

Example:

```bash
python osrm1.py 16.44224 80.62061 16.44057 80.62291
```

---

### Automatically Open the Map

```bash
python osrm1.py --open
```

or

```bash
python osrm1.py 16.44224 80.62061 16.44057 80.62291 --open
```

---

# User Interaction

The application operates using a simple click-based interface.

1. Click once to select the starting location.
2. Click again to select the destination.
3. The system automatically requests routes for:

   * Driving
   * Cycling
   * Walking
4. A railway travel estimate is also displayed.
5. All routes are visualized simultaneously.

The **Clear** button removes the current route and allows a new route to be created.

---

# Working Principle

The application performs the following operations:

1. Load the interactive Leaflet map.
2. Receive user-selected start and destination points.
3. Send routing requests to the OSRM server.
4. Retrieve the optimal routes for each transportation profile.
5. Draw route polylines on the map.
6. Calculate travel distance.
7. Estimate travel duration.
8. Compute a straight-line railway travel estimate.
9. Display route statistics.

---

# System Architecture

```text
User Input
     │
     ▼
Leaflet Interactive Map
     │
     ▼
OSRM Routing Service
     │
     ▼
Driving Route
Cycling Route
Walking Route
     │
     ▼
Distance Calculation
     │
     ▼
Travel Time Estimation
     │
     ▼
Railway Time Estimation
     │
     ▼
Interactive Route Visualization
```

---

# Transportation Profiles

The application supports the following routing modes.

| Profile | Description                                                              |
| ------- | ------------------------------------------------------------------------ |
| Driving | Road network routing for motor vehicles                                  |
| Cycling | Bicycle routing                                                          |
| Walking | Pedestrian routing                                                       |
| Railway | Straight-line travel time estimation based on configurable average speed |

---

# Railway Estimation

The railway mode estimates travel time using the great-circle distance between the selected locations.

Estimated travel time is computed using:

```text
Travel Time = Distance ÷ Average Train Speed
```

The default average train speed is:

```text
80 km/h
```

This estimate is intended for comparison purposes and does not represent an actual railway network.

---

# Output

The application generates:

### Interactive HTML Map

```text
osrm1_map.html
```

The map displays:

* Start marker
* Destination marker
* Driving route
* Cycling route
* Walking route
* Railway estimate
* Route summaries
* Distance
* Estimated travel time

---

# Applications

* Autonomous Vehicle Route Planning
* Smart Navigation Systems
* Intelligent Transportation Systems
* GIS Research
* Mobility Analysis
* Fleet Management
* Smart Campus Navigation
* Delivery Route Optimization
* Logistics Planning
* Transportation Research

---

# Future Enhancements

* Real-time traffic information
* Multiple destination routing
* Alternative route comparison
* Turn-by-turn navigation
* Public transportation integration
* Elevation-aware routing
* Weather-aware route planning
* GeoHash integration
* GPS live tracking
* Route export to GPX
* Offline routing support
* Autonomous vehicle path planning
* ROS 2 integration
* Digital twin visualization

---

# Requirements

* Python 3.8 or later
* Internet connection for OSRM routing service

---

# Dependencies

This project uses only Python's standard library.

* math
* os
* sys
* webbrowser

Routing and map visualization are handled through embedded Leaflet.js and the public Open Source Routing Machine (OSRM) service.

---

# Author

**Kaushal Reddy**

AI & Autonomous Systems Engineer

GitHub: https://github.com/Kaushal1525
