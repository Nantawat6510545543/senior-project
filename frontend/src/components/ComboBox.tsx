"use client";

import { useState } from "react";
import { ChevronsUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

interface ComboboxProps {
  options: { value: string; label: string }[];
  value: string;
  onChange: (value: string) => void;
}

export default function Combobox({ options, value, onChange }: ComboboxProps) {
  const [open, setOpen] = useState(false);

  const selectedLabel = options.find((opt) => opt.value === value)?.label || "Select option...";

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className="
            w-auto
            min-w-[200px]
            max-w-none
            justify-between
            bg-purple-200 border-purple-300 text-purple-800
          "
        >
          <span className="whitespace-nowrap">
            {selectedLabel}
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 flex-shrink-0" />
        </Button>
      </PopoverTrigger>

      <PopoverContent className="w-[200px] p-0">
        <ul className="py-1 text-purple-800">
          {options.map(({ value: val, label }) => (
            <li
              key={val}
              className={`cursor-pointer px-2 py-1 ${value === val ? "bg-purple-100" : "hover:bg-purple-50"}`}
              onClick={() => {
                onChange(value === val ? "" : val);
                setOpen(false);
              }}
            >
              {label}
            </li>
          ))}
        </ul>
      </PopoverContent>
    </Popover>
  );
}
