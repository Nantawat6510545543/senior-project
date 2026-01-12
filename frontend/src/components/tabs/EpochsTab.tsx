import { SubHeader } from "@/components/Fonts"
import NumberInput from "@/components/NumberInput"
import { Input } from "@/components/ui/input"

export default function EpochsTab() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {[
        { label: "tmin", type: "number" },
        { label: "tmax", type: "number" },
        { label: "Stimulus", type: "text" },
      ].map((field) => (
        <div key={field.label}>
          <SubHeader>{field.label}</SubHeader>
          {field.type === "number" ? <NumberInput /> : <Input />}
        </div>
      ))}
    </div>
  )
}
