"use client"

import type { SessionFormSchema } from "@/api/types"
import { useForm, FormProvider } from "react-hook-form"

export default function SessionForm({ children }: { children: React.ReactNode }) {
  const methods = useForm<SessionFormSchema>({
    defaultValues: {
      subject_type: "single",

      // Force populate form
      task: {},
      subject_filter: {},
      filter: {},
      epochs: {},
      time: {},
      psd: {},
      evoked: {},
      topomap: {},
      table: {}
    }
  })

  return (
    <FormProvider {...methods}>
      {children}
    </FormProvider>
  )
}