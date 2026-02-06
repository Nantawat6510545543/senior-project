import SchemaFieldGrid from "./SchemaFieldGrid"

// #TODO bring back "Combine Channels" AND "Show bad"
export default function FilteringCleaningTab(
  { sessionId, schema }: { sessionId: string, schema: any }
) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["filter", "channels", "cleaning"]}
      sessionId={sessionId}
      endpoint="filter"
    />
  )
}
