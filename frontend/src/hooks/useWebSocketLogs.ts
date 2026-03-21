import { useEffect, useState } from "react"
import { BACKEND_URL } from "@/config";

type LogMessage = {
  time: string
  level: string
  message: string
}

export function useWebSocketLogs(runId: string | null) {
  const [logs, setLogs] = useState<LogMessage[]>([])

  useEffect(() => {
    if (!runId) return

  setLogs([
    {
      time: new Date().toTimeString().split(" ")[0],
      level: "INFO",
      message: "Please wait until the server is connected before running the experiment..."
    }
  ])

    // WS URL: `ws://localhost:8000/progress/${runId}`
    const wsUrl = BACKEND_URL.replace(/^http/, "ws") + `/progress/${runId}`
    const ws = new WebSocket(wsUrl)


    ws.onopen = () => {
      setLogs((prev) => [
        ...prev,
        {
          time: new Date().toTimeString().split(" ")[0],
          level: "INFO",
          message: "Server is connected"
        }
      ])
    }

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