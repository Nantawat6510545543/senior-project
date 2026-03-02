"use client"

import { useForm, Controller } from "react-hook-form"
import Combobox from "@/components/ComboBox"
import IntegerInput from "@/components/IntegerInput"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"
import useSessionPatch from "@/hooks/useSessionPatch"

function toSubjectFilterParams(values: CohortTaskFormValues) {
  return {
    ...values,
    sex: values.sex === "None" ? null : values.sex,
  }
}

type Range = {
  min: number | null
  max: number | null
}

type CohortTaskFormValues = {
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

type Props = {
  sessionId: string
}

export default function CohortTaskForm({ sessionId }: Props) {
  const { control, watch } = useForm<CohortTaskFormValues>({
    defaultValues: {
      task: "",
      subject_limit: null,
      per_subject: false,
      sex: "None",

      age: { min: null, max: null },
      ehq_total: { min: null, max: null },
      p_factor: { min: null, max: null },
      attention: { min: null, max: null },
      internalizing: { min: null, max: null },
      externalizing: { min: null, max: null },
      ccd_accuracy: { min: null, max: null },
      ccd_response_time: { min: null, max: null }
    },
  })

  const values = watch()

  const subjectFilter = toSubjectFilterParams(values)
  useSessionPatch(sessionId, "subject_filter", subjectFilter)

  // TODO fix hardcode
    const taskOptions: { value: string; label: string }[] = [
    { value: "DespicableMe", label: "DespicableMe" },
    { value: "DiaryOfAWimpyKid", label: "DiaryOfAWimpyKid" },
    { value: "FunwithFractals", label: "FunwithFractals" },
    { value: "RestingState", label: "RestingState" },
    { value: "ThePresent", label: "ThePresent" },
    { value: "contrastChangeDetection_run-1", label: "contrastChangeDetection (run 1)" },
    { value: "contrastChangeDetection_run-2", label: "contrastChangeDetection (run 2)" },
    { value: "contrastChangeDetection_run-3", label: "contrastChangeDetection (run 3)" },
    { value: "seqlearning8target", label: "seqlearning8target" },
    { value: "surroundSupp_run-1", label: "surroundSupp (run 1)" },
    { value: "surroundSupp_run-2", label: "surroundSupp (run 2)" },
    { value: "symbolSearch", label: "symbolSearch" },
    ]

  const rangeFields = [
    "age",
    "ehq_total",
    "p_factor",
    "attention",
    "internalizing",
    "externalizing",
    "ccd_accuracy",
    "ccd_response_time",
  ] as const

  return (
    <div className="space-y-4 mt-4">

      {/* Task */}
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

      {/* Subject Limit */}
      <div>
        <SubHeader>Subject limit</SubHeader>
        <Controller
          control={control}
          name="subject_limit"
          render={({ field }) => (
            <IntegerInput
              value={field.value ?? ""}
              onChange={field.onChange}
            />
          )}
        />
      </div>

      {/* Per Subject */}
      <div className="flex items-center gap-2">
        <Controller
          control={control}
          name="per_subject"
          render={({ field }) => (
            <PurpleCheckbox
              checked={field.value}
              onChange={field.onChange}
            />
          )}
        />
        <SubHeader>Per subject</SubHeader>
      </div>

      {/* Sex */}
      <div>
        <SubHeader>Sex</SubHeader>
        <Controller
          control={control}
          name="sex"
          render={({ field }) => (
            <Combobox
              options={[
                { value: "None", label: "None" },
                { value: "M", label: "Male" },
                { value: "F", label: "Female" },
              ]}
              value={field.value}
              onChange={field.onChange}
            />
          )}
        />
      </div>

      {/* Ranges */}
      {rangeFields.map((name) => (
        <div key={name}>
          <SubHeader>{name}_range</SubHeader>

          <div className="flex gap-2">
            <Controller
              control={control}
              name={`${name}.min`}
              render={({ field }) => (
                <IntegerInput
                  placeholder="min"
                  value={field.value ?? ""}
                  onChange={field.onChange}
                />
              )}
            />

            <Controller
              control={control}
              name={`${name}.max`}
              render={({ field }) => (
                <IntegerInput
                  placeholder="max"
                  value={field.value ?? ""}
                  onChange={field.onChange}
                />
              )}
            />
          </div>
        </div>
      ))}
    </div>
  )
}
