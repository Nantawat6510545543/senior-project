import { SubHeader } from "@/components/Fonts"
import NumberInput from "@/components/NumberInput"
import PurpleCheckbox from "@/components/PurpleCheckbox"

export default function PSDTab() {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          "fmin",
          "fmax",
        ].map((f) => (
          <div key={f}>
            <SubHeader>{f}</SubHeader>
            <NumberInput />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="mt-4 flex items-center gap-2">
          <PurpleCheckbox />
          <SubHeader>Average</SubHeader>
        </div>

        <div className="mt-4 flex items-center gap-2">
          <PurpleCheckbox />
          <SubHeader>dB</SubHeader>
        </div>

        <div className="mt-4 flex items-center gap-2">
          <PurpleCheckbox />
          <SubHeader>Spatial Colors</SubHeader>
        </div>
      </div>
    </div>
  )
}
