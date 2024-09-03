import { useEffect, useState } from 'react'
import axios from 'axios';
import './App.css'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState("")
  const [number1, setNumber1] = useState('');
  const [number2, setNumber2] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/hello')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  const handleAddition = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/add', {
        params: {
          a: number1,
          b: number2
        }
      });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error fetching the result:', error);
    }
  };

  return (
    <>
      <h1>Test Leaflet Map</h1>
      <div className='map-container'>
        <MapContainer center={[-37.8095, 145.0351]} zoom={13} scrollWheelZoom={true}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
          <Marker position={[-37.8095, 145.0351]}>
            <Popup>
              A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
          </Marker>
        </MapContainer>
      </div>
    </>
  )
}

export default App
