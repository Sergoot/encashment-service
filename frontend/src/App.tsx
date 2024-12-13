import {useEffect, useState} from 'react'
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert"
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
  const [alertMessage, setAlertMessage] = useState('Это первый маршрут данной команды.');
  const [loading, setLoading] = useState(false);

  const showWayHome = (teamId: number | null) => {
    setCurrentTeamId(teamId);
    if (teamId === null) return;
    if (teamsAndRoutes[teamId].isDayFinished) {
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routePoints.length-1;
      teamsAndRoutes[teamId].isDayFinished = true;
    } else {
      teamsAndRoutes[teamId].routePoints.push(teamsAndRoutes[teamId].routePoints[0]);
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routePoints.length-1;
      teamsAndRoutes[teamId].isDayFinished = true;
    }
    const length = teamsAndRoutes[teamId].routePoints.length;
    setCurrentRoute([teamsAndRoutes[teamId].routePoints[length-2], teamsAndRoutes[teamId].routePoints[length-1]])
  }

  useEffect(() => {
    console.log(currentRoute)
    if (currentTeamId)
    console.log(teamsAndRoutes[currentTeamId].routePoints)
  }, [currentRoute]);

  const showNextRoute = (teamId: number | null) => {
    setCurrentTeamId(teamId);
    if (teamId === null) return;
    const countRoutePoints = teamsAndRoutes[teamId].routePoints.length;
    const currentRound = teamsAndRoutes[teamId].routeRound;
    const isDayFinished = teamsAndRoutes[teamId].isDayFinished;
    if (currentRound < countRoutePoints - 1 || isDayFinished) {
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routeRound + 1;
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound], teamsAndRoutes[teamId].routePoints[currentRound + 1]])
      if (isDayFinished && currentRound === countRoutePoints-2) {
        setShowAlert(true);
        setAlertMessage('Это последний маршрут данной команды на сегодня.');
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
      }
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
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[teamsAndRoutes[teamId].routePoints.length - 2], teamsAndRoutes[teamId].startPoint])
    }
  }

  const showPreviousRoute = (teamId: number | null) => {
    if (teamId === null) return;
    const currentRound = teamsAndRoutes[teamId].routeRound;
    if (currentRound === 1) {
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound - 1], teamsAndRoutes[teamId].routePoints[currentRound]])
      setShowAlert(true);
      setAlertMessage('Это первый маршрут данной команды.');
      setTimeout(() => {
        setShowAlert(false);
      }, 3000);
    } else {
      if (currentRound === 2) {
        setShowAlert(true);
        setAlertMessage('Это первый маршрут данной команды.');
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
      }
      teamsAndRoutes[teamId].routeRound = teamsAndRoutes[teamId].routeRound - 1;
      setCurrentRoute([teamsAndRoutes[teamId].routePoints[currentRound - 2], teamsAndRoutes[teamId].routePoints[currentRound - 1]])
    }
  }

  const fetchRouteData = async (teamId: number | null) => {
    const requestId = teamId || 0;
    const {lat: current_lat, lon: current_lon} = teamsAndRoutes[requestId].startPoint;

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:9001/routes/?current_lat=${current_lat}&current_long=${current_lon}&radius=1000`, {
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        console.error(new Error(`Error: ${response.status}`));
      }

      const data = await response.json();
      if (data.next_step === 'FINAL') {
        setShowAlert(true);
        setAlertMessage('Это последний маршрут данной команды на сегодня.');
        setTimeout(() => {
          setShowAlert(false);
        }, 3000);
        showWayHome(teamId);
      } else {
        // @ts-ignore
        const newPoint = {lat: data.next_step.coords.lat, lon: data.next_step.coords.long};
        setCurrentRoute([teamsAndRoutes[requestId].startPoint, newPoint])
        teamsAndRoutes[requestId].startPoint = {...newPoint};

        teamsAndRoutes[requestId].routePoints.push({...newPoint});
        console.log(data);
        console.log([teamsAndRoutes[requestId].startPoint, data.next_step.osm_id]);
      }
    } catch (err: any) {
      console.error(err)
    } finally {
      setLoading(false);
    }
  };
  const fillDb = async () => {
    try {
      const response = await fetch('http://localhost:9002/api/v1/atm', {
        method: 'POST',
      });
      const data = await response.json();
      console.log(data);
    } catch (err) {
      console.error(err);
    }
  }

  // useEffect(() => {
  //   fillDb()
  // }, [])

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
                <Terminal className="h-4 w-4"/>
                <AlertTitle>Внимание!</AlertTitle>
                <AlertDescription>{alertMessage}</AlertDescription>
              </Alert>
            </div>
        )}
        <div className='flex flex-col items-start gap-4'>
          <h2>Маршруты инкассаторов</h2>
          <Form
              showNextRoute={showNextRoute}
              showCurrentRoute={showCurrentRoute}
              showPreviousRoute={showPreviousRoute}
              showWayHome={showWayHome}
              currentRound={teamsAndRoutes[currentTeamId || 1].routeRound}
              isDayFinished={teamsAndRoutes[currentTeamId || 1].isDayFinished}
              isFinalRound={teamsAndRoutes[currentTeamId || 1].routeRound === teamsAndRoutes[currentTeamId || 1].routePoints.length-1}
              loading={loading}
          />
        </div>
        <RouteMap coords={currentRoute} teamId={currentTeamId}/>
      </div>
  )
}

export default App
