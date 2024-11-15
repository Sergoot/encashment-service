import {useEffect, useState} from 'react'
import './App.css'
import RouteMap from './components/RouteMap/RouteMap'
import Form from './components/Form/Form.tsx'
import {mockCarRoutes} from './components/RouteMap/helpers';
import {route} from "@yandex/ymaps3-types";

function App() {
  const [currentRoute, setCurrentRoute] = useState<number[] | null>(null)
  const [currentTeamId, setCurrentTeamId] = useState<number | null>(null)
  // const [routesData, setRoutesData] = useState<any>(mockCarRoutes);
  // const [loading, setLoading] = useState<boolean>(true);
  // const [error, setError] = useState<string | null>(null);
  const routesData = mockCarRoutes;
  const roundsCount = mockCarRoutes.map(route => route.route?.length - 1 || 0);

  const handleChangeForm = (teamId: number | null, routeRound: number | null) => {
    console.log(routeRound)
    if (teamId !== null) {
      setCurrentTeamId(teamId);
      if (routeRound !== null) {
        if (routeRound === 'all') {
          setCurrentRoute(routesData[teamId - 1]?.route || null)
        } else {
          setCurrentRoute(routesData[teamId - 1]?.route?.slice(routeRound - 1, routeRound + 1) || null)
        }
      } else {
        setCurrentRoute(null)
      }
    } else {
      setCurrentRoute(null);
    }
  }

  useEffect(() => {
    console.log(currentRoute)
  }, [currentRoute])

  // const fetchRouteData = async () => {
  //   // setLoading(true); // Установка состояния загрузки
  //   // setError(null); // Очистка ошибок перед запросом
  //   const requestId = 0;
  //   try {
  //     const response = await fetch(`http://localhost:9001/routes/${requestId}`, {
  //       headers: {
  //         'Accept': 'application/json',
  //       },
  //     });
  //
  //     if (!response.ok) {
  //       console.error(new Error(`Error: ${response.status}`));
  //     }
  //
  //     const data = await response.json();
  //     setRoutesData(data.routes); // Запись только массива маршрутов в состояние
  //     // setLoading(false);
  //     console.log(data);
  //   } catch (err: any) {
  //     // setError(err.message || 'An error occurred');
  //     console.error(err)
  //     // setLoading(false);
  //   }
  // };
  //
  // useEffect(() => {
  //   fetchRouteData()
  // }, [])

  // useEffect(() => {
  //   console.log(routesData);
  // }, [routesData])

  // if (error) {
  //   return <h3>Error: {error}</h3>;
  // }

  return (
      <div className='w-screen p-10 flex flex-col gap-10'>
        <div className='flex flex-col items-start gap-4'>
          <h2>Маршруты инкассаторов</h2>
          <Form onClick={handleChangeForm} roundsCount={roundsCount}/>
        </div>
        <RouteMap coords={currentRoute} teamId={currentTeamId}/>
      </div>
  )
}

export default App
