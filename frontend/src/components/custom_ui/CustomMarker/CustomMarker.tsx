import { Marker, Popup } from "react-leaflet";
import L from "leaflet";
import './CustomMarker.css';

type MarkerType = "current" | "destination" | "atm";

interface CustomMarkerProps {
  coord: [number, number];
  index: number;
  type: MarkerType;
}

const CustomMarker: React.FC<CustomMarkerProps> = ({ coord, index, type }) => {
  // В зависимости от типа маркера создаем иконки
  let icon;

  let popupText = `Банкомат ${index+1}`

  switch (type) {
    case "current":
      icon = new L.Icon({
        iconUrl: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIycmVtIiBoZWlnaHQ9IjJyZW0iIHZpZXdCb3g9IjAgMCAyNCAyNCI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iOCIgZmlsbD0iI2U4NDU0NSIgb3BhY2l0eT0iMC45NSIvPjxwYXRoIGZpbGw9IiNlODQ1NDUiIGQ9Ik0xMiAyQzYuNDcgMiAyIDYuNDcgMiAxMnM0LjQ3IDEwIDEwIDEwczEwLTQuNDcgMTAtMTBTMTcuNTMgMiAxMiAybTAgMThjLTQuNDIgMC04LTMuNTgtOC04czMuNTgtOCA4LThzOCAzLjU4IDggOHMtMy41OCA4LTggOCIvPjwvc3ZnPg==", // Путь к иконке текущей точки
        iconSize: [30, 30],
        iconAnchor: [16, 20],
        popupAnchor: [-1, -14],
      });
      popupText = "Вы здесь";
      break;

    case "destination":
      icon = new L.Icon({
        iconUrl: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxLjVyZW0iIGhlaWdodD0iMnJlbSIgdmlld0JveD0iMCAwIDM4NCA1MTIiPjxwYXRoIGZpbGw9IiMyNDI0MjRlZSIgZD0iTTE3Mi4yNjggNTAxLjY3QzI2Ljk3IDI5MS4wMzEgMCAyNjkuNDEzIDAgMTkyQzAgODUuOTYxIDg1Ljk2MSAwIDE5MiAwczE5MiA4NS45NjEgMTkyIDE5MmMwIDc3LjQxMy0yNi45NyA5OS4wMzEtMTcyLjI2OCAzMDkuNjdjLTkuNTM1IDEzLjc3NC0yOS45MyAxMy43NzMtMzkuNDY0IDBNMTkyIDI3MmM0NC4xODMgMCA4MC0zNS44MTcgODAtODBzLTM1LjgxNy04MC04MC04MHMtODAgMzUuODE3LTgwIDgwczM1LjgxNyA4MCA4MCA4MCIvPjwvc3ZnPg==", // Путь к иконке для точки назначения
        iconSize: [32, 32],
        iconAnchor: [16, 30],
        popupAnchor: [2, -30],
      });
      break;
    default:
      icon = new L.Icon({
        iconUrl: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIycmVtIiBoZWlnaHQ9IjJyZW0iIHZpZXdCb3g9IjAgMCAxMjAwIDEyMDAiPjxwYXRoIGZpbGw9IiMyNzI3MjdGQSIgZD0iTTYwMCAwQzM1MC4xNzggMCAxNDcuNjU2IDIwMi41MjEgMTQ3LjY1NiA0NTIuMzQ0YzAgODMuNTQ3IDE2LjM1MyAxNjkuODM3IDYzLjI4MSAyMzIuMDMxTDYwMCAxMjAwbDM4OS4wNjItNTE1LjYyNWM0Mi42MjUtNTYuNDkgNjMuMjgxLTE1Ni4zNTYgNjMuMjgxLTIzMi4wMzFDMTA1Mi4zNDQgMjAyLjUyMSA4NDkuODIyIDAgNjAwIDBtMCAyNjEuOTg3YzEwNS4xMTYgMCAxOTAuMzU2IDg1LjI0MSAxOTAuMzU2IDE5MC4zNTZDNzkwLjM1NiA1NTcuNDYgNzA1LjExNiA2NDIuNyA2MDAgNjQyLjdzLTE5MC4zNTYtODUuMjQtMTkwLjM1Ni0xOTAuMzU2UzQ5NC44ODQgMjYxLjk4NyA2MDAgMjYxLjk4NyIvPjwvc3ZnPg==", // Путь к иконке для точки назначения
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [2, -30],
      });
      break;
  }

  return (
      <Marker key={index} position={coord} icon={icon}>
        <Popup>{popupText}</Popup>
      </Marker>
  );
};

export default CustomMarker;
