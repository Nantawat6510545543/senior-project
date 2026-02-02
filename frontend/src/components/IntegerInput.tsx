import { Input } from "@/components/ui/input"

interface IntegerInputProps {
  value?: string
  placeholder?: string
  onChange?: (value: string) => void
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
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange?.(e.target.value)}
    />
  )
}