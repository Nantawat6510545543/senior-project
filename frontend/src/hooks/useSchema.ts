import { useEffect, useState } from "react"
import { apiFetch } from "@/api/api"
import type { SchemaEndpoints } from "@/api/types"

export function useSchema(name: SchemaEndpoints) {
  const [schema, setSchema] = useState<any>(null)

  useEffect(() => {
    apiFetch(`/schemas/${name}`, {}).then(setSchema)
  }, [name])

  return schema
}