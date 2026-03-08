import { Input } from "@/components/ui/input"

interface IntegerInputProps {
  value?: number | null
  placeholder?: string
  onChange?: (value: number | null) => void
}

export default function IntegerInput({
  value,
  placeholder,
  onChange,
}: IntegerInputProps) {
  return (
    <Input
      type="text"
      inputMode="numeric"
      className="bg-purple-200 border-purple-300 text-purple-900 !text-base"
      value={value ?? ""}
      placeholder={placeholder}
      onChange={(e) => {
        const v = e.target.value
        onChange?.(v === "" ? null : parseInt(v))
      }}
    />
  )
}