import { SubHeader } from "@/components/Fonts"
import NumberInput from "@/components/NumberInput"

export default function TopomapTab() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <div>
        <SubHeader>Times</SubHeader>
        <NumberInput />
      </div>
    </div>
  )
}
