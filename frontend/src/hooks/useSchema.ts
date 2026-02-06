import { useEffect, useState } from "react"
import { apiFetch } from "@/api/api"

export const schemaEndpoints = [
  "filter",
  "epochs",
  "psd",
  "evoked",
  "topomap",
  "time",
  "tables",
] as const

export type SchemaEndpoints = typeof schemaEndpoints[number]

export function useSchema(name: SchemaEndpoints) {
  const [schema, setSchema] = useState<any>(null)

  useEffect(() => {
    apiFetch(`/schemas/${name}`, {}).then(setSchema)
  }, [name])

  return schema
}