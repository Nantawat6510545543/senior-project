import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"

export default function EpochsTab() {
  const schema = useSchema("evoked")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["evoked"]}
    />
  )
}