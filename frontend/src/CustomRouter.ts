import L, { Routing } from "leaflet";
import "leaflet-routing-machine";

type GeometryType = "LineString" | "Point" | "Polygon" | "MultiLineString";

type InstructionType =
  | "Straight"
  | "SlightRight"
  | "Right"
  | "SharpRight"
  | "TurnAround"
  | "SharpLeft"
  | "Left"
  | "SlightLeft"
  | "WaypointReached"
  | "Roundabout"
  | "StartAt"
  | "DestinationReached"
  | "EnterAgainstAllowedDirection"
  | "LeaveAgainstAllowedDirection";

type CustomInstruction = {
  text: string;
  type: InstructionType;
  distance: number;
  time: number;
};

type CustomRouteAPIResponse = {
  name: string;
  geometry: {
    type: GeometryType;
    coordinates: number[][];
  };
  distance: number;
  duration: number;
  instructions: CustomInstruction[];
};

// type RoutingCallback = (
//   error: Error | null,
//   routes: L.Routing.IRoute[] | null
// ) => void;

export class CustomRouter implements L.Routing.IRouter {
  route(
    waypoints: L.Routing.Waypoint[],
    callback: (err?: L.Routing.IError, routes?: L.Routing.IRoute[]) => void,

    // context is the map instance
    context: unknown,
    options: Routing.RoutingOptions
  ): void {
    console.log("chat im routing");
    console.log(waypoints);
    const start = waypoints[0];
    const end = waypoints[waypoints.length - 1];

    // rebind callback to the context of the map instance

    console.log(callback + "");

    callback = callback.bind(context);

    console.log(options);

    // Simulate an API call to your custom routing service
    this.fetchRouteFromAPI(start, end)
      .then((routeData: CustomRouteAPIResponse) => {
        const route = this.convertToLeafletFormat(routeData);
        callback(undefined, [route]);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  convertToLeafletFormat(routeData: CustomRouteAPIResponse): L.Routing.IRoute {
    const coordinates = routeData.geometry.coordinates.map(
      (coord) => new L.LatLng(coord[1], coord[0])
    );

    return {
      name: routeData.name,
      coordinates: coordinates,
      instructions: routeData.instructions.map(
        (customInstruction: CustomInstruction) => ({
          text: customInstruction.text,
          // we can actually pull this
          type: customInstruction.type,
          distance: routeData.distance / routeData.instructions.length,
          time: routeData.duration / routeData.instructions.length,
        })
      ),
      summary: {
        totalDistance: routeData.distance,
        totalTime: routeData.duration,
      },
    };
  }

  async fetchRouteFromAPI(
    start: L.Routing.Waypoint,
    end: L.Routing.Waypoint
  ): Promise<CustomRouteAPIResponse> {
    // simulated delay

    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          name: "Custom Route",
          geometry: {
            type: "LineString",
            coordinates: [
              [start.latLng.lng, start.latLng.lat],
              [end.latLng.lng, end.latLng.lat],
            ],
          },
          distance: 1200, // in meters
          duration: 600, // in seconds
          instructions: [
            {
              text: "Go straight",
              type: "Straight",
              distance: 600,
              time: 300,
            },
          ],
        });
      }, 1000);
    });
  }
}
