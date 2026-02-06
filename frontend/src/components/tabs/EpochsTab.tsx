import SchemaFieldGrid from "./SchemaFieldGrid"

// TODO why this tab doesn't render
export default function EpochsTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["epochs"]}
      sessionId={sessionId}
      endpoint="epochs"
    />
  )
}