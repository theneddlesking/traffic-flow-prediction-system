import axios from 'axios';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import './App.css';
import MapRouting from './MapRouting';

import MapSidebar from './MapSidebar';
import type { Location } from './types';


function Map() {
  const [mapInit, setMapInit] = useState(false);
  const [locations, setLocations] = useState<Location[]>([]);
  const [startPoint, setStartPoint] = useState<Location | null>(null);
  const [endPoint, setEndPoint] = useState<Location | null>(null);

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
    return await axios.get<{ flow: number }>(`http://127.0.0.1:8000/site/flow?location_id=${location_id}&time=12:00`)
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
    }
  };

  const setEndPointAndFetchTraffic = async (location: Location | null) => {
    setEndPoint(location);

    if (location !== null) {
      const flow = await getFlow(location.location_id);
      if (flow !== undefined) {
        location.flow = flow;
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
                  } else if (endPoint === null) {
                    setEndPoint(location);
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
        
        {mapInit && startPoint && endPoint && (
          <MapRouting startPoint={startPoint} endPoint={endPoint} />
        )}
      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map;