import { Checkbox } from "@/components/ui/checkbox"

export default function PurpleCheckbox() {
  return (
    <Checkbox
      className="
        border-purple-800
        data-[state=checked]:bg-purple-700
        data-[state=checked]:text-white
      "
    />
  )
}