import './App.css';

import type { Location } from './types';

type NavigationMenuProps = {
  startPoint: Location | null;
  endPoint: Location | null;
  setStartPoint: (coordinates: Location | null) => void;
  setEndPoint: (coordinates: Location | null) => void;
  locations: Location[];
};

function NavigationMenu({ startPoint, endPoint, setStartPoint, setEndPoint, locations }: NavigationMenuProps) {

  const validateStartInput = (input: string) => {
    if (input === '') {
      setStartPoint(null);
      return;
    }
    const location = locations.find(location => location.name === input);
    if (location != null) {
      setStartPoint(location);
    }
  };

  const validateEndInput = (input: string) => {
    if (input === '') {
      setEndPoint(null);
      return;
    }
    const location = locations.find(location => location.name === input);
    if (location != null) {
      setEndPoint(location);
    }
  };

  return (
    <>
      <div className='navigation-container'>
        <input
          placeholder='Starting Point'
          type="text"
          id="start"
          onClick={(e) => e.currentTarget.select()}
          onChange={(e) => validateStartInput(e.target.value)}
          list="locations"
        />
        <input
          placeholder='Destination'
          type="text"
          id="end"
          onClick={(e) => e.currentTarget.select()}
          onChange={(e) => validateEndInput(e.target.value)}
          list="locations"
        />
        {/* TODO: Make this button actually dispatch to MapRouting */}
        <button>Find Route</button>
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