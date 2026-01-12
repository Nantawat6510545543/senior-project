import NumberInput from "@/components/NumberInput"
import { SubHeader } from "@/components/Fonts"

export default function TablesTab() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {[
        { label: "rows", type: "number" },
        { label: "table_type", type: "number" },
      ].map((field) => (
        <div key={field.label}>
          <SubHeader>{field.label}</SubHeader>
          <NumberInput />
        </div>
      ))}
    </div>
  )
}