import { YMapLocation } from "@yandex/ymaps3-types/imperative/YMap";

import type { LngLat, DrawingStyle, RouteOptions, TruckParameters } from '@yandex/ymaps3-types';

export const location: YMapLocation = { center: [25.229762, 55.289311], zoom: 9 };
export const apiKey = import.meta.env.VITE_APP_YMAP_KEY as string;

// Wait for the api to load to access the map configuration
// ymaps3.ready.then(() => {
//     // Copy your api key for routes from the developer's dashboard and paste it here
//     ymaps3.getDefaultConfig().setApikeys({ router: apiKey });
// });

// // An object containing the route line style
// export const lineStyle: DrawingStyle = {
//     fillRule: 'nonzero',
//     fill: '#333',
//     fillOpacity: 0.9,
//     stroke: [
//         { width: 6, color: '#007afce6' },
//         { width: 10, color: '#fff' }
//     ]
// };

// // Converting [Lng, Lat] coordinates to string format
// export function getPointStr(point: LngLat) {
//     //@ts-ignore
//     return point.map((c) => c.toFixed(4)).join('; ');
// }

// // The function for fetching a route between two points
// export async function fetchRoute(
//     startCoordinates: LngLat,
//     endCoordinates: LngLat,
//     type: RouteOptions['type'] = 'driving'
// ) {
//     let truck: TruckParameters;
//     if (type === 'truck') {
//         // set truck with trailer by default
//         truck = {
//             weight: 40,
//             maxWeight: 40,
//             axleWeight: 10,
//             payload: 20,
//             height: 4,
//             width: 2.5,
//             length: 16,
//             ecoClass: 4,
//             hasTrailer: true
//         };
//     }
//     // Request a route from the Router API with the specified parameters.
//     const routes = await ymaps3.route({
//         points: [startCoordinates, endCoordinates], // Start and end points of the route LngLat[]
//         type, // Type of the route
//         bounds: true, // Flag indicating whether to include route boundaries in the response
//     });

//     // Check if a route was found
//     if (!routes[0]) return;

//     // Convert the received route to a RouteFeature object.
//     const route = routes[0].toRoute();

//     // Check if a route has coordinates
//     if (route.geometry.coordinates.length == 0) return;

//     return route;
// }

// // Create a custom information message control
// export let InfoMessage = null;

// interface InfoMessageProps {
//     text: string;
// }

// // Wait for the api to load to access the entity system (YMapComplexEntity)
// ymaps3.ready.then(() => {
//     class InfoMessageClass extends ymaps3.YMapComplexEntity<InfoMessageProps> {
//         private _element!: HTMLDivElement;
//         private _detachDom!: () => void;

//         // Method for create a DOM control element
//         _createElement(props: InfoMessageProps) {
//             // Create a root element
//             const infoWindow = document.createElement('div');
//             infoWindow.className = 'infoWindow';
//             infoWindow.textContent = props.text;

//             // Create an icon element
//             const infoIcon = document.createElement('img');
//             infoIcon.src = '../info-icon.svg';
//             infoIcon.className = 'infoIcon';
//             infoWindow.appendChild(infoIcon);

//             return infoWindow;
//         }

//         // Method for attaching the control to the map
//         _onAttach() {
//             this._element = this._createElement(this._props);
//             this._detachDom = ymaps3.useDomContext(this, this._element, this._element);
//         }

//         // Method for detaching control from the map
//         _onDetach() {
//             this._detachDom();
//             //@ts-ignore
//             this._detachDom = undefined;
//             //@ts-ignore
//             this._element = undefined;
//         }
//     }
//     //@ts-ignore
//     InfoMessage = InfoMessageClass;
// });

// ymaps3.ready.then(() => {
//     ymaps3.import.registerCdn('https://cdn.jsdelivr.net/npm/{package}', ['@yandex/ymaps3-default-ui-theme@latest']);
// });