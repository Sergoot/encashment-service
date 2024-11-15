import {useEffect, useState} from 'react';
import {MapContainer, TileLayer, Polyline, useMap, Marker, Popup} from 'react-leaflet';
import "leaflet/dist/leaflet.css";
import polyline from '@mapbox/polyline';
import {latLng} from "leaflet";
import CustomMarker from "@/components/custom_ui/CustomMarker/CustomMarker.tsx";
import {getAtmIndex} from "@/components/RouteMap/helpers.ts";

const INIT_CENTER: [number, number] = [55.7558, 37.6173];

export type RouteCoords = number[] | null;

const SetViewOnChange = ({coords}: { coords: [number, number][] | null }) => {
  const map = useMap();
  useEffect(() => {
    const center = coords && coords.length > 0 ? coords[0] : INIT_CENTER;
    map.setView(latLng(center[0], center[1]), 13);
  }, [coords, map]);

  return null;
};

const RouteMap = ({coords, teamId}: { coords: number[], teamId: number | null }) => {
  const [routeCoords, setRouteCoords] = useState<[number, number][] | null>(null);
  const [nodesCoords, setNodesCoords] = useState<[number, number][]>([]);

  const fetchNodeCoordinates = async (nodeId: number): Promise<[number, number] | null> => {
    try {
      const response = await fetch(`https://api.openstreetmap.org/api/0.6/node/${nodeId}`);
      if (!response.ok) throw new Error(`Failed to fetch node ${nodeId}`);
      const text = await response.text();
      const parser = new DOMParser();
      const xml = parser.parseFromString(text, "application/xml");
      const node = xml.querySelector("node");
      if (!node) throw new Error(`Node ${nodeId} not found`);
      const lat = parseFloat(node.getAttribute("lat")!);
      const lon = parseFloat(node.getAttribute("lon")!);
      return [lat, lon];
    } catch (error) {
      console.error(`Error fetching coordinates for node ${nodeId}:`, error);
      return null;
    }
  };

  useEffect(() => {
    const fetchNodes = async () => {
      if (!coords || coords.length === 0) {
        setNodesCoords([]);
        return;
      }

      const results = await Promise.all(coords.map(fetchNodeCoordinates));
      const validCoords = results.filter((coord): coord is [number, number] => coord !== null);
      setNodesCoords(validCoords);
    };

    fetchNodes();
  }, [coords]);

  useEffect(() => {
    const fetchRoute = async () => {
      if (!nodesCoords || nodesCoords.length < 2) {
        setRouteCoords(null); // Сбрасываем маршрут, если недостаточно точек
        return;
      }

      const waypoints = nodesCoords.map(([lat, lng]) => `${lng},${lat}`).join(';');
      try {
        const response = await fetch(
            `http://router.project-osrm.org/route/v1/driving/${waypoints}?overview=full&alternatives=false&steps=true&annotations=false`
        );

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching route: ${errorText}`);
        }

        const data = await response.json();
        if (data.routes.length > 0) {
          const decodedCoords = polyline.decode(data.routes[0].geometry);
          const formattedCoords = decodedCoords.map(([lat, lng]) => [lat, lng]);
          setRouteCoords(formattedCoords as [number, number][]);
        } else {
          console.error("No routes found");
          setRouteCoords(null);
        }
      } catch (error) {
        console.error(error);
        setRouteCoords(null);
      }
    };

    fetchRoute();
  }, [nodesCoords]);

  const center =
      routeCoords && routeCoords.length > 0
          ? routeCoords[0]
          : nodesCoords.length > 0
              ? nodesCoords[0]
              : INIT_CENTER;

  const gradient = [
    [0.9, "blue"],
    [0.9, "green"],
    [0.9, "red"]
  ];

  return (
      <div className="w-full h-[42rem] z-0">
        <MapContainer
            center={center}
            zoom={13}
            style={{height: "100%", width: "100%"}}
            className="rounded-lg shadow-lg"
        >
          <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
          />
          <SetViewOnChange coords={routeCoords || [center]}/>
          {routeCoords && (
              // <Polyline
              //     positions={routeCoords}
              //     gradient={gradient}
              //     color={"#242424"}
              //     weight={6}          // Толщина линии
              //     opacity={0.8}       // Прозрачность линии
              //     dashArray="10,10"
              // />
              <>
                {/* Обводка (контур) */}
                <Polyline
                    positions={routeCoords}
                    color={"#f1f1f1aa"}        // Цвет обводки
                    weight={8}           // Толщина обводки
                    opacity={0.8}        // Прозрачность обводки
                    lineCap="round"
                    lineJoin="round"
                />
                {/* Основная линия */}
                <Polyline
                    positions={routeCoords}
                    gradient={gradient}
                    color={"#242424"}
                    weight={4}           // Толщина основной линии
                    opacity={0.7}        // Прозрачность основной линии
                    lineCap="round"
                    lineJoin="round"
                    dashArray="10,8"
                />
              </>
          )}

          {nodesCoords.map((coord, index) => {
            const pointIndex = getAtmIndex(teamId, coords[index]);
            if (index === 0) {
              return (<CustomMarker key={index} coord={coord} index={pointIndex} type={"current"}/>)
            }
            return (<CustomMarker key={index} coord={coord} index={pointIndex} type={"destination"}/>)
          })}
        </MapContainer>
      </div>
  );
};

export default RouteMap;
