
import { patchSession } from "@/api/api"
import { useEffect, useRef } from "react"


export default function useSessionPatch(
  sessionId: string,
  endpoint: any,
  data: any
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
      const cleaned = Object.fromEntries(
        Object.entries(data ?? {}).map(([k, v]) => {
          if (v === "") return [k, null]
          return [k, v]
        })
      )

      patchSession(sessionId, endpoint, cleaned).catch(console.error)
    }, 100)

    return () => {
      if (timeout.current) clearTimeout(timeout.current)
    }
  }, [data, sessionId, endpoint])
}
