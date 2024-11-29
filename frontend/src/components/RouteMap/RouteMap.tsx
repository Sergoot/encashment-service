import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Polyline, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import polyline from "@mapbox/polyline";
import { latLng } from "leaflet";
import CustomMarker from "@/components/custom_ui/CustomMarker/CustomMarker.tsx";
import { getAtmIndex } from "@/components/RouteMap/helpers.ts";

const INIT_CENTER: [number, number] = [55.7558, 37.6173];

const SetViewOnChange = ({ coords }: { coords: [number, number][] | null }) => {
  const map = useMap();
  useEffect(() => {
    const center = coords && coords.length > 0 ? coords[0] : INIT_CENTER;
    map.setView(latLng(center[0], center[1]), 13);
  }, [coords, map]);

  return null;
};

const RouteMap = ({
                    coords,
                    teamId,
                  }: {
  coords: [number, number][] | null; // Массив координат или null
  teamId: number | null;
}) => {
  const [routeCoords, setRouteCoords] = useState<[number, number][] | null>(null);

  useEffect(() => {
    const fetchRoute = async () => {
      if (!coords || coords.length < 2) { // Проверяем, что coords существует и содержит минимум 2 точки
        setRouteCoords(null); // Сбрасываем маршрут
        return;
      }

      // Формируем строку для OSRM API
      const waypoints = coords.map(({lat, lon}) => `${lon},${lat}`).join(";");
      console.log(coords);

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
  }, [coords]);

  const center =
      routeCoords && routeCoords.length > 0
          ? routeCoords[0]
          : coords && coords.length > 0
              ? coords[0]
              : INIT_CENTER;

  return (
      <div className="w-full h-[42rem] z-0">
        <MapContainer
            center={center}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
            className="rounded-lg shadow-lg"
        >
          <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"
          />
          {routeCoords && (
              <>
                <Polyline
                    positions={routeCoords}
                    color={"#242424"}
                    weight={4}
                    opacity={0.7}
                    lineCap="round"
                    lineJoin="round"
                />
              </>
          )}
          {coords &&
              coords.map((coord, index) => (
                  <CustomMarker
                      key={index}
                      coord={coord}
                      index={index}
                      type={index === 0 ? "current" : "destination"}
                  />
              ))}
        </MapContainer>
      </div>
  );
};


export default RouteMap;
