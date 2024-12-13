import React, {useState} from 'react';
import {Button} from "@/components/ui/button";
import Select from "@/components/Form/DropdownSelect/Select";
import {Badge} from "@/components/ui/badge"
import {Loader2} from "lucide-react"


import {teamsForSelect} from '../RouteMap/helpers';

interface TeamFormProps {
  showNextRoute: (teamId: number | null) => void;
  showCurrentRoute: (teamId: number) => void;
  showPreviousRoute: (teamId: number | null) => void;
  showWayHome: (teamId: number | null) => void;
  currentRound: number;
  isDayFinished: boolean;
  isFinalRound: boolean;
  loading: boolean;
  // roundsCount: number[]; // Массив количества раундов для каждой команды
}

const Form: React.FC<TeamFormProps> = ({
                                         showNextRoute,
                                         showCurrentRoute,
                                         showPreviousRoute,
                                         showWayHome,
                                         currentRound,
                                         isDayFinished,
                                         isFinalRound,
                                         loading
                                       }) => {
  const teams = teamsForSelect;
  const [teamId, setTeamId] = useState<number | null>(null);

  const handleTeamSelect = (teamId: number) => {
    setTeamId(teamId);
    if (teamId !== null) {
      showCurrentRoute(teamId);
    }
  }

  const handleClickNext = () => {
    showNextRoute(teamId);
  };
  const handleClickPrev = () => {
    showPreviousRoute(teamId);
  }
  const handleClickWayHome = () => {
    showWayHome(teamId);
  }

  const routeRoundMessage = (isFinalRound && isDayFinished) ? 'Маршрут на базу' : `Маршрут №${currentRound}`;

  return (
      <div className="z-10 w-full flex flex-row justify-between">
        <div className="flex flex-row gap-5">
          <Select options={teams} selectedValue={teamId} onSelect={handleTeamSelect} placeholder="Выберите команду"/>
          <Button disabled={!teamId || !(currentRound > 1) || loading} variant="secondary" onClick={handleClickPrev}>
            Предыдущий маршрут
          </Button>
          <Button disabled={!teamId || (isFinalRound && isDayFinished) || loading} onClick={handleClickNext}>
            Следующий маршрут
          </Button>
          {teamId &&
            <Badge variant="outline" className="flex justify-center">{routeRoundMessage}</Badge>
          }
          {loading && <div className={'self-center gap-2  align-middle flex flex-row'}>
            <Loader2 className="animate-spin"/>
            Идёт загрузка...
          </div>}
        </div>
        {teamId &&
          <div className="z-10">
            {isDayFinished ? (
                <Button disabled variant='destructive'>Рабочий день завершён</Button>
            ) : (
                <Button variant='destructive' disabled={loading} onClick={handleClickWayHome}>Завершить рабочий
                  день</Button>
            )}
          </div>
        }
      </div>
  );
};

export default Form;
