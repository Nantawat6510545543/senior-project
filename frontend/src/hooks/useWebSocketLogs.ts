import { useEffect, useState } from "react"

type LogMessage = {
  time: string
  level: string
  message: string
}

export function useWebSocketLogs(runId: string | null) {
  const [logs, setLogs] = useState<LogMessage[]>([])

  useEffect(() => {
    if (!runId) return

    setLogs([])

    const ws = new WebSocket(`ws://localhost:8000/progress/${runId}`)

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLogs((prev) => [...prev, data])
      } catch {
        // ignore malformed messages
      }
    }

    return () => ws.close()
  }, [runId])

  return logs
}