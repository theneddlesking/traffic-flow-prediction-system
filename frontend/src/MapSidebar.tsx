import { useEffect, useState } from "react";

import type { Location, RoutingPoint } from './types';

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
  setModel: (model: string) => void;
  allModels: string[];
  locations: Location[];
  hoursTaken: number;
  waypoints: RoutingPoint[];
  loading: boolean;
};


function MapSidebar({ startPoint, endPoint, setStartPoint, setEndPoint, timeOfDay, setTimeOfDay, setModel, allModels, locations, hoursTaken, waypoints, loading }: MapSidebarProps) {
  const [startPointInput, setStartPointInput] = useState('');
  const [endPointInput, setEndPointInput] = useState('');

  const [menuCollapse, setMenuCollapse] = useState(false);
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
    
    const inMinutes = parseInt((hoursTaken * 60).toFixed(0));

    // eg. 73
    // 73 % 60 = 13

    const minutes = inMinutes % 60;

    // (73 - 13) / 60 = 1

    const hours = (inMinutes - minutes) / 60


    const hourStr = hours == 1 ? "hr" : "hrs";

    // eg. 1hr 5min

    return `${hours}${hourStr} ${minutes}min`;
  }

  // filter to only have one per scat site
  const waypointsPerScat = waypoints.filter((waypoint, index, self) =>
    index === self.findIndex((t) => (
      t.site_number === waypoint.site_number
    ))
  );

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
                <label>Starting Point</label>
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
                <label>Destination</label>
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
                <label>Time Of Day</label>
                <input
                  type="time"
                  id="timeOfDay"
                  value={timeOfDay}
                  onChange={(e) => setTimeOfDay(e.target.value)}
                />
                <label>Model</label>
                <select>
                  {allModels && allModels.map(model => (
                    <option key={model} value={model} onChange={() => setModel(model)}>{model}</option>
                  ))}
                </select>
              </div>
              <datalist id="locations">
                {locations.map(location => (
                <option key={location.location_id} value={location.name} />
                ))}
              </datalist>
            </Menu>
            {loading && (
              <div className="spinner-container">
                <div className="spinner"></div>
              </div>
            )}
            {startPoint && endPoint && !loading && (
              <Menu>
                <p className="time">{getTimeStringFromHours(hoursTaken)}</p>

                <h2>Directions</h2>

                {/* render waypoints */}
                {waypointsPerScat.map(waypoint => (
                  <div key={waypoint.location_id}>
                    <p className="waypoint">{waypoint.site_number} - {waypoint.street_name} / {waypoint.other_street_name}</p>
                    {/* vertical line */}
                    {
                      waypointsPerScat[waypointsPerScat.length - 1] !== waypoint &&
                      <div className="vertical-line">|</div>
                    }
                  </div>
                ))}

              </Menu>
            )}
          </SidebarContent>
        </ProSidebar>
      </div>
    </>
  );
};

export default MapSidebar;
