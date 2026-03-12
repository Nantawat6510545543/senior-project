import { Input } from "@/components/ui/input"
import { Controller, useFormContext } from "react-hook-form"

interface TextInputProps {
  name: string
  placeholder?: string
  defaultValue?: string | null
}

export default function TextInput({
  name,
  placeholder,
  defaultValue = "",
}: TextInputProps) {
  const { control } = useFormContext()

  return (
    <Controller
      name={name}
      control={control}
      defaultValue={defaultValue ?? ""}
      render={({ field }) => (
        <Input
          type="text"
          className="bg-purple-200 border-purple-300 text-purple-900 !text-base"
          value={field.value ?? ""}
          placeholder={placeholder}
          onChange={(e) => field.onChange(e.target.value)}
        />
      )}
    />
  )
}