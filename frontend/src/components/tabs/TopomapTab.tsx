import SchemaFieldGrid from "./SchemaFieldGrid"

export default function TopomapTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["topomap"]}
      sessionId={sessionId}
      endpoint="topomap"
    />
  )
}
