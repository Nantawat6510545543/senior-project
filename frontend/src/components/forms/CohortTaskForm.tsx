"use client"

import Combobox from "@/components/ComboBox"
import IntegerInput from "@/components/IntegerInput"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { SubHeader } from "@/components/Fonts"

export default function CohortTaskForm() {
  // TODO remove hardcode
  const taskOptions = [
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
        <Combobox
          name="subject_filter.task"
          options={taskOptions}
        />
      </div>

      {/* Subject Limit */}
      <div>
        <SubHeader>Subject limit</SubHeader>
        <IntegerInput
          name="subject_filter.subject_limit"
        />
      </div>

      {/* Per Subject */}
      <div className="flex items-center gap-2">
        <PurpleCheckbox
          name="subject_filter.per_subject"
        />
        <SubHeader>Per subject</SubHeader>
      </div>

      {/* Sex */}
      <div>
        <SubHeader>Sex</SubHeader>
        <Combobox
          name="subject_filter.sex"
          options={[
            { value: "None", label: "None" },
            { value: "M", label: "Male" },
            { value: "F", label: "Female" },
          ]}
        />
      </div>

      {/* Ranges */}
      {rangeFields.map((name) => (
        <div key={name}>
          <SubHeader>{name}_range</SubHeader>

          <div className="flex gap-2">
            <IntegerInput
              name={`subject_filter.${name}.min`}
              placeholder="min"
            />

            <IntegerInput
              name={`subject_filter.${name}.max`}
              placeholder="max"
            />
          </div>
        </div>
      ))}
    </div>
  )
}