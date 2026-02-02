import { useEffect, useState } from "react"
import { apiFetch } from "@/api/api"

export const schemaPaths = [
  "filter",
  "epochs",
  "psd",
  "evoked",
  "topomap",
  "time",
  "tables",
] as const

export type SchemaPath = typeof schemaPaths[number]

export function useSchema(name: SchemaPath) {
  const [schema, setSchema] = useState<any>(null)

  useEffect(() => {
    apiFetch(`/schemas/${name}`, {}).then(setSchema)
  }, [name])

  return schema
}