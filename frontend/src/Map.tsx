import 'leaflet/dist/leaflet.css';
import { useState } from 'react';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import './App.css';
import MapRouting from './MapRouting';

function Map() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const [mapInit, setMapInit] = useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  const saveMap = (map: unknown) => {
    if (map) {
      setMapInit(true);
    }
  };

  const lightTileLayer = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
  const darkTileLayer = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

  return (
    <div className='map-container'>
      <h1>Test Leaflet Map</h1>
      <button onClick={toggleDarkMode} style={{ margin: '10px', padding: '10px' }}>
        Toggle to {isDarkMode ? 'Light' : 'Dark'} Mode
      </button>

      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true} ref={saveMap}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={isDarkMode ? darkTileLayer : lightTileLayer}
          />
        <Marker position={[-37.79477,145.03077]}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
        
        {mapInit && <MapRouting />}
      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map
