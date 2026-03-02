import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TimeDomainTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["time"]}
      sessionId={sessionId}
      endpoint="time"
    />
  )
}
