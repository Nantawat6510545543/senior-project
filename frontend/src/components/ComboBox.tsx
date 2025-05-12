"use client"

import { useState } from "react";
import { Check, ChevronsUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

interface ComboboxProps {
  options: { value: string; label: string }[];
}

export function Combobox({ options }: ComboboxProps) {
  const [open, setOpen] = useState(false)
  const [value, setValue] = useState("")

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className="w-[200px] justify-between bg-purple-200 border border-purple-300 text-purple-800"
          aria-expanded={open}
        >
          {value
            ? options.find((option) => option.value === value)?.label
            : "Select options..."}
          <ChevronsUpDown className="ml-2 h-4 w-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <ul className="py-1">
          {options.map((option) => (
            <li
              key={option.value}
              className={`cursor-pointer px-2 py-1 ${
                value === option.value ? "bg-purple-100" : "hover:bg-purple-50"
              } text-purple-800`}
              onClick={() => {
                setValue(option.value === value ? "" : option.value);
                setOpen(false);
              }}
            >
              <span className="flex items-center">
                <Check
                  className={`mr-2 h-4 w-4 ${
                    value === option.value ? "opacity-100" : "opacity-0"
                  }`}
                />
                {option.label}
              </span>
            </li>
          ))}
        </ul>
      </PopoverContent>
    </Popover>
  )
}
