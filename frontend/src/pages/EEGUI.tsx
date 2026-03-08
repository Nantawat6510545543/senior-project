"use client"

import { useState } from "react"
import { useFormContext } from "react-hook-form"

import { Card } from "@/components/ui/card"
import OptionButtons from "@/components/OptionsButton"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import SettingsTab from "@/components/TabRenderer"
import PrimaryButton from "@/components/PrimaryButton"
import { fetchTableData, getPlotUrl } from "@/api/api"
import { SETTINGS_MODE } from "./settings_mode"
import LogPanel from "@/components/LogPanel"
import TaskForm from "@/components/forms/TaskForm"
import CohortTaskForm from "@/components/forms/CohortTaskForm"
import PurpleTable from "@/components/PurpleTable"
import type { SessionFormSchema } from "@/api/types"


export default function EEGUI() {
  const [mode, setMode] = useState<keyof typeof SETTINGS_MODE>("Plot")
  const [action, setAction] = useState(
    Object.keys(SETTINGS_MODE.Plot.actions)[0]
  )

  const modeData = SETTINGS_MODE[mode]
  const actions = Object.keys(modeData.actions)

  // TODO resolve
  const TABLE_VIEWS = ["eeg_table", "epochs_table", "metadata"]
  const [tableData, setTableData] = useState<any>(null)
  const [plotUrl, setPlotUrl] = useState<string | null>(null)
  const [runId] = useState(() =>
    crypto.randomUUID().replace(/-/g, "").slice(0, 8)
  )

  const { watch, setValue, getValues } = useFormContext<SessionFormSchema>()
  const subjectType = watch("subject_type")

  let safeAction = action
  if (!(safeAction in modeData.actions)) {
    safeAction = actions[0]
  }

  // TODO resolve
  async function handleRunInline() {
    const session = getValues()
    console.log("Session", session)

    const view = modeData.actions[safeAction]

    if (TABLE_VIEWS.includes(view)) {
      const json = await fetchTableData(session, view, runId)
      setTableData(json)
      setPlotUrl(null)
    } else {
      const url = await getPlotUrl(session, view, runId)
      setPlotUrl(url)
      setTableData(null)
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Input Type */}
      <Card className="p-4">
        <Header>Input Type:</Header>
        <OptionButtons
          options={["Single subject", "Meta filter (group)"]}
          value={subjectType === "single" ? "Single subject" : "Meta filter (group)"}
          onChange={(v) =>
            setValue(
              "subject_type",
              v === "Single subject" ? "single" : "cohort"
            )
          }
        />

        {subjectType === "single" && <TaskForm />}
        {subjectType === "cohort" && <CohortTaskForm />}
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

      {/* Schema Parameters Tabs */}
      <SettingsTab action={safeAction}/>

      {/* Run */}
      <PrimaryButton onClick={handleRunInline}>
        Run Inline
      </PrimaryButton>

      <LogPanel runId={runId} />

      <div className="w-full flex justify-center mt-6">
        {plotUrl && (
          <img src={plotUrl} alt={safeAction} />
        )}

        {tableData && (
          <PurpleTable data={tableData} />
        )}
      </div>
    </div>
  )
}
