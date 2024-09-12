import L from "leaflet";
import "leaflet-routing-machine";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

import type { Location } from "./types";

type MapRoutingProps = {
  startPoint: Location
  endPoint: Location
};

function MapRouting({ startPoint, endPoint }: MapRoutingProps) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    const routingControl = L.Routing.control({
      waypoints: [
        L.latLng(startPoint.lat, startPoint.long),
        L.latLng(endPoint.lat, endPoint.long)   
      ],
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
  }, [map, startPoint, endPoint]);

  return null;
}

export default MapRouting;