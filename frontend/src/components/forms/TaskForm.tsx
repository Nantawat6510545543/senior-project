"use client"

import Combobox from "@/components/ComboBox"
import { SubHeader } from "@/components/Fonts"
import { Controller, useForm } from "react-hook-form"
import useSubjectOption from "@/hooks/useSubjectOption"
import useTaskOption from "@/hooks/useTaskOption"
import useSessionPatch from "@/hooks/useSessionPatch"

type TaskFormValues = {
  subject: string
  task: string
  run: number | null
}

type Props = {
  sessionId: string
}

export default function TaskForm({ sessionId }: Props) {
  const { control, watch } = useForm<TaskFormValues>({
    defaultValues: {
      subject: "",
      task: "",
      run: null,
    },
  })

  const subject = watch("subject")
  const task = watch("task")
  const run = watch("run")

  useSessionPatch(sessionId, "task", {
    subject,
    task,
    run,
  })

  const subjectOptions = useSubjectOption()
  const taskOptions = useTaskOption(subject)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
    <div>
      <SubHeader>Subject</SubHeader>
      <Controller
        control={control}
        name="subject"
        render={({ field }) => (
            <Combobox
            options={subjectOptions}
            value={field.value}
            onChange={field.onChange}
            />
        )}
      />
    </div>

    <div>
      <SubHeader>Task</SubHeader>
      <Controller
        control={control}
        name="task"
        render={({ field }) => (
            <Combobox
            options={taskOptions}
            value={field.value}
            onChange={field.onChange}
            />
        )}
      />
    </div>
    </div>
  )
}