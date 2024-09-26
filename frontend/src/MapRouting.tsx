import L from "leaflet";
import "leaflet-routing-machine";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

import type { Location } from "./types";


type MapRoutingProps = {
  waypoints: Location[];
};

function MapRouting({ waypoints }: MapRoutingProps) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    const routingControl = L.Routing.control({
      waypoints: waypoints.map(waypoint => L.latLng(waypoint.lat, waypoint.long)),
      lineOptions: {
        styles: [
          {
            color: "blue",
            opacity: 0.6,
            weight: 4
          }
        ],
        extendToWaypoints: true,
        missingRouteTolerance: 100
      },
      addWaypoints: false,
      fitSelectedRoutes: true,
      showAlternatives: false, 
    }).addTo(map);

    console.log("foo")
    console.log(map)
    console.log(routingControl)

    // try waiting 10 seconds

    setTimeout(() => {
      const unsafeRouter = routingControl as any;

      const routes = unsafeRouter._routes as any[];

      console.log("routes")
      console.log(routes)

      if (routes) {
        const coords = routes[0]

        console.log("coords")
        console.log(coords)
    
      }
    }, 10000)


    


    return () => {
      map.removeControl(routingControl);
    };

    

  }, [map, waypoints]);

  return null;
}

export default MapRouting;