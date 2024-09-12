import 'leaflet/dist/leaflet.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import {Icon} from 'leaflet';
import './App.css';
import MapRouting from './MapRouting';
import NavigationMenu from './NavigationMenu';

type Location = {
  site_number: number;
  name: string;
  lat: number;
  long: number;
};

function Map() {

  const [mapInit, setMapInit] = useState(false);
  const [locations, setLocations] = useState<Location[]>([]);

  useEffect(() => {
    axios.get<{ locations: Location[] }>('http://127.0.0.1:8000/site/locations')
      .then(locations => {
        setLocations(locations.data.locations);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  const dotIcon = new Icon({
    iconUrl: 'https://img.icons8.com/?size=100&id=24801&format=png&color=000000',
    iconSize: [15, 15]
  });

  const saveMap = (map: unknown) => {
    if (map) {
      setMapInit(true);
    }
  };

  return (
    <div className='map-container'>
      <NavigationMenu />

      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true} ref={saveMap}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          />
        {locations.map(location => (
          <Marker key={location.site_number} position={[location.lat, location.long]} icon={dotIcon}>
            <Popup>
              {location.site_number} - {location.name}
            </Popup>
          </Marker>
        ))}
        
        {mapInit && <MapRouting />}
      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map
