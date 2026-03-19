"use client"

import { useRef, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { useWebSocketLogs } from "@/hooks/useWebSocketLogs"

interface LogPanelProps {
  runId: string | null
}

export default function LogPanel({ runId }: LogPanelProps) {
  const logs = useWebSocketLogs(runId)
  const scrollRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const viewport = scrollRef.current?.querySelector(
      "[data-radix-scroll-area-viewport]"
    ) as HTMLDivElement | null

    if (viewport) {
      viewport.scrollTop = viewport.scrollHeight
    }
  }, [logs])

  return (
    <Card className="h-[300px] rounded-2xl shadow-lg border-purple-200 bg-purple-50">
      <CardHeader>
        <CardTitle className="text-purple-800">
          Execution Log
        </CardTitle>
      </CardHeader>

      <CardContent className="p-0">
        <ScrollArea
          ref={scrollRef}
          className="h-[230px] px-4 py-2 font-mono text-sm bg-white text-purple-900"
        >
          {logs.map((log, index) => (
            <div key={index} className="flex gap-2 items-start mb-1">
              <span className="text-purple-400">
                [{log.time}]
              </span>

              {log.level === "error" && (
                <Badge className="bg-purple-600 text-white">
                  ERROR
                </Badge>
              )}

              <span>{log.message}</span>
            </div>
          ))}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}