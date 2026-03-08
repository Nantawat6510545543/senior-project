import { Input } from "@/components/ui/input"

interface DecimalInputProps {
  value?: number | null
  placeholder?: string
  onChange?: (value: number | null) => void
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
      value={value ?? ""}
      placeholder={placeholder}
      onChange={(e) => {
        const v = e.target.value
        onChange?.(v === "" ? null : Number(v))
      }}
    />
  )
}