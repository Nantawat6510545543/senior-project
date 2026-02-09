"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import OptionButtons from "@/components/OptionsButton"
import Combobox from "@/components/ComboBox"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import SettingsTab from "@/components/TabRenderer"
import PrimaryButton from "@/components/PrimaryButton"
import { createSession, getPlotUrl } from "@/api/api"
import { SETTINGS_MODE } from "./settings_mode"
import { useSubjectOption } from "@/hooks/useSubjectOption"
import { useTaskOption } from "@/hooks/useTaskOption"
import IntegerInput from "@/components/IntegerInput"
import type { SingleSubjectTask } from "@/api/types"
import useSessionPatch from "@/hooks/useSessionPatch"


export default function EEGUI() {
  const [inputType, setInputType] = useState("Single subject")
  const [mode, setMode] = useState<keyof typeof SETTINGS_MODE>("Plot")
  const [action, setAction] = useState(
    Object.keys(SETTINGS_MODE.Plot.actions)[0]
  )

  const modeData = SETTINGS_MODE[mode]
  const actions = Object.keys(modeData.actions)

  const [plotUrl, setPlotUrl] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string>("")

  useEffect(() => {
    createSession().then(setSessionId).catch(console.error)
  }, [])

  const [singleTask, setSingleTask] = useState<SingleSubjectTask>({
    subject: "",
    task: "",
    run: null,
  })

  let safeAction = action
  if (!(safeAction in modeData.actions)) {
    safeAction = actions[0]
  }

  useSessionPatch(sessionId, "task", singleTask)

  function handleRunInline() {
    if (!sessionId) return
    const plotType = modeData.actions[safeAction]
    setPlotUrl(getPlotUrl(sessionId, plotType))
  }

  const subjectOptions = useSubjectOption()
  const taskOptions = useTaskOption(singleTask.subject)

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
                value={singleTask.subject}
                onChange={(value) =>
                  setSingleTask((prev) => ({ ...prev, subject: value }))
                }
              />
            </div>

            <div>
              <SubHeader>Task</SubHeader>
              <Combobox
                options={taskOptions}
                value={singleTask.task}
                onChange={(value) =>
                  setSingleTask((prev) => ({ ...prev, task: value }))
                }
              />
            </div>
          </div>
        )}

        {inputType === "Meta filter (group)" && (
          <div className="space-y-4 mt-4">
            <SubHeader>Task</SubHeader>
              <Combobox
                options={subjectOptions}
                value={singleTask.subject}
                onChange={(value) =>
                  setSingleTask((prev) => ({ ...prev, subject: value }))
                }
              />

            <SubHeader>Subject limit</SubHeader>
            <IntegerInput />

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
                    <IntegerInput placeholder="min" />
                    <IntegerInput placeholder="max" />
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

      {/* Schema Settings Tabs */}
      <SettingsTab action={safeAction} sessionId={sessionId} />

      {/* Run */}
      <PrimaryButton onClick={handleRunInline}>
        Run Inline
      </PrimaryButton>

      <div className="w-full flex justify-center mt-6">
        {plotUrl && <img src={plotUrl} alt={safeAction} />}
      </div>
    </div>
  )
}
