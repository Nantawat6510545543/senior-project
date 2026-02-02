import { Checkbox } from "@/components/ui/checkbox"

interface PurpleCheckboxProps {
  checked: boolean
  onChange: (checked: boolean) => void
}

export default function PurpleCheckbox({ checked, onChange }: PurpleCheckboxProps) {
  return (
    <Checkbox
      checked={checked}
      onCheckedChange={(v) => onChange(Boolean(v))}
      className="
        border-purple-800
        data-[state=checked]:bg-purple-700
        data-[state=checked]:text-white
      "
    />
  )
}
