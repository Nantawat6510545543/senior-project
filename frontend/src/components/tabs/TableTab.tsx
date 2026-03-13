import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TableTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["table"]}
      endpoint="table"
    />
  )
}