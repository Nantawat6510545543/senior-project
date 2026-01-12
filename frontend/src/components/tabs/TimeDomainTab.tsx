import NumberInput from "@/components/NumberInput"
import { SubHeader } from "@/components/Fonts"

export default function TimeDomainTab() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {[
        { label: "Duration", type: "number" },
        { label: "Start", type: "number" },
        { label: "Number of Channels", type: "number" },
      ].map((field) => (
        <div key={field.label}>
          <SubHeader>{field.label}</SubHeader>
          <NumberInput />
        </div>
      ))}
    </div>
  )
}
