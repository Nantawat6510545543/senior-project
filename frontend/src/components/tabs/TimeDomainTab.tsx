import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TimeDomainTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["time"]}
      endpoint="time"
    />
  )
}
