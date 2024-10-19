import axios from 'axios';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import './App.css';

import MapSidebar from './MapSidebar';
import type { Connection, Intersection, Location, Route, RoutingPoint } from './types';


type RoutingResponse = {
  routes: Route[];
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
  const [waypoints, setWaypoints] = useState<RoutingPoint[]>([]);
  const [intersections, setIntersections] = useState<Intersection[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);

  const [error, setError] = useState<string | null>(null);

  const SHOW_INTERSECTIONS = false;
  const SHOW_CONNECTIONS = false;


  const [timeOfDay, setTimeOfDay] = useState('12:00');

  const [hoursTaken, setHoursTaken] = useState<number | null>(null);

  const generateRoute = async (routeStartPoint: Location, routeEndPoint: Location) => {

    // fetch route from backend
    const res = await axios.get<RoutingResponse>(`http://localhost:8000/routing/route?start_location_id=${routeStartPoint.location_id}&end_location_id=${routeEndPoint.location_id}&time_of_day=${timeOfDay}`)

    // handle error
    if (res.data.error) {
      console.error(res.data.error);
      setError(`There was an error fetching the route between ${routeStartPoint.location_id} and ${routeEndPoint.location_id} - ${res.data.error}`);
      return;
    }

    const bestRoute = res.data.routes[0];

    const routeWaypoints = bestRoute.waypoints;

    const routeHours = bestRoute.hours_taken;

    setWaypoints(routeWaypoints);

    setHoursTaken(routeHours);

    setRoutes(res.data.routes);

    console.log(`Route takes ${routeHours} hours`);
  }

  useEffect(() => {
    axios.get<{ locations: Location[] }>('http://127.0.0.1:8000/site/locations')
      .then(locations => {
        console.log("original locations");
        console.log(locations.data.locations);

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

  useEffect(() => {
    axios.get<ConnectionResponse>('http://127.0.0.1:8000/site/connections')
      .then(connections => {

        const connectionsArr = connections.data.connections;

        console.log("connections");
        console.log(connectionsArr);

        setConnections(connectionsArr);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
        setError(`There was an error fetching connection data - ${error}`);
      });
  }, []);


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

    if (location !== null && endPoint !== null) {
        generateRoute(location, endPoint);
    }
  };

  const setEndPointAndFetchTraffic = async (location: Location | null) => {
    setEndPoint(location);

    if (location !== null && startPoint !== null) {
      generateRoute(startPoint, location);
    }
  };

  function rgbaString(color: string, opacity: number) {
    return `rgba(${parseInt(color.slice(-6,-4), 16)}, ${parseInt(color.slice(-4,-2), 16)}, ${parseInt(color.slice(-2), 16)}, ${opacity})`;
  }

  function getRouteColor(routeIndex: number) {

    const blueHex = '0000FF';

    // lower route index is higher opacity

    const opacity = 1 - (routeIndex / routes.length) * 2;

    return rgbaString(blueHex, opacity);
  }

  function getLineSegments(waypoints: RoutingPoint[]) {
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

      <MapSidebar startPoint={startPoint} endPoint={endPoint} setStartPoint={setStartPointAndFetchTraffic} setEndPoint={setEndPointAndFetchTraffic} timeOfDay={timeOfDay} setTimeOfDay={(time) => setTimeOfDay(time)} locations={locations} hoursTaken={hoursTaken || 0} waypoints={waypoints} />

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

      {/* draws the routes */}
      {/* <Polyline positions={waypointCoordinates} pathOptions={{color: getRandomColor() }} />     */}
      {
        routes.map((route, index) => (
            <Polyline key={index} positions={getLineSegments(route.waypoints) as unknown as L.LatLng[]} pathOptions={{color: getRouteColor(index) }} />
        ))
      }



      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map;