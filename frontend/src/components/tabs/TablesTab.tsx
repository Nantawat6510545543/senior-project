import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TablesTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["tables"]}
      endpoint="tables"
    />
  )
}