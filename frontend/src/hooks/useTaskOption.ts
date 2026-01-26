import { getTasks } from "@/api/api";
import { useEffect, useState } from "react"

export function useTaskOption(subject: string) {
  const [taskOptions, setTaskOptions] = useState<
    { value: string; label: string }[]
  >([])

  useEffect(() => {
    if (!subject) {
      setTaskOptions([])
      return
    }

    getTasks(subject)
      .then((tasks) =>
        setTaskOptions(tasks.map(([task]) => ({ value: task, label: task })))
      )
      .catch(console.error)
  }, [subject])

  return taskOptions
}
