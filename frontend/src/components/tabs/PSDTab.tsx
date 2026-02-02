import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"

export default function PSDTab() {
  const schema = useSchema("psd")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["psd"]}
    />
  )
}