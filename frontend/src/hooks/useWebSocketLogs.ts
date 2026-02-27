import { useEffect, useState } from "react"

type LogMessage = {
  time: string
  level: string
  message: string
}

export function useWebSocketLogs(sessionId: string | null) {
  const [logs, setLogs] = useState<LogMessage[]>([])

  useEffect(() => {
    if (!sessionId) return

    setLogs([])

    const ws = new WebSocket(`ws://localhost:8000/progress/${sessionId}`)

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLogs((prev) => [...prev, data])
      } catch {
        // ignore malformed messages
      }
    }

    return () => ws.close()
  }, [sessionId])

  return logs
}