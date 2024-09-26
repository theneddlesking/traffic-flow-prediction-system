import axios from 'axios';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import './App.css';
import MapRouting from './MapRouting';

import MapSidebar from './MapSidebar';
import type { Location } from './types';


type RoutingResponse = {
  waypoints: Location[];
  hours_taken: number;
  error?: string;
}


function Map() {
  const [mapInit, setMapInit] = useState(false);
  const [locations, setLocations] = useState<Location[]>([]);
  const [startPoint, setStartPoint] = useState<Location | null>(null);
  const [endPoint, setEndPoint] = useState<Location | null>(null);
  const [waypoints, setWaypoints] = useState<Location[]>([]);

  const [timeOfDay, setTimeOfDay] = useState('12:00');

  const roadSegments = [
    [
      [141.587093, -38.34681],
      [141.58711, -38.34604]
    ],
    [
      [141.58711, -38.34604],
      [141.587122, -38.345727]
    ],
    [
      [141.587122, -38.345727],
      [141.587134, -38.345126],
      [141.587166, -38.34433]
    ]
  ];

  const flippedRoadSegements = roadSegments.map(segment => {
    return segment.map(point => {
      return [point[1], point[0]];
    });
  });

  const allPoints = roadSegments.flat();

  const generateRoute = async (possibleEndPoint?: Location) => {

    const routeEndPoint = possibleEndPoint || endPoint;

    // fetch route from backend
    const res = await axios.get<RoutingResponse>(`http://localhost:8000/routing/route?start_location_id=${startPoint?.location_id}&end_location_id=${routeEndPoint?.location_id}&time_of_day=${timeOfDay}`)

    // handle error
    if (res.data.error) {
      console.error(res.data.error);
      return;
    }

    const routeWaypoints = res.data.waypoints;

    const routeHours = res.data.hours_taken;

    const latOffset = 0.00151;
    const longOffset = 0.0013;

    const adjustedWaypoints = routeWaypoints.map(waypoint => {
      waypoint.lat += latOffset;
      waypoint.long += longOffset;
      return waypoint;
    });
       
    setWaypoints(adjustedWaypoints);

    console.log(`Route takes ${routeHours} hours`);
  }

  useEffect(() => {
    axios.get<{ locations: Location[] }>('http://127.0.0.1:8000/site/locations')
      .then(locations => {
        // remap position based on offset
        const latOffset = 0.00151;
        const longOffset = 0.0013;

        // for some reason the long lat is slightly off
        locations.data.locations.forEach(location => {
          location.lat += latOffset;
          location.long += longOffset;
        });

        setLocations(locations.data.locations);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  const getFlow = async (location_id: number) => {
    return await axios.get<{ flow: number }>(`http://127.0.0.1:8000/site/flow?location_id=${location_id}&time=${timeOfDay}`)
      .then(flow => {
        return flow.data.flow;
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }

  const dotIcon = new Icon({
    iconUrl: 'https://img.icons8.com/?size=100&id=24801&format=png&color=000000',
    iconSize: [15, 15]
  });

  const saveMap = (map: unknown) => {
    if (map) {
      setMapInit(true);
    }
  };

  const setStartPointAndFetchTraffic = async (location: Location | null) => {
    setStartPoint(location);

    if (location !== null) {
      const flow = await getFlow(location.location_id);
      if (flow !== undefined) {
        location.flow = flow;
      }

      if (endPoint !== null) {
        generateRoute();
      }
    }
  };

  const setEndPointAndFetchTraffic = async (location: Location | null) => {
    setEndPoint(location);

    if (location !== null) {
      const flow = await getFlow(location.location_id);
      if (flow !== undefined) {
        location.flow = flow;
      }

      if (startPoint !== null) {
        generateRoute();
      }
    }
  };


  return (
    <div className='map-container'>
      <MapSidebar startPoint={startPoint} endPoint={endPoint} setStartPoint={setStartPointAndFetchTraffic} setEndPoint={setEndPointAndFetchTraffic} locations={locations} />

      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true} ref={saveMap}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          />
        {locations.map(location => (
            <Marker key={location.location_id} position={[location.lat, location.long]} icon={dotIcon}
              eventHandlers={{
                click: async () => {
                  if (startPoint === null) {
                    setStartPoint(location);

                    if (endPoint === null) {
                      generateRoute(location);
                    }

                  } else if (endPoint === null) {
                    setEndPoint(location);
                    generateRoute(location);
                  }
                  
                  const flow = await getFlow(location.location_id);

                  if (flow === undefined) {
                    console.log(`Traffic flow at ${location.site_number} - ${location.name} is not available`);
                    return;
                  }
                  
                  const flowStr = flow.toFixed(0);
                  location.flow = flow;
                  console.log(`Predicted traffic flow at ${location.site_number} - ${location.name} is ${flowStr} at 12:00`);

                }
              }}
            >
              <Popup>
                {location.site_number} - {location.name}
              </Popup>
            </Marker>
        ))}

        <Polyline positions={flippedRoadSegements} pathOptions={{color: "blue"}} />    

        {flippedRoadSegements.flat().map(([lat, lng], index) => (
        <Marker key={index} position={[lat, lng]} icon={dotIcon}>
          <Popup>
            Lat: {lat}, Lng: {lng}
          </Popup>
        </Marker>
      ))}



        {mapInit && startPoint && endPoint && (
          <MapRouting waypoints={waypoints} />
        )}

      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map;