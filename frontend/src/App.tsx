import { useEffect, useState } from 'react'
import './App.css'
import RouteMap from './components/RouteMap/RouteMap'
import TeamForm from './components/TeamForm'

function App() {

  const [teamId, setTeamId] = useState<number | null>(null);
  const [currentRoute, setCurrentRoute] = useState<[number, number][] | null>(null)

  const [routeData, setRouteData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const handleChangeTeamId = (id: number | null) => {
    if (id !== null) {
      setTeamId(id);
      setCurrentRoute([routeData[id*10+id], routeData[id*20-id]])
    }
  }

  const fetchRouteData = async () => {
    setLoading(true); // Установка состояния загрузки
    setError(null); // Очистка ошибок перед запросом
    const requestId = 0;
    try {
      const response = await fetch(`http://localhost:9001/routes/${requestId}`, {
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setRouteData(data.routes); // Запись только массива маршрутов в состояние
      setLoading(false);
      console.log(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      console.error(err)
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRouteData()
  }, [])

  useEffect(() => {
    console.log(routeData);
  }, [routeData])

  if (error) {
    return <h3>Error: {error}</h3>;
  }

  return (
    <div className='w-screen p-10 flex flex-col gap-10'>
      <div className='flex flex-col items-start gap-4'>
        <h2>Маршруты инкассаторов</h2>
        <TeamForm onClick={handleChangeTeamId} />
      </div>
      <RouteMap coords={currentRoute} />
    </div>
  )
}

export default App
