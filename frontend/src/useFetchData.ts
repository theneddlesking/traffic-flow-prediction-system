import axios from "axios";
import { useEffect, useState } from "react";
import type { Connection, Intersection, Location } from "./types";

const useFetchData = (
  setError: (error: string | null) => void,
  skipLoadingScreen: boolean
) => {
  const [locations, setLocations] = useState<Location[]>([]);
  const [intersections, setIntersections] = useState<Intersection[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [allModels, setAllModels] = useState<string[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      // first wait for the server to be fully loaded

      if (!skipLoadingScreen) {
        await new Promise((resolve) => setTimeout(resolve, 5000));
      }

      try {
        const locationResponse = await axios.get<{ locations: Location[] }>(
          "http://127.0.0.1:8000/site/locations"
        );
        setLocations(locationResponse.data.locations);

        const intersectionResponse = await axios.get<{
          intersections: Intersection[];
        }>("http://127.0.0.1:8000/site/intersections");
        setIntersections(intersectionResponse.data.intersections);

        const connectionResponse = await axios.get<{
          connections: Connection[];
        }>("http://127.0.0.1:8000/site/connections");
        setConnections(connectionResponse.data.connections);

        const modelResponse = await axios.get<{ models: string[] }>(
          "http://127.0.0.1:8000/site/models"
        );
        setAllModels(modelResponse.data.models);
      } catch (err) {
        console.error("There was an error fetching the data!", err);
        setError(`There was an error fetching data - ${err}`);
      }
    };

    fetchData();
  }, [setError]);

  return { locations, intersections, connections, allModels };
};

export default useFetchData;
