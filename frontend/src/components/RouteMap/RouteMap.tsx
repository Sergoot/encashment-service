import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polyline, useMap, Marker, Popup } from 'react-leaflet';
import "leaflet/dist/leaflet.css";
import polyline from '@mapbox/polyline';

const INIT_CENTER = [55.7558, 37.6173];

export type RouteCoords = [number, number][] | null;

const SetViewOnChange = ({ coords }: { coords: RouteCoords }) => {
    const map = useMap();
    useEffect(() => {
        if (coords !== null && coords.length > 0) {
            map.setView(coords[0], 13); // Устанавливаем центр и уровень зума
        } else {
            map.setView(INIT_CENTER, 13);
        }
    }, [coords, map]);

    return null; // Этот компонент не отображает ничего
};

const RouteMap = ({ coords }: { coords: RouteCoords }) => {
    const [routeCoords, setRouteCoords] = useState<[number, number][] | null>(null);
    const center = routeCoords !== null && routeCoords.length > 0 ? routeCoords[0] : INIT_CENTER;

    useEffect(() => {
        const fetchRoute = async () => {
            if (coords && coords.length > 1) {
                // Преобразуем массив координат в строку, разделенную точками с запятой
                const waypoints = coords.map(coord => `${coord[1]},${coord[0]}`).join(';');
                try {
                    const response = await fetch(`http://router.project-osrm.org/route/v1/driving/${waypoints}?overview=simplified&alternatives=false&steps=true&annotations=false`);

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
                    setRouteCoords(null); // Если произошла ошибка, сбрасываем координаты маршрута
                }
            }
        };

        fetchRoute();
    }, [coords]);

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
                <SetViewOnChange coords={routeCoords} />
                {
                    routeCoords !== null && routeCoords.length > 0 &&
                    <>
                        <Polyline positions={routeCoords} color="blue" />
                        {/* Добавляем маркеры для каждой точки маршрута */}
                        {coords.map((coord, index) => (
                            <Marker key={index} position={coord}>
                                <Popup>{`Точка ${index + 1}`}</Popup>
                            </Marker>
                        ))}
                    </>
                }
            </MapContainer>
        </div>
    );
};

export default RouteMap;
