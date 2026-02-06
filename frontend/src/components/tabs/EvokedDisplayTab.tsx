import SchemaFieldGrid from "./SchemaFieldGrid"

export default function EvokedDisplayTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["evoked"]}
      sessionId={sessionId}
      endpoint="evoked"
    />
  )
}
