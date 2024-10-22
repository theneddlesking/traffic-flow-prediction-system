import axios from 'axios';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import './App.css';
import MapSidebar from './MapSidebar';
import type { Location, Route, RoutingPoint } from './types';
import useFetchData from './useFetchData';

type RoutingResponse = {
  routes: Route[];
  error?: string;
};

function Map() {
  const [startPoint, setStartPoint] = useState<Location | null>(null);
  const [endPoint, setEndPoint] = useState<Location | null>(null);
  const [waypoints, setWaypoints] = useState<RoutingPoint[]>([]);
  const [routes, setRoutes] = useState<Route[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [timeOfDay, setTimeOfDay] = useState('12:00');
  const [model, setModel] = useState('');
  const [hoursTaken, setHoursTaken] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const {
    locations,
    intersections,
    connections,
    allModels
  } = useFetchData(setError); 

  const options = {
    showConnections : false,
    showIntersections : false,
    showLocations : true,
    showRoutes : true
  }

  const generateRoute = async (routeStartPoint: Location, routeEndPoint: Location) => {
    setLoading(true);
    try {
      const res = await axios.get<RoutingResponse>(`http://localhost:8000/routing/route?start_location_id=${routeStartPoint.location_id}&end_location_id=${routeEndPoint.location_id}&time_of_day=${timeOfDay}&model_name=${model}`);
      if (res.data.error) throw new Error(res.data.error);
      const bestRoute = res.data.routes[0];
      setWaypoints(bestRoute.waypoints);
      setHoursTaken(bestRoute.hours_taken);
      setRoutes(res.data.routes);
    } catch (error) {
      const typedError = error as Error

      console.error(typedError);

      setError(`Error fetching route: ${typedError.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (allModels.length > 0) {
      setModel(allModels[0]); 
    }
  }, [allModels]);

  const setStartPointAndFetchTraffic = (location: Location | null) => {
    setStartPoint(location);
    if (location && endPoint) generateRoute(location, endPoint);
  };

  const setEndPointAndFetchTraffic = (location: Location | null) => {
    setEndPoint(location);
    if (location && startPoint) generateRoute(startPoint, location);
  };

  const dotIcon = new Icon({
    iconUrl: 'https://img.icons8.com/?size=100&id=24801&format=png&color=000000',
    iconSize: [15, 15],
  });

  const getRouteColour = (index: number) => {
    // blue, red, green, yellow, pink, cyan
    const colours = ['blue', 'red', 'green','yellow', 'pink', 'cyan'];
    return colours[index % colours.length
    ];
  }

  return (
    <div className='map-container'>
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button className="close-button" onClick={() => setError(null)}>&times;</button>
        </div>
      )}

      <MapSidebar
        startPoint={startPoint}
        endPoint={endPoint}
        setStartPoint={setStartPointAndFetchTraffic}
        setEndPoint={setEndPointAndFetchTraffic}
        timeOfDay={timeOfDay}
        setTimeOfDay={setTimeOfDay}
        setModel={setModel}
        allModels={allModels}
        locations={locations}
        hoursTaken={hoursTaken || 0}
        waypoints={waypoints}
        loading={loading}
        model={model}
      />

      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        />

        {/* render locations */}
        {options.showLocations && locations.map((location, index) => (
          <Marker key={index} position={[location.lat, location.long]} icon={dotIcon}>
            <Popup>
              <strong>{location.site_number}</strong> - {location.name}
              <br />
              <button onClick={() => setStartPointAndFetchTraffic(location)}>Set Start Point</button>
              <button onClick={() => setEndPointAndFetchTraffic(location)}>Set Destination</button>
            </Popup>
          </Marker>
        ))}

        {/* render intersections */}
        {options.showIntersections && intersections.map((intersection, index) => (
          <Marker key={index} position={[intersection.lat, intersection.long]} icon={dotIcon} />
        ))}

        {/* render connections */}
        {options.showConnections && connections.map((connection, index) => (
          <Polyline key={index} positions={[[connection.intersection.lat, connection.intersection.long], [connection.other_intersection.lat, connection.other_intersection.long]]} pathOptions={{ color: '#f0bab4' }} />
        ))}

        {/* draw routes */}
        {options.showRoutes && routes.map((route, index) => (
          <Polyline key={index} positions={route.waypoints.map(w => [w.lat, w.long])} pathOptions={{ color: getRouteColour(index) }} />
        ))}
      </MapContainer>

      <div className='padding-div' />
    </div>
  );
}

export default Map;