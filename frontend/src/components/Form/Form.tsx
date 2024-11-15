import React, { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import Select from "@/components/Form/DropdownSelect/Select";

import { teamsForSelect } from '../RouteMap/helpers';

interface TeamFormProps {
  onClick: (teamId: number | null, routeRound: number | null) => void;
  roundsCount: number[]; // Массив количества раундов для каждой команды
}

const Form: React.FC<TeamFormProps> = ({ onClick, roundsCount }) => {
  const teams = teamsForSelect;

  const [teamId, setTeamId] = useState<number | null>(null);
  const [routeRound, setRouteRound] = useState<number | null>(null);
  const [roundOptions, setRoundOptions] = useState<{ label: string; value: number }[]>([]);

  useEffect(() => {
    if (teamId !== null && roundsCount[teamId - 1]) {
      const options = Array.from(
          { length: roundsCount[teamId - 1] },
          (_, index) => ({
            label: `Маршрут №${index + 1}`,
            value: index + 1,
          })
      );
      options.unshift({ label: "Показать все маршруты", value: 'all' });
      setRoundOptions(options);
    } else {
      setRoundOptions([]);
      setRouteRound(null); // Сбросить выбранный раунд, если команда меняется
    }
  }, [teamId, roundsCount]);

  const handleClick = () => {
    onClick(teamId, routeRound);
  };

  return (
      <div className="z-10 flex flex-row gap-10">
        <Select options={teams} selectedValue={teamId} onSelect={setTeamId} placeholder="Выберите команду" />
        <Select options={roundOptions} selectedValue={routeRound} onSelect={setRouteRound} placeholder="Выберите маршрут" />
        <Button variant="secondary" onClick={handleClick}>
          Показать маршрут
        </Button>
      </div>
  );
};

export default Form;
