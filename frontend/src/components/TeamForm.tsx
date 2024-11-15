import React from 'react';

import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "@/components/ui/command"
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover"
import {teamsForSelect } from './RouteMap/helpers';

const teams = teamsForSelect;

interface TeamFormProps {
    onClick: (id: number | null) => void
}

const TeamForm: React.FC<TeamFormProps> = ({ onClick }) => {

    const [open, setOpen] = React.useState(false)
    const [value, setValue] = React.useState<number | null>(null)

    const handleClick = () => {
        const id = !!value ? Number(value) : null;
        onClick(id)
    }



    return (
        <div className='z-10 flex flex-row gap-10'>
            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        className="w-[200px] justify-between"
                    >
                        {value
                            ? teams.find((team) => Number(team.value) === value)?.label
                            : "Выберите команду..."}
                        <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-[200px] p-0">
                    <Command>
                        <CommandInput placeholder="Поиск команды..." />
                        <CommandList>
                            <CommandEmpty>No framework found.</CommandEmpty>
                            <CommandGroup>
                                {teams.map((team) => (
                                    <CommandItem
                                        key={team.value}
                                        value={team.value}
                                        onSelect={(currentValue) => {
                                            setValue(Number(currentValue) === value ? null : Number(currentValue))
                                            setOpen(false)
                                        }}
                                    >
                                        <Check
                                            className={cn(
                                                "mr-2 h-4 w-4",
                                                value === Number(team.value) ? "opacity-100" : "opacity-0"
                                            )}
                                        />
                                        {team.label}
                                    </CommandItem>
                                ))}
                            </CommandGroup>
                        </CommandList>
                    </Command>
                </PopoverContent>
            </Popover>
            <Button variant={'secondary'} onClick={handleClick}>Показать маршрут</Button>
        </div>
    );
};

export default TeamForm;