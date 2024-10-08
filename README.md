# traffic-flow-prediction-system

This project implements a traffic flow prediction system, or TFPS for short. Accurate and timely traffic flow information is important for traffic authorities (such as VicRoads) to identify congested areas and implement traffic management policies to reduce congestion. 

It is also critical for route guidance systems (such as Google maps) to calculate the best routes for their users considering the traffic conditions potentially experienced along each route. Thanks to recent advancement in sensor technologies, traffic authorities are able to collect massive amount of traffic data to enable accurate predictions of traffic information (such as traffic flow, speed, travel time, etc.). 

The solution utilises historical traffic data for traffic flow prediction. The system will start as a basic system but then will become more advanced by adding further improvements and extensions.

## Installation

### Run init.sh

```./init.sh```

This will start build the frontend and start up the backend.
If you make changes you can simply rerun the script.

The app will be running at ```localhost:8000/app```

### Training

To train a model use:

```python train.py --location <location_name> --model <model_name>```

However, you need to the data files to already exist for that location.
To add a location use:

```python vic_convert.py --location <location_name>```

### Run Model

To see the results use:

```python main.py --location <location_name>```

This will create a graph visualisation in the image directory called results.png.

### Frontend Dev

If you are only working on the frontend, first init the app like above.

But then you can run the dev build:

First cd into the frontend directory

```cd frontend```

And then start up the dev server

```npm run dev```

The development app will be running at ```localhost:5173```

### Backend Dev

If you are only working on the backend and API, first init the app like above.

From the root folder start up the dev server

```uvicorn app:app --reload```
