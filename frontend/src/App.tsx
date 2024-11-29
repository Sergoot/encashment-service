import {useEffect, useState} from 'react'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import './App.css'
import RouteMap from './components/RouteMap/RouteMap'
import Form from './components/Form/Form.tsx'
import {startTeamsAndRoutes} from './components/RouteMap/helpers';
import {Terminal} from "lucide-react";

const teamsAndRoutes = {...startTeamsAndRoutes};

function App() {
  const [currentRoute, setCurrentRoute] = useState<number[] | null>(null)
  const [currentTeamId, setCurrentTeamId] = useState<number | null>(null)
  const [showAlert, setShowAlert] = useState(false);
  // const [routesData, setRoutesData] = useState<any>(mockCarRoutes);
  // const [loading, setLoading] = useState<boolean>(true);
  // const [error, setError] = useState<string | null>(null);
  // const routesData = mockCarRoutes;
  // const roundsCount = mockCarRoutes.map(route => route.route?.length - 1 || 0);

  const showNextRoute = (teamId: number | null) => {
    setCurrentTeamId(teamId);
    if (teamId === null) return;
    const countRoutePoints = teamsAndRoutes[teamId].routePoints.length;
    const currentRound = teamsAndRoutes[teamId].routeRound;
    if (currentRound < countRoutePoints - 1) {
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routeRound + 1;
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound], teamsAndRoutes[teamId].routePoints[currentRound+1]])
    } else {
      fetchRouteData(teamId);
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routeRound + 1;
    }
  }

  const showCurrentRoute = (teamId: number) => {
    setCurrentTeamId(teamId);
    if (teamsAndRoutes[teamId].routePoints.length === 1) {
      fetchRouteData(teamId);
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routeRound + 1;
    } else {
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[teamsAndRoutes[teamId].routePoints.length - 2],teamsAndRoutes[teamId].startPoint])
    }
  }

  const showPreviousRoute = (teamId: number | null) => {
    if (teamId === null) return;
    const currentRound = teamsAndRoutes[teamId].routeRound;
    if (currentRound === 1) {
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound-1], teamsAndRoutes[teamId].routePoints[currentRound]])
      setShowAlert(true);
      // Через 3 секунды скрываем alert (по желанию)
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
    } else {
      if (currentRound === 2) {
        setShowAlert(true);
        // Через 3 секунды скрываем alert (по желанию)
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
      }
      teamsAndRoutes[teamId].routeRound =  teamsAndRoutes[teamId].routeRound - 1;
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound-2], teamsAndRoutes[teamId].routePoints[currentRound-1]])
    }
  }

  const fetchRouteData = async (teamId: number | null) => {
    // setLoading(true); // Установка состояния загрузки
    // setError(null); // Очистка ошибок перед запросом
    const requestId = teamId || 0;
    const {lat: current_lat, lon: current_lon} = teamsAndRoutes[requestId].startPoint;
    try {
      const response = await fetch(`http://localhost:9001/routes/?current_lat=${current_lat}&current_long=${current_lon}&radius=5000`, {
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        console.error(new Error(`Error: ${response.status}`));
      }

      const data = await response.json();
      // @ts-ignore
      const newPoint = {lat: data.next_step.coords.lat, lon: data.next_step.coords.long};
      setCurrentRoute([teamsAndRoutes[requestId].startPoint, newPoint])
      teamsAndRoutes[requestId].startPoint = {...newPoint};

      teamsAndRoutes[requestId].routePoints.push({...newPoint});
      // setLoading(false);
      console.log(data);
      console.log([teamsAndRoutes[requestId].startPoint, data.next_step.osm_id]);
    } catch (err: any) {
      // setError(err.message || 'An error occurred');
      console.error(err)
      // setLoading(false);
    }
  };
  const fillDb = async () => {
    try {
      const response = await fetch('http://localhost:9002/atm/v1/fill_db', {
        method: 'POST',
      });
      const data = await response.json();
      console.log(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fillDb()
  }, [])

  // useEffect(() => {
  //   console.log(routesData);
  // }, [routesData])

  // if (error) {
  //   return <h3>Error: {error}</h3>;
  // }

  return (
      <div className='w-screen p-10 flex flex-col gap-10'>
        {showAlert && (
            <div
                className="fixed top-0 right-0 z-50 p-4"
                style={{
                  position: 'fixed',
                  top: '20px',
                  right: '20px',
                  zIndex: 9999,
                  width: '400px',
                  padding: '10px 20px',
                  color: 'white',
                  transition: 'opacity 0.5s ease-in-out',
                }}
            >
              <Alert>
                <Terminal className="h-4 w-4" />
                <AlertTitle>Внимание!</AlertTitle>
                <AlertDescription>Это первый маршрут данной команды.</AlertDescription>
              </Alert>
            </div>
        )}
        <div className='flex flex-col items-start gap-4'>
          <h2>Маршруты инкассаторов</h2>
          <Form showNextRoute={showNextRoute} showCurrentRoute={showCurrentRoute} showPreviousRoute={showPreviousRoute} currentRound={teamsAndRoutes[currentTeamId || 1].routeRound}/>
        </div>
        <RouteMap coords={currentRoute} teamId={currentTeamId}/>
      </div>
  )
}

export default App
