import SchemaFieldGrid from "./SchemaFieldGrid"

export default function TablesTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["tables"]}
      sessionId={sessionId}
      endpoint="tables"
    />
  )
}