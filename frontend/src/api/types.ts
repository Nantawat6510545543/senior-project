export interface SingleSubjectTask {
  task: string
  subject: string
  run?: string | null
}

export type Range = {
  min: number | null
  max: number | null
}

export type SessionFormSchema = {
  subject_type: "single" | "cohort"

  task: SingleSubjectTask

  subject_filter: {
    task: string | null
    subject_limit: number | null
    per_subject: boolean
    sex: string

    age: Range
    ehq_total: Range
    p_factor: Range
    attention: Range
    internalizing: Range
    externalizing: Range
    ccd_accuracy: Range
    ccd_response_time: Range
  }

  filter: Record<string, any>
  epochs: Record<string, any>
  time: Record<string, any>
  psd: Record<string, any>
  evoked: Record<string, any>
  topomap: Record<string, any>
  table: Record<string, any>
}

export const schemaEndpoints = [
  "filter",
  "epochs",
  "psd",
  "evoked",
  "topomap",
  "time",
  "table",
  "training",
  "subject_type",
] as const

export type SchemaEndpoints = typeof schemaEndpoints[number]
