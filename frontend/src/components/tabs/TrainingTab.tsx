import SchemaFieldGrid from "../forms/SchemaFieldGrid"

export default function TrainingTab({ schema }: { schema: any }) {
  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["training"]}
      endpoint="training"
    />
  )
}
