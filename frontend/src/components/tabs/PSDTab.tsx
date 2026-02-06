import SchemaFieldGrid from "./SchemaFieldGrid"

export default function PSDTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["psd"]}
      sessionId={sessionId}
      endpoint="psd"
    />
  )
}
