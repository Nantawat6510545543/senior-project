import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function EvokedDisplayTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["evoked"]}
      endpoint="evoked"
    />
  )
}
