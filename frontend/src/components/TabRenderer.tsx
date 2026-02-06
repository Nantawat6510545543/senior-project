import EpochsTab from "@/components/tabs/EpochsTab"
import EvokedDisplayTab from "@/components/tabs/EvokedDisplayTab"
import FilteringCleaningTab from "@/components/tabs/FilteringCleaningTab"
import PSDTab from "@/components/tabs/PSDTab"
import TimeDomainTab from "@/components/tabs/TimeDomainTab"
import TopomapTab from "@/components/tabs/TopomapTab"
import { Card } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import TablesTab from "./tabs/TablesTab"
import ModelsTab from "./tabs/ModelsTab"
import TrainingTab from "./tabs/TrainingTab"
import PredictionTab from "./tabs/PredictionTab"
import { useEffect, useState, type ReactNode } from "react"
import { useSchema, type SchemaEndpoints } from "@/hooks/useSchema"

// -----------------------------
// Which action needs which tabs
// -----------------------------
const tabDependencies: Record<string, string[]> = {
  "Sensor Layout": ["Filtering and Cleaning"],
  "Time Domain Plot": ["Filtering and Cleaning", "Time Domain"],
  "Frequency Domain": ["Filtering and Cleaning", "Epochs", "PSD"],
  "Epoch Plot": ["Filtering and Cleaning", "Epochs"],
  "Evoked Plot": ["Filtering and Cleaning", "Epochs", "Evoked Display"],
  "Evoked Topo Plot": ["Filtering and Cleaning", "Evoked Display", "Topomap"],
  "Evoked Plot Joint": ["Filtering and Cleaning", "Epochs", "Topomap", "Evoked Display"],
  "Evoked per Condition": ["Filtering and Cleaning", "Epochs", "Evoked Display"],
  "SNR Spectrum": ["Filtering and Cleaning", "Epochs", "PSD"],

  "PSD Grid": ["Filtering and Cleaning", "Epochs", "PSD"],
  "SNR Grid": ["Filtering and Cleaning", "Epochs", "PSD"],
  "Evoked Grid": ["Filtering and Cleaning", "Epochs", "Evoked Display"],

  "EEG Table": ["Filtering and Cleaning", "Tables"],
  "Epochs Table": ["Filtering and Cleaning", "Epochs"],
  "Metadata": [],

  "Models": [],
  "Build Dataset": ["Filtering and Cleaning", "Epochs", "Models", "Training"],
  "Train": ["Filtering and Cleaning", "Epochs", "Models", "Training"],
  "Predict": ["Filtering and Cleaning", "Epochs", "Models", "Prediction"]
}


// ----------------------------------------
// Map tab → backend schema endpoint name
// ----------------------------------------
const tabToSchemaEndpoint: Record<string, SchemaEndpoints> = {
  "Filtering and Cleaning": "filter",
  "Time Domain": "time",
  "Epochs": "epochs",
  "PSD": "psd",
  "Evoked Display": "evoked",
  "Topomap": "topomap",
  "Tables": "tables",
  "Models": "models",
  "Training": "training",
  "Prediction": "prediction",
}


// -----------------------------
// Tab component registry
// -----------------------------
const tabComponents: Record<string, (sessionId: string, schema: any) => ReactNode> = {
  "Filtering and Cleaning": (sid, schema) => <FilteringCleaningTab sessionId={sid} schema={schema} />,
  "Time Domain": (sid, schema) => <TimeDomainTab sessionId={sid} schema={schema} />,
  "Epochs": (sid, schema) => <EpochsTab sessionId={sid} schema={schema} />,
  "PSD": (sid, schema) => <PSDTab sessionId={sid} schema={schema} />,
  "Evoked Display": (sid, schema) => <EvokedDisplayTab sessionId={sid} schema={schema} />,
  "Topomap": (sid, schema) => <TopomapTab sessionId={sid} schema={schema} />,
  "Tables": (sid, schema) => <TablesTab sessionId={sid} schema={schema} />,
  "Models": (sid, schema) => <ModelsTab sessionId={sid} schema={schema} />,
  "Training": (sid, schema) => <TrainingTab sessionId={sid} schema={schema} />,
  "Prediction": (sid, schema) => <PredictionTab sessionId={sid} schema={schema} />,
}

export default function SettingsTab({ action, sessionId }: {
  action: string, sessionId: string }
) {
  const requiredTabs = tabDependencies[action] || []
  const [activeTab, setActiveTab] = useState(requiredTabs[0])

  const endpoint = tabToSchemaEndpoint[activeTab]
  const schema = useSchema(endpoint)

  useEffect(() => {
    setActiveTab(requiredTabs[0])
  }, [action])

  if (requiredTabs.length === 0) return null

  return (
    <Card className="p-4 space-y-4 bg-white border border-purple-300">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="w-full bg-purple-100 border-0 rounded-md">
          {requiredTabs.map((tabName) => (
            <TabsTrigger
              key={tabName}
              value={tabName}
              className="text-purple-900 text-lg py-3 px-4
                data-[state=active]:bg-purple-800 
                data-[state=active]:text-white 
                hover:bg-purple-300"
            >
              {tabName}
            </TabsTrigger>
          ))}
        </TabsList>

        {requiredTabs.map((tabName) => (
          <TabsContent
            key={tabName}
            value={tabName}
            className="bg-white text-purple-900 p-4"
          >
            {tabComponents[tabName]?.(sessionId, schema)}
          </TabsContent>
        ))}
      </Tabs>
    </Card>
  )
}