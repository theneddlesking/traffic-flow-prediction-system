import './App.css'
import { useState } from 'react';

function NavigationMenu() {
  const [startPoint, setStartPoint] = useState('');
  const [endPoint, setEndPoint] = useState('');

  const handleRouting = () => {
    console.log(`Start Point: ${startPoint}, End Point: ${endPoint}`);
  };

  return (
    <div className='navigation-container'>
      <input
        placeholder='Starting Point'
        type="text"
        id="start"
        value={startPoint}
        onChange={(e) => setStartPoint(e.target.value)}
      />
      <input
        placeholder='Destination'
        type="text"
        id="end"
        value={endPoint}
        onChange={(e) => setEndPoint(e.target.value)}
      />
      <button onClick={handleRouting}>Find Route</button>
    </div>
  );
};

export default NavigationMenu
