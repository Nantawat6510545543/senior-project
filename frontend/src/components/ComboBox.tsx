"use client"

import { useState } from "react"
import { ChevronsUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Controller, useFormContext } from "react-hook-form"

interface ComboboxProps {
  name: string
  options: { value: string; label: string }[]
  placeholder?: string
  defaultValue?: string
}

export default function Combobox({
  name,
  options,
  placeholder = "Select option...",
  defaultValue = "",
}: ComboboxProps) {
  const { control } = useFormContext()
  const [open, setOpen] = useState(false)

  return (
    <Controller
      name={name}
      control={control}
      defaultValue={defaultValue}
      render={({ field }) => {
        const selectedLabel =
          options.find((opt) => opt.value === field.value)?.label ||
          placeholder

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

            <PopoverContent className="w-[200px] p-0 max-h-[50vh] overflow-y-auto overscroll-contain">
              <ul className="py-1 text-purple-800">
                {options.map(({ value: val, label }) => (
                  <li
                    key={val}
                    className={`cursor-pointer px-2 py-1 ${
                      field.value === val
                        ? "bg-purple-100"
                        : "hover:bg-purple-50"
                    }`}
                    onClick={() => {
                      field.onChange(field.value === val ? "" : val)
                      setOpen(false)
                    }}
                  >
                    {label}
                  </li>
                ))}
              </ul>
            </PopoverContent>
          </Popover>
        )
      }}
    />
  )
}