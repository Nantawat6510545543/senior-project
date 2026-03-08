import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function PSDTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["psd"]}
      endpoint="psd"
    />
  )
}
