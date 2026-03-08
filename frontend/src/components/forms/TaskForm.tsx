"use client"

import Combobox from "@/components/ComboBox"
import { SubHeader } from "@/components/Fonts"
import { Controller, useFormContext } from "react-hook-form"
import useSubjectOption from "@/hooks/useSubjectOption"
import useTaskOption from "@/hooks/useTaskOption"
import type { SessionFormSchema } from "@/api/types"


export default function TaskForm() {
  const { control, watch } = useFormContext<SessionFormSchema>()

  const subject = watch("task.subject")
  const subjectOptions = useSubjectOption()
  const taskOptions = useTaskOption(subject)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
      <div>
        <SubHeader>Subject</SubHeader>
        <Controller
          control={control}
          name="task.subject"
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
          name="task.task"
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