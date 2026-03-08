import { Input } from "@/components/ui/input"
import { Controller, useFormContext } from "react-hook-form"

interface DecimalInputProps {
  name: string
  placeholder?: string
  defaultValue?: number | null
}

export default function DecimalInput({
  name,
  placeholder,
  defaultValue = null,
}: DecimalInputProps) {
  const { control } = useFormContext()

  return (
    <Controller
      name={name}
      control={control}
      defaultValue={defaultValue}
      render={({ field }) => (
        <Input
          type="text"
          inputMode="decimal"
          className="bg-purple-200 border-purple-300 text-purple-900 !text-base"
          value={field.value ?? ""}
          placeholder={placeholder}
          onChange={(e) => {
            const v = e.target.value
            field.onChange(v === "" ? null : Number(v))
          }}
        />
      )}
    />
  )
}