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
      showAlternatives: false
    }).addTo(map);

    return () => {
      map.removeControl(routingControl);
    };
  }, [map, waypoints]);

  return null;
}

export default MapRouting;