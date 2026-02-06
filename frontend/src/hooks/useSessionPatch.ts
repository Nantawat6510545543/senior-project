
import { patchSession } from "@/api/api"
import { useEffect, useRef } from "react"
import type { SchemaEndpoints } from "./useSchema"

export default function useSessionPatch(
  sessionId: string,
  endpoint: SchemaEndpoints,
  data: Record<string, any>
) {
  const first = useRef(true)
  const timeout = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (!sessionId) return

    // skip initial hydration
    if (first.current) {
      first.current = false
      return
    }

    if (timeout.current) clearTimeout(timeout.current)

    timeout.current = setTimeout(() => {
      patchSession(sessionId, endpoint, data).catch(console.error)
    }, 400)

    return () => {
      if (timeout.current) clearTimeout(timeout.current)
    }
  }, [data, sessionId, endpoint])
}
