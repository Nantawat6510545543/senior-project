import SchemaFieldGrid from "../forms/SchemaFieldGrid"


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
