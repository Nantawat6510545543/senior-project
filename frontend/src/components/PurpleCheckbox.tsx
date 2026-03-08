import { Checkbox } from "@/components/ui/checkbox"
import { Controller, useFormContext } from "react-hook-form"

interface PurpleCheckboxProps {
  name: string
  defaultValue?: boolean
}

export default function PurpleCheckbox({
  name,
  defaultValue = false,
}: PurpleCheckboxProps) {
  const { control } = useFormContext()

  return (
    <Controller
      name={name}
      control={control}
      defaultValue={defaultValue}
      render={({ field }) => (
        <Checkbox
          checked={Boolean(field.value)}
          onCheckedChange={(v) => field.onChange(Boolean(v))}
          className="
            border-purple-800
            data-[state=checked]:bg-purple-700
            data-[state=checked]:text-white
          "
        />
      )}
    />
  )
}