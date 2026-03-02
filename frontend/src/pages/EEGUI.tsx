"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import OptionButtons from "@/components/OptionsButton"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import SettingsTab from "@/components/TabRenderer"
import PrimaryButton from "@/components/PrimaryButton"
import { createSession, getPlotUrl } from "@/api/api"
import { SETTINGS_MODE } from "./settings_mode"
import LogPanel from "@/components/LogPanel"

import TaskForm from "@/components/forms/TaskForm"
import CohortTaskForm from "@/components/forms/CohortTaskForm"
import useSessionPatch from "@/hooks/useSessionPatch"


export default function EEGUI() {
  const [subjectType, setSubjectType] = useState("Single subject")
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

  const backendSubjectType =
    subjectType === "Single subject" ? "single" : "cohort"

  useSessionPatch(sessionId, "subject_type", backendSubjectType)

  let safeAction = action
  if (!(safeAction in modeData.actions)) {
    safeAction = actions[0]
  }

  function handleRunInline() {
    if (!sessionId) return
    const plotType = modeData.actions[safeAction]
    setPlotUrl(getPlotUrl(sessionId, plotType))
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Input Type */}
      <Card className="p-4">
        <Header>Input Type:</Header>
        <OptionButtons
          options={["Single subject", "Meta filter (group)"]}
          value={subjectType}
          onChange={setSubjectType}
        />

        {subjectType === "Single subject" && (
          <TaskForm sessionId={sessionId} />
        )}

        {subjectType === "Meta filter (group)" && (
          <CohortTaskForm sessionId={sessionId} />
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

      <LogPanel sessionId={sessionId} />

      <div className="w-full flex justify-center mt-6">
        {plotUrl && <img src={plotUrl} alt={safeAction} />}
      </div>
    </div>
  )
}
