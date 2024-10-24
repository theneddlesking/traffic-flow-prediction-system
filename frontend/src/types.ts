export type Direction = "N" | "S" | "E" | "W" | "NE" | "NW" | "SE" | "SW";

export type Location = {
  location_id: number;
  site_number: number;
  name: string;
  lat: number;
  long: number;
  flow: number | null;
};

export type RoutingPoint = {
  location_id: number;
  site_number: number;
  lat: number;
  long: number;
  street_name: string;
  other_street_name: string;
  direction: {
    value: Direction;
  };
  street_names: string[];
};

export type Intersection = {
  street_names: string[];
  points: RoutingPoint[];
  lat: number;
  long: number;
};

export type Connection = {
  intersection: Intersection;
  other_intersection: Intersection;
  along_street: string;
  speed_limit: Direction;
  direction: string;
  length: number;
};

export type RouteDirection = {
  instruction: string;
  distance: number;
  is_straight: boolean;
};

export type Route = {
  waypoints: RoutingPoint[];
  hours_taken: number;
  directions: RouteDirection[];
};
