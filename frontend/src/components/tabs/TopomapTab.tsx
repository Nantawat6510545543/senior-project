import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TopomapTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["topomap"]}
      endpoint="topomap"
    />
  )
}
