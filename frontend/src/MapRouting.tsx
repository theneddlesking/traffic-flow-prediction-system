import L from "leaflet";
import "leaflet-routing-machine";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

function MapRouting() {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    const routingControl = L.Routing.control({
      waypoints: [
        // L.latLng(16.506, 80.648),
        // L.latLng(17.384, 78.4866),
        // L.latLng(12.971, 77.5945)
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
      fitSelectedRoutes: false,
      showAlternatives: false

 
    }).addTo(map);

    return () => {
      map.removeControl(routingControl);
    };
  }, [map]);

  return null;
};

export default MapRouting;