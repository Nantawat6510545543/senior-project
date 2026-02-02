import SchemaFieldGrid from "./SchemaFieldGrid"
import { useSchema } from "@/hooks/useSchema"


// #TODO bring back "Combine Channels" AND "Show bad"
export default function FilteringCleaningTab() {
  const schema = useSchema("filter")

  if (!schema) return null

  return (
    <SchemaFieldGrid
      schema={schema}
      groups={["filter", "cleaning"]}
    />
  )
}
