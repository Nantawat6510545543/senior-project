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