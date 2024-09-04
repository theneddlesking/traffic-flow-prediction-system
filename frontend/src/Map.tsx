import { useState } from 'react';
import './App.css'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';

function Map() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  const lightTileLayer = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
  const darkTileLayer = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

  return (
    <div className='map-container'>
      <h1>Test Leaflet Map</h1>
      <button onClick={toggleDarkMode} style={{ margin: '10px', padding: '10px' }}>
        Toggle to {isDarkMode ? 'Light' : 'Dark'} Mode
      </button>
      <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url={isDarkMode ? darkTileLayer : lightTileLayer}
          />
        <Marker position={[-37.8095, 145.0351]}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>
      <div className='padding-div' />
    </div>
  )
}

export default Map
