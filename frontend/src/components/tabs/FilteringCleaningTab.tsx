import SchemaFieldGrid from "../forms/SchemaFieldGrid"

// #TODO bring back "Combine Channels" AND "Show bad"
export default function FilteringCleaningTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["filter", "channels", "cleaning"]}
      endpoint="filter"
    />
  )
}
