"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import NumberInput from "@/components/NumberInput"
import OptionButtons from "@/components/OptionsButton"
import Combobox from "@/components/ComboBox"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import SettingsTab from "@/components/TabRenderer"
import PrimaryButton from "@/components/PrimaryButton"
import { getPlotUrl } from "@/api/api"
import { SETTINGS_MODE } from "./settings_mode"
import { useSubjectOption } from "@/hooks/useSubjectOption"
import { useTaskOption } from "@/hooks/useTaskOption"


export default function EEGUI() {
  const [inputType, setInputType] = useState("Single subject")
  const [mode, setMode] = useState<keyof typeof SETTINGS_MODE>("Plot")
  const [action, setAction] = useState(
    Object.keys(SETTINGS_MODE.Plot.actions)[0]
  )

  const [plotUrl, setPlotUrl] = useState<string | null>(null)

  const [subject, setSubject] = useState("")
  const [task, setTask] = useState("")

  const modeData = SETTINGS_MODE[mode]
  const actions = Object.keys(modeData.actions)

  let safeAction = action
  if (!(safeAction in modeData.actions)) {
    safeAction = actions[0]
  }

  function handleRunInline() {
    const plotType = modeData.actions[safeAction]
    if (!plotType) return

    setPlotUrl(
      getPlotUrl({type: plotType, subject, task})
    )
  }

  const subjectOptions = useSubjectOption()
  const taskOptions = useTaskOption(subject)

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Input Type */}
      <Card className="p-4">
        <Header>Input Type:</Header>
        <OptionButtons
          options={["Single subject", "Meta filter (group)"]}
          value={inputType}
          onChange={setInputType}
        />

        {inputType === "Single subject" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
            <div>
              <SubHeader>Subject</SubHeader>
              <Combobox
                options={subjectOptions}
                value={subject}
                onChange={setSubject}
              />
            </div>

            <div>
              <SubHeader>Task</SubHeader>
              <Combobox
                options={taskOptions}
                value={task}
                onChange={setTask}
              />
            </div>
          </div>
        )}

        {inputType === "Meta filter (group)" && (
          <div className="space-y-4 mt-4">
            <SubHeader>Task</SubHeader>
            <Combobox
              options={taskOptions}
              value={task}
              onChange={setTask}
            />

            <SubHeader>Subject limit</SubHeader>
            <NumberInput />

            <div className="flex items-center gap-2">
              <PurpleCheckbox />
              <SubHeader>Per subject</SubHeader>
            </div>

            <SubHeader>Sex</SubHeader>
            <Combobox
              options={[
                { value: "None", label: "None" },
                { value: "Male", label: "Male" },
                { value: "Female", label: "Female" },
              ]}
            />

            {[
              "age",
              "ehq_total",
              "p_factor",
              "attention",
              "internalizing",
              "externalizing",
              "ccd_accuracy",
              "ccd_response_time",
            ].map(function (name) {
              return (
                <div key={name}>
                  <SubHeader>{name}_range</SubHeader>
                  <div className="flex gap-2">
                    <NumberInput placeholder="min" />
                    <NumberInput placeholder="max" />
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </Card>

      {/* Mode */}
      <Card className="p-4">
        <Header>Select Mode</Header>
        <OptionButtons
          options={Object.keys(SETTINGS_MODE)}
          value={mode}
          onChange={setMode}
        />
        <p className="text-sm text-muted-foreground max-w-3xl">
          {modeData.description}
        </p>
      </Card>

      {/* Action */}
      <Card className="p-4 space-y-3">
        <Header>Select Action:</Header>
        <OptionButtons
          options={actions}
          value={safeAction}
          onChange={setAction}
        />

        <div className="flex items-center gap-2">
          <PurpleCheckbox />
          <SubHeader>Show all groups</SubHeader>
        </div>
      </Card>

      <SettingsTab action={safeAction} />

      {/* Run */}
      <div className="flex gap-4">
        <PrimaryButton>Run on Tmux</PrimaryButton>
        <PrimaryButton onClick={handleRunInline}>
          Run Inline
        </PrimaryButton>
      </div>

      <div className="w-full flex justify-center mt-6">
        {plotUrl && <img src={plotUrl} alt={safeAction} />}
      </div>
    </div>
  )
}
