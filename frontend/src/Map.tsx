import axios from 'axios';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import './App.css';

import MapSidebar from './MapSidebar';
import type { Connection, Intersection, Location } from './types';


type RoutingResponse = {
  waypoints: Location[];
  hours_taken: number;
  error?: string;
}

type IntersectionResponse = {
  "intersections" : Intersection[];
};

type ConnectionResponse = {
  "connections": Connection[];
};

function Map() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [startPoint, setStartPoint] = useState<Location | null>(null);
  const [endPoint, setEndPoint] = useState<Location | null>(null);
  const [waypoints, setWaypoints] = useState<Location[]>([]);
  const [intersections, setIntersections] = useState<Intersection[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);

  const [error, setError] = useState<string | null>(null);

  const SHOW_INTERSECTIONS = false;
  const SHOW_CONNECTIONS = false;


  const [timeOfDay, setTimeOfDay] = useState('12:00');


  const generateRoute = async (possibleEndPoint?: Location) => {

    const routeEndPoint = possibleEndPoint || endPoint;

    // fetch route from backend
    const res = await axios.get<RoutingResponse>(`http://localhost:8000/routing/route?start_location_id=${startPoint?.location_id}&end_location_id=${routeEndPoint?.location_id}&time_of_day=${timeOfDay}`)

    // handle error
    if (res.data.error) {
      console.error(res.data.error);
      setError(`There was an error fetching the route between ${startPoint?.location_id} and ${routeEndPoint?.location_id} - ${res.data.error}`);
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

        console.log("original locations");
        console.log(locations.data.locations);

        // for some reason the long lat is slightly off
        locations.data.locations.forEach(location => {
          location.lat += latOffset;
          location.long += longOffset;
        });

        setLocations(locations.data.locations);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setError(`There was an error fetching location data - ${error}`);
      });
  }, []);

  useEffect(() => {
    axios.get<IntersectionResponse>('http://127.0.0.1:8000/site/intersections')
      .then(intersections => {

        const intersectionsArray = intersections.data.intersections;

        intersectionsArray.forEach(intersection => {
          return remapIntersection(intersection);
        });

        console.log("intersections");
        console.log(intersectionsArray);

        setIntersections(intersectionsArray);
      }
      )
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setError(`There was an error fetching intersection data - ${error}`);
      });
    }, []);

  function remapIntersection(intersection: Intersection) {
    const latOffset = 0.00151;
    const longOffset = 0.0013;

    intersection.lat += latOffset;
    intersection.long += longOffset;

    intersection.points.forEach(point => {
      point.lat += latOffset;
      point.long += longOffset;
    });

    return intersection
  }

  useEffect(() => {
    axios.get<ConnectionResponse>('http://127.0.0.1:8000/site/connections')
      .then(connections => {

        const connectionsArr = connections.data.connections;

        connectionsArr.forEach(connection => {
          connection.intersection = remapIntersection(connection.intersection);
          connection.other_intersection = remapIntersection(connection.other_intersection);
        });

        setConnections(connectionsArr);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setError(`There was an error fetching connection data - ${error}`);
      });
  }, []);

  const getFlow = async (location: Location) => {
        console.error('There was an error fetching the data!', error);
    return await axios.get<{ flow: number }>(`http://127.0.0.1:8000/site/flow?location_id=${location.location_id}&time=${timeOfDay}`)
      .then(flow => {
        return flow.data.flow;
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setError(`There was an error fetching the traffic flow for ${location.name} - ${error}`);
      });
  }

  const dotIcon = new Icon({
    iconUrl: 'https://img.icons8.com/?size=100&id=24801&format=png&color=000000',
    iconSize: [15, 15]
  });

  const intersectionIcon = new Icon({
    iconUrl: 'https://img.icons8.com/?size=100&id=24801&format=png&color=ab5543',
    iconSize: [15, 15]
  });


  const setStartPointAndFetchTraffic = async (location: Location | null) => {
    setStartPoint(location);

    if (location !== null) {
      const flow = await getFlow(location);
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
      const flow = await getFlow(location);
      if (flow !== undefined) {
        location.flow = flow;
      }

      if (startPoint !== null) {
        generateRoute();
      }
    }
  };

  function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  const waypointCoordinates = getLineSegments(waypoints);

  function getLineSegments(waypoints: Location[]) {
    const segments = [];

    console.log('waypoints');
    console.log(waypoints);

    for (let i = 0; i < waypoints.length - 1; i++) {
      const start = waypoints[i];
      const end = waypoints[i + 1];

      segments.push([[start.lat, start.long], [end.lat, end.long]]);
    }

    console.log('segments');
    console.log(segments);

    return segments;
  }

  return (
    <div className='map-container'>
      {error && <div className="error-banner">{error}</div>}

      <MapSidebar startPoint={startPoint} endPoint={endPoint} setStartPoint={setStartPointAndFetchTraffic} setEndPoint={setEndPointAndFetchTraffic} locations={locations} />

      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          />

        {/* locations */}
        {locations.map(location => (
            <Marker key={location.location_id} position={[location.lat, location.long]} icon={dotIcon}
              eventHandlers={{
                mouseover: (e) => {
                  const marker = e.target;
                  marker.openPopup();
                }
              }}
            >
              <Popup>
                <div>
                  <strong>{location.site_number}</strong> - {location.name}
                  <br />
                  <button onClick={() => {
                    setStartPointAndFetchTraffic(location);
                  }}>Set Start Point</button>
                  <button onClick={() => {
                    setEndPointAndFetchTraffic(location);
                  }}>Set Destination</button>
                </div>
              </Popup>
            </Marker>
        ))}

        {/* intersections */}
        {SHOW_INTERSECTIONS && intersections.map(intersection => (
          <Marker key={intersection.lat + intersection.long} position={[intersection.lat, intersection.long]} icon={intersectionIcon} />
        ))}

        {/* connections */}
        {SHOW_CONNECTIONS && connections.map(connection => (
          <Polyline key={connection.intersection.lat + connection.other_intersection.lat} positions={[[connection.intersection.lat, connection.intersection.long], [connection.other_intersection.lat, connection.other_intersection.long]]} pathOptions={{color: '#f0bab4'}} />
        ))}

      {/* draws the route */}
      {/* <Polyline positions={waypointCoordinates} pathOptions={{color: getRandomColor() }} />     */}
      {
        waypointCoordinates.map((segment, index) => (
          <Polyline key={index} positions={segment} pathOptions={{color: getRandomColor() }} />
        ))
      }



      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map;