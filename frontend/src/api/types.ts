export interface TrainModelData {
  model_name: string;
  dataset_name: string;
  epochs: number;
  kfolds: number;
}

export interface PredictModelData {
  file: File;
  model_name: string;
}

export interface EvaluateModelData {
  file: File;
}

export interface CompareModelData {
  file1: File;
  file2: File;
}

export interface SingleSubjectTask {
  task: string
  subject: string
  run?: string | null
}

// #TODO add types
export type PipelineSession = {
  task: SingleSubjectTask

  filter?: any
  epochs?: any
  psd?: any
  evoked?: any
  topomap?: any
  table?: any
}

export type Range = {
  min: number | null
  max: number | null
}
export type Range = {
  min: number | null
  max: number | null
}

export type SessionFormSchema = {
  subject_type: "single" | "cohort"

  task: {
    subject: string
    task: string
    run: number | null
  }

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
