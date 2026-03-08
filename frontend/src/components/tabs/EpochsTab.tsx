import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function EpochsTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["epochs"]}
      endpoint="epochs"
    />
  )
}