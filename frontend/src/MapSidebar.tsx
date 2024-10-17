import { useEffect, useState } from "react";

import type { Location } from './types';

import {
  Menu,
  ProSidebar,
  SidebarContent,
  SidebarHeader,
} from "react-pro-sidebar";

import { FiArrowLeftCircle, FiArrowRightCircle } from "react-icons/fi";

import "react-pro-sidebar/dist/css/styles.css";
import "./MapSidebar.css";

type MapSidebarProps = {
  startPoint: Location | null;
  endPoint: Location | null;
  setStartPoint: (coordinates: Location | null) => void;
  setEndPoint: (coordinates: Location | null) => void;
  timeOfDay: string;
  setTimeOfDay: (time: string) => void;
  locations: Location[];
  hoursTaken: number;
};


function MapSidebar({ startPoint, endPoint, setStartPoint, setEndPoint, timeOfDay, setTimeOfDay, locations, hoursTaken }: MapSidebarProps) {
  const [startPointInput, setStartPointInput] = useState('');
  const [endPointInput, setEndPointInput] = useState('');

  const [menuCollapse, setMenuCollapse] = useState(true);
  const menuIconClick = () => {
    return menuCollapse ? setMenuCollapse(false) : setMenuCollapse(true);
  };

  useEffect(() => {
    if (startPoint != null) {
      setStartPointInput(startPoint.name);
    }
    if (endPoint != null) {
      setEndPointInput(endPoint.name);
    }
  }, [startPoint, endPoint]);

  const validateStartInput = (input: string) => {
    setStartPointInput(input);
    const location = locations.find(location => location.name === input);
    if (location != null) {
      setStartPoint(location);
    }
  };

  const validateEndInput = (input: string) => {
    setEndPointInput(input);
    const location = locations.find(location => location.name === input);
    if (location != null) {
      setEndPoint(location);
    }
  };

  const changeStartInput = (input: string) => {
    if (input === '') {
      setStartPointInput('');
      setStartPoint(null);
      return;
    } 

    if (startPoint != null) {
      setStartPointInput(startPoint.name);
    }
  };

  const changeEndInput = (input: string) => {
    if (input === '') {
      setEndPointInput('');
      setEndPoint(null);
      return;
    }

    if (endPoint != null) {
      setEndPointInput(endPoint.name);
    }
  };

  function getTimeStringFromHours(hoursTaken: number) {
    
    const inMinutes = hoursTaken * 60;

    // eg. 73
    // 73 % 60 = 13

    const minutes = inMinutes % 60

    // (73 - 13) / 60 = 1

    const hours = (inMinutes - minutes) / 60


    const hourStr = hours == 1 ? "hr" : "hrs";

    // eg. 1hr 5min

    return `${hours}${hourStr} ${minutes}min`;
  }

  return (
    <>
      <div id="header">
        <ProSidebar collapsed={menuCollapse}>
          <SidebarHeader>
          <div className="logotext">
              {menuCollapse ? ( <p>Map</p> ) : ( <p>Map Navigation</p> )}
            </div>
            <div className="closemenu" onClick={menuIconClick}>
              {menuCollapse ? (
                <FiArrowRightCircle/>
              ) : (
                <FiArrowLeftCircle/>
              )}
            </div>
          </SidebarHeader>
          <SidebarContent>
            <Menu>
              <div className='navigation-container'>
                <input
                  placeholder='Starting Point'
                  type="text"
                  id="start"
                  onClick={(e) => e.currentTarget.select()}
                  onBlur={(e) => changeStartInput(e.target.value)}
                  value={startPointInput}
                  onChange={(e) => validateStartInput(e.target.value)}
                  list="locations"
                />
                <input
                  placeholder='Destination'
                  type="text"
                  id="end"
                  onClick={(e) => e.currentTarget.select()}
                  onBlur={(e) => changeEndInput(e.target.value)}
                  disabled={startPoint == null}
                  value={endPointInput}
                  onChange={(e) => validateEndInput(e.target.value)}
                  list="locations"
                />
                <input
                  type="time"
                  id="timeOfDay"
                  value={timeOfDay}
                  onChange={(e) => setTimeOfDay(e.target.value)}
                />
              </div>
              <datalist id="locations">
                {locations.map(location => (
                <option key={location.location_id} value={location.name} />
                ))}
              </datalist>
            </Menu>
            {startPoint && (
              <Menu>
                <h2>Start Point</h2>
                <p>{startPoint.site_number} - {startPoint.name}</p>
                <p>Latitude: {startPoint.lat}</p>
                <p>Longitude: {startPoint.long}</p>
                <p>Traffic flow at {timeOfDay}: {startPoint.flow}</p>
              </Menu>
            )}
            {endPoint && (
              <Menu>
                <h2>Destination</h2>
                <p>{endPoint.site_number} - {endPoint.name}</p>
                <p>Latitude: {endPoint.lat}</p>
                <p>Longitude: {endPoint.long}</p>
                <p>Traffic flow at {timeOfDay}: {endPoint.flow}</p>
              </Menu>
            )}
            {startPoint && endPoint && (
              <Menu>
                <h2>Route Information</h2>
                <p>Time Taken: {getTimeStringFromHours(hoursTaken)}</p>
              </Menu>
            )}
          </SidebarContent>
        </ProSidebar>
      </div>
    </>
  );
};

export default MapSidebar;
