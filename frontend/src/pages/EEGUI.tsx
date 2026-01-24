"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import NumberInput from "@/components/NumberInput"
import OptionButtons from "@/components/OptionsButton"
import Combobox from "@/components/ComboBox"
import { Header, SubHeader } from "@/components/Fonts"
import PurpleCheckbox from "@/components/PurpleCheckbox"
import SettingsTab from "@/components/TabRenderer"
import PrimaryButton from "@/components/PrimaryButton"
import { getPlotUrl } from "@/api/api"

const ACTION_TO_PLOT_TYPE: Record<string, string> = {
  "Sensor Layout": "sensor_layout",
  "Time Domain Plot": "time_domain",
  "Frequency Domain": "frequency_domain",
  "Epoch Plot": "epoch",
  "Evoked Plot": "evoked",
  "Evoked Topo Plot": "evoked_topo",
  "Evoked Plot Joint": "evoked_joint",
  "Evoked per Condition": "evoked_per_condition",
  "SNR Spectrum": "snr_spectrum",
};

export default function EEGUI() {
  const [inputType, setInputType] = useState("Single subject")
  const [mode, setMode] = useState("Plot")
  const [action, setAction] = useState("Sensor Layout")
  const [subject, setSubject] = useState("")
  const [task, setTask] = useState("")
  const [plotUrl, setPlotUrl] = useState<string | null>(null);

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

  const modeDescriptions: Record<string, string> = {
    Plot: "Produces one concise figure for the current EEG selection.",
    "Grid Plot":
      "Displays per-condition results in a labeled grid for side-by-side comparison with consistent axes and scaling.",
    Data:
      "Provides structured tables from the current selection for quick inspection and lightweight export (annotations, channels/electrodes, metadata, epoch summaries).",
    AI: "AI training and inference on epochs (registry-based).",
  }

  const handleRun = () => {
    setPlotUrl(
      getPlotUrl({
        type: ACTION_TO_PLOT_TYPE[action],
        subject,
        task,
      })
    );
  };

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
        <p className="text-sm text-muted-foreground max-w-3xl">
          {modeDescriptions[mode]}
        </p>
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

      <SettingsTab action={action} />

      {/* Run */}
      <div className="flex gap-4">
        <PrimaryButton>Run on Tmux</PrimaryButton>
        <PrimaryButton onClick={handleRun}>Run Inline</PrimaryButton>
        {plotUrl && <img src={plotUrl} alt={action} />}
      </div>
    </div>
  )
}
