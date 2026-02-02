import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"

export default function TopomapTab() {
  const schema = useSchema("topomap")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["topo"]}
    />
  )
}