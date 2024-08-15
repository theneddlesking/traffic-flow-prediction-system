# traffic-flow-prediction-system

This project implements a traffic flow prediction system, or TFPS for short. Accurate and timely traffic flow information is important for traffic authorities (such as VicRoads) to identify congested areas and implement traffic management policies to reduce congestion. 

It is also critical for route guidance systems (such as Google maps) to calculate the best routes for their users considering the traffic conditions potentially experienced along each route. Thanks to recent advancement in sensor technologies, traffic authorities are able to collect massive amount of traffic data to enable accurate predictions of traffic information (such as traffic flow, speed, travel time, etc.). 

The solution utilises historical traffic data for traffic flow prediction. The system will start as a basic system but then will become more advanced by adding further improvements and extensions.

## Installation

### Python (API / Model)

To install dependencies
```pip install -r -requirements```

To run the api use
```uvicorn test_api:app --reload```

### Node (Frontend)

Run with /frontend as the current working directory.
```cd frontend```

To install dependencies
```npm install```

To run in development mode use
```npm run dev```

To create a new build use
```npm run build```