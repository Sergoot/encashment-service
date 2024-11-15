import React, { useState } from 'react';
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Check, ChevronsUpDown } from "lucide-react";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { cn } from "@/lib/utils";

type Option = {
  label: string;
  value: string | number;
};

interface DropdownSelectProps {
  options: Option[];
  selectedValue: string | number | null;
  onSelect: (value: string | number | null) => void;
  placeholder?: string;
}

const DropdownSelect: React.FC<DropdownSelectProps> = ({ options, selectedValue, onSelect, placeholder = "Выберите..." }) => {
  const [open, setOpen] = useState(false);

  const handleSelect = (value: string | number) => {
    onSelect(value === selectedValue ? null : value);
    setOpen(false);
  };

  return (
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
              variant="outline"
              role="combobox"
              aria-expanded={open}
              className="min-w-[200px] justify-between"
          >
            {selectedValue
                ? options.find((option) => option.value === selectedValue)?.label
                : placeholder}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[200px] p-0">
          <Command>
            <CommandInput placeholder="Поиск..." />
            <CommandList>
              <CommandEmpty>Ничего не найдено.</CommandEmpty>
              <CommandGroup>
                {options.map((option) => (
                    <CommandItem
                        key={option.value}
                        onSelect={() => handleSelect(option.value)}
                    >
                      <Check
                          className={cn(
                              "mr-2 h-4 w-4",
                              selectedValue === option.value ? "opacity-100" : "opacity-0"
                          )}
                      />
                      {option.label}
                    </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
  );
};

export default DropdownSelect;
