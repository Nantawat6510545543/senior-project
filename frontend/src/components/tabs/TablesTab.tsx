import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"

export default function TablesTab() {
  const schema = useSchema("tables")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["tables"]}
    />
  )
}