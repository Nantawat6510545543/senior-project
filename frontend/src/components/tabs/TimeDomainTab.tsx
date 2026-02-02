import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"

export default function TimeDomainTab() {
  const schema = useSchema("time")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["time"]}
    />
  )
}