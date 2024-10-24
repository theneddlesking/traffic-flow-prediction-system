import { useEffect, useState } from "react";
import { FiArrowLeftCircle, FiArrowRightCircle } from "react-icons/fi";
import { Menu, ProSidebar, SidebarContent, SidebarHeader } from "react-pro-sidebar";
import "react-pro-sidebar/dist/css/styles.css";
import "./MapSidebar.css";
import type { Location, Route, RoutingPoint } from './types';

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
    model: string;
    routes: Route[];
    route : Route | null;
    setRoute: (route: Route | null) => void;
};

function MapSidebar({ startPoint, endPoint, setStartPoint, setEndPoint, timeOfDay, setTimeOfDay, setModel, model, allModels, locations, hoursTaken, loading, setRoute, routes, route }: MapSidebarProps) {
    const [inputValues, setInputValues] = useState({ start: '', end: '' });
    const [menuCollapse, setMenuCollapse] = useState(false);

    const menuIconClick = () => {
        setMenuCollapse(prev => !prev);
    };

    useEffect(() => {
        if (startPoint) {
            setInputValues(prev => ({ ...prev, start: startPoint.name }));
        }
        if (endPoint) {
            setInputValues(prev => ({ ...prev, end: endPoint.name }));
        }
    }, [startPoint, endPoint]);

    const handleInputChange = (field: 'start' | 'end', value: string) => {
        setInputValues(prev => ({ ...prev, [field]: value }));

        const location = locations.find(location => location.name === value);
        if (field === 'start') {
            setStartPoint(location || null);
        } else {
            setEndPoint(location || null);
        }
    };

    const getTimeStringFromHours = (hoursTaken: number) => {
        const inMinutes = parseInt((hoursTaken * 60).toFixed(0));
        const minutes = inMinutes % 60;
        const hours = Math.floor(inMinutes / 60);
        return `${hours} ${hours === 1 ? "hr" : "hrs"} ${minutes}min`;
    };

    const getRouteStr = (index: number) => {
        return "Route " + (index + 1).toString();
    }

    return (
        <div id="header">
            <ProSidebar collapsed={menuCollapse}>
                <SidebarHeader>
                    <div className="logotext">
                        {menuCollapse ? <p>Map</p> : <p>Map Navigation</p>}
                    </div>
                    <div className="closemenu" onClick={menuIconClick}>
                        {menuCollapse ? <FiArrowRightCircle /> : <FiArrowLeftCircle />}
                    </div>
                </SidebarHeader>
                <SidebarContent>
                    <Menu>
                        <div className='navigation-container'>
                            <label>Starting Point</label>
                            <input
                                placeholder='Starting Point'
                                type="text"
                                value={inputValues.start}
                                onChange={(e) => handleInputChange('start', e.target.value)}
                                list="locations"
                            />
                            <label>Destination</label>
                            <input
                                placeholder='Destination'
                                type="text"
                                value={inputValues.end}
                                onChange={(e) => handleInputChange('end', e.target.value)}
                                disabled={!inputValues.start}
                                list="locations"
                            />
                            <label>Time Of Day</label>
                            <input
                                type="time"
                                value={timeOfDay}
                                onChange={(e) => setTimeOfDay(e.target.value)}
                            />
                            <label>Model</label>
                            <select value={model} onChange={(e) => setModel(e.target.value)}>
                                {allModels.map(model => (
                                    <option key={model} value={model}>{model}</option>
                                ))}
                            </select>

                            {
                                route && (
                                    <>
                                        <label>Route</label>
                                        <select value={routes.findIndex(r => r === route)} onChange={(e) => {
                                            const int = parseInt(e.target.value);
                                            setRoute(routes[int]);
                                        }}>
                                            {routes.map((_, index) => (
                                                <option key={index} value={index}>{getRouteStr(index)}</option>
                                            ))}
                                        </select>   
                                    </>
                                )
                            }
                        
                    
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
                    {startPoint && endPoint && !loading && route && (
                        <Menu>
                            <p className="time">{getTimeStringFromHours(hoursTaken)}</p>
                            <h2>Directions</h2>
                 
                            {route.directions.map((direction) => (
                                <div key={direction.instruction}>
                                    <p className="waypoint">{direction.instruction}</p>
                                </div>
                            ))}
                        </Menu>
                    )}
                </SidebarContent>
            </ProSidebar>
        </div>
    );
}

export default MapSidebar;