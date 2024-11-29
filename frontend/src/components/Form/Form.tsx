import React, {useState} from 'react';
import {Button} from "@/components/ui/button";
import Select from "@/components/Form/DropdownSelect/Select";

import {teamsForSelect} from '../RouteMap/helpers';

interface TeamFormProps {
  showNextRoute: (teamId: number | null) => void;
  showCurrentRoute: (teamId: number) => void;
  showPreviousRoute: (teamId: number | null) => void;
  currentRound: number;
  // roundsCount: number[]; // Массив количества раундов для каждой команды
}

const Form: React.FC<TeamFormProps> = ({showNextRoute, showCurrentRoute, showPreviousRoute, currentRound}) => {
  const teams = teamsForSelect;

  const [teamId, setTeamId] = useState<number | null>(null);
  // const [routeRound, setRouteRound] = useState<number | null>(null);
  // const [roundOptions, setRoundOptions] = useState<{ label: string; value: number }[]>([]);

  // useEffect(() => {
  //   if (teamId !== null) {
  //     // const options = Array.from(
  //     //     { length: roundsCount[teamId - 1] },
  //     //     (_, index) => ({
  //     //       label: `Маршрут №${index + 1}`,
  //     //       value: index + 1,
  //     //     })
  //     // );
  //     // options.unshift({ label: "Показать все маршруты", value: 'all' });
  //     // setRoundOptions(options);
  //   } else {
  //     // setRoundOptions([]);
  //     // setRouteRound(null); // Сбросить выбранный раунд, если команда меняется
  //   }
  // }, [teamId]);

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

  return (
      <div className="z-10 flex flex-row gap-5">
        <Select options={teams} selectedValue={teamId} onSelect={handleTeamSelect} placeholder="Выберите команду"/>
        {/*<Select options={roundOptions} selectedValue={routeRound} onSelect={setRouteRound} placeholder="Выберите маршрут" />*/}
        {/*<Button variant="secondary" onClick={handleClick}>*/}
        {/*  Показать маршрут*/}
        {/*</Button>*/}
        {teamId &&
            (<Button onClick={handleClickNext}>
              Показать следующий маршрут
            </Button>)
        }
        {teamId && currentRound > 1 &&
            (<Button variant="secondary" onClick={handleClickPrev}>
              Показать предыдущий маршрут
            </Button>)
        }

      </div>
  );
};

export default Form;
