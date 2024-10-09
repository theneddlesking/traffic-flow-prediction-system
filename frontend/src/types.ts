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
    value: string;
  };
  street_names: string[];
};

export type Intersection = {
  street_names: string[];
  points: RoutingPoint[];
  lat: number;
  long: number;
};
