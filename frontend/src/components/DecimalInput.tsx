import { Input } from "@/components/ui/input"

interface DecimalInputProps {
  value?: string
  placeholder?: string
  onChange?: (value: string) => void
}

export default function DecimalInput({
  value,
  placeholder,
  onChange,
}: DecimalInputProps) {
  return (
    <Input
      type="text"
      inputMode="decimal"
      className="bg-purple-200 border-purple-300 text-purple-900 !text-base"
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange?.(e.target.value)}
    />
  )
}
