import L from "leaflet";

export class CustomRouter implements L.Routing.IRouter {
  // <L.Routing.Waypoint[]> waypoints, <Function> callback, <Object> context?), <RoutingOptions> options

  route(
    waypoints: L.Routing.Waypoint[],
    callback: (error?: L.Routing.IError, routes?: L.Routing.IRoute[]) => void,
    context?: object | undefined,
    options?: L.Routing.RoutingOptions | undefined
  ) {
    console.log("route");
    console.log(waypoints);
    console.log(callback);
    console.log(context);
    console.log(options);

    const route: L.Routing.IRoute = {
      name: "Route",
      coordinates: waypoints.map((waypoint) => waypoint.latLng),
      instructions: [
        {
          distance: 100,
          time: 100,
          type: "Straight",
          road: "Road",
          direction: "Direction",
        },
      ],
      summary: {
        totalDistance: 100,
        totalTime: 100,
      },
    };

    callback(undefined, [route]);

    return this;
  }
}
