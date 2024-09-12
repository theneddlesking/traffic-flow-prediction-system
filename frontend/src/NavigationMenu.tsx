import { useState } from 'react';
import './App.css';

import type { Location } from './types';

type NavigationMenuProps = {
  setStartPoint: (coordinates: Location) => void;
  setEndPoint: (coordinates: Location) => void;
  locations: Location[];
};

function NavigationMenu({ setStartPoint, setEndPoint, locations }: NavigationMenuProps) {
  const [startInput, setStartInput] = useState('');
  const [endInput, setEndInput] = useState('');

  const handleRouting = () => {
    // get name and coordinates from startInput
    const startLocation = locations.find(location => location.name === startInput);

    if (!startLocation) {
      alert('Starting point not found');
      return;
    }
    
    const endLocation = locations.find(location => location.name === endInput);

    if (!endLocation) {
      alert('Destination not found');
      return;
    }

    setStartPoint(startLocation);
    setEndPoint(endLocation);
  };

  return (
    <>
      <div className='navigation-container'>
        <input
          placeholder='Starting Point'
          type="text"
          id="start"
          value={startInput}
          onChange={(e) => setStartInput(e.target.value)}
          list="locations"
        />
        <input
          placeholder='Destination'
          type="text"
          id="end"
          value={endInput}
          onChange={(e) => setEndInput(e.target.value)}
          list="locations"
        />
        <button onClick={handleRouting}>Find Route</button>
      </div>

    
      <datalist id="locations">
        {locations.map(location => (
          <option key={location.location_id} value={location.name} />
        ))}
      </datalist>
    </>
  );
};

export default NavigationMenu;