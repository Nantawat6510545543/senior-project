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
          const value = run ? `${task}_run-${run}` : task
          const label = run ? `${task} (run ${run})` : task
          return { value, label }
        })
      )
    })
    .catch(console.error)
  }, [subject])

  return taskOptions
}
