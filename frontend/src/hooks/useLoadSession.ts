
import { getSession } from "@/api/api"
import { useEffect, useRef, useState } from "react"

export default function useLoadSession(sessionId: string, section: string) {
  const [data, setData] = useState<Record<string, any> | null>(null)
  const loaded = useRef(false)

  useEffect(() => {
    if (!sessionId || loaded.current) return

    getSession(sessionId)
      .then(session => {
        setData(session?.[section] ?? {})
        loaded.current = true
      })
      .catch(console.error)

  }, [sessionId, section])

  return data
}
