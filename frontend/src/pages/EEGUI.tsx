"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import ApiButton from "@/components/ApiButton"
import NumberInput from "@/components/NumberInput"
import OptionButtons from "@/components/OptionsButton"
import Combobox from "@/components/ComboBox"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import FilteringCleaningTabs from "@/components/FilteringCleaningTabs"

export default function EEGUI() {
  const [inputType, setInputType] = useState("Single subject")
  const [mode, setMode] = useState("Plot")
  const [action, setAction] = useState("Sensor Layout")
  const [subject, setSubject] = useState("")
  const [task, setTask] = useState("")

  const subjectOptions = [
    { value: "sub-NDARAC904DMU", label: "sub-NDARAC904DMU" },
    { value: "sub-NDARAC111AAA", label: "sub-NDARAC111AAA" },
  ]

  const taskOptions = [
    { value: "DespicableMe", label: "DespicableMe" },
    { value: "RestingState", label: "Resting State" },
  ]

  // Define actions depending on mode
  const modeActions = {
    Plot: [
      "Sensor Layout",
      "Time Domain Plot",
      "Frequency Domain",
      "Epoch Plot",
      "Evoked Plot",
      "Evoked Topo Plot",
      "Evoked Plot Joint",
      "Evoked per Condition",
      "SNR Spectrum",
    ],
    "Grid Plot": ["PSD Grid", "SNR Grid", "Evoked Grid"],
    Data: ["EEG Table", "Epochs Table", "Metadata"],
    AI: ["Models", "Build Dataset", "Train", "Predict"],
  }

  // Update action automatically if mode changes
  useEffect(() => {
    const actions = modeActions[mode]
    if (!actions.includes(action)) {
      setAction(actions[0])
    }
  }, [mode])

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

        {/* Single Subject Fields */}
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

        {/* Meta Filter Fields */}
        {inputType === "Meta filter (group)" && (
          <div className="space-y-4 mt-4">
            <SubHeader>Task</SubHeader>
            <Combobox options={taskOptions} value={task} onChange={setTask} />

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
            ].map((name) => (
              <div key={name}>
                <SubHeader>{name}_range</SubHeader>
                <div className="flex gap-2">
                  <NumberInput placeholder="min" />
                  <NumberInput placeholder="max" />
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Mode */}
      <Card className="p-4">
        <Header>Select Mode</Header>
        <OptionButtons
          options={["Plot", "Grid Plot", "Data", "AI"]}
          value={mode}
          onChange={setMode}
        />
      </Card>

      {/* Action */}
      <Card className="p-4 space-y-3">
        <Header>Select Action:</Header>
        <OptionButtons
          options={modeActions[mode]}
          value={action}
          onChange={setAction}
        />

        <div className="flex items-center gap-2">
          <PurpleCheckbox />
          <SubHeader>Show all groups</SubHeader>
        </div>
      </Card>

      {mode !== "AI" && <FilteringCleaningTabs />}

      {/* Run */}
      <div className="flex gap-4">
        <ApiButton label="Run on Tmux" />
        <ApiButton label="Run Inline" />
      </div>
    </div>
  )
}
