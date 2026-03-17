import { getTasks } from "@/api/api";
import { useEffect, useState } from "react"

export default function useTaskOption(subject: string) {
  const [taskOptions, setTaskOptions] = useState<
    { value: string; label: string }[]
  >([])

  useEffect(() => {
    if (!subject) {
      setTaskOptions([])
      return
    }

    getTasks(subject)
    .then((tasks) => {
      setTaskOptions(
        tasks.map(([task, run]) => {
          if (!run) {
            return { value: task, label: task }
          }

          return {
            value: `${task}|run=${run}`,
            label: `${task} (run ${run})`,
          }
        })
      )
    })
    .catch(console.error)
  }, [subject])

  return taskOptions
}
