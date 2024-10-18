import { useState } from 'react'
import './App.css'
import RouteMap from './components/RouteMap/RouteMap'
import TeamForm from './components/TeamForm'

function App() {

  const [teamId, setTeamId] = useState<number | null>(null);

  // const [routeData, setRouteData] = useState<any>(null);
  // const [loading, setLoading] = useState<boolean>(true);
  // const [error, setError] = useState<string | null>(null);

  // const fetchRouteData = async () => {
  //   const id = 0; // временная заглушка для теста запросов
  //   try {
  //     const response = await fetch(`http://localhost:9001/routes/${id}`);

  //     if (!response.ok) {
  //       throw new Error(`Error: ${response.status}`);
  //     }

  //     const data = await response.json();
  //     setRouteData(data);
  //     setLoading(false);
  //   } catch (err: any) {
  //     setError(err.message || 'An error occurred');
  //     setLoading(false);
  //   }
  // };

  // if (error) {
  //   return <div>Error: {error}</div>;
  // }

  // const handleClick = () => {
  //   setCount((count) => count + 1);
  //   fetchRouteData();
  // }

  // useEffect(() => {
  //   console.log(routeData);
  // },[routeData])

  return (
    <div className='w-screen p-10 flex flex-col gap-10'>
      <div className='flex flex-col items-start gap-4'>
        <h2>Маршруты инкассаторов</h2>
        <TeamForm setTeamId={setTeamId} />
      </div>
      <RouteMap teamId={teamId} />
    </div>
  )
}

export default App
