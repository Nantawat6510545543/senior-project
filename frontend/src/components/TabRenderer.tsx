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


// Mapping: full action name → required tab names
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

// Mapping: tab name → React component
const tabComponents: Record<string, React.ReactNode> = {
  "Filtering and Cleaning": <FilteringCleaningTab />,
  "Time Domain": <TimeDomainTab />,
  "Epochs": <EpochsTab />,
  "PSD": <PSDTab />,
  "Evoked Display": <EvokedDisplayTab />,
  "Topomap": <TopomapTab />,
  "Tables": <TablesTab />,
  "Models": <ModelsTab />,
  "Training": <TrainingTab />,
  "Prediction": <PredictionTab />
}

export default function SettingsTab({ action }: { action: string }) {
  const requiredTabs = tabDependencies[action] || []

  if (requiredTabs.length === 0) return null

  return (
    <Card className="p-4 space-y-4 bg-white border border-purple-300">
      <Tabs defaultValue={requiredTabs[0]}>
        <TabsList className="bg-purple-100 border border-purple-300 rounded-md">
          {requiredTabs.map((tabName) => (
            <TabsTrigger
              key={tabName}
              value={tabName}
              className="text-purple-900 data-[state=active]:bg-purple-800 data-[state=active]:text-white text-lg py-3 px-4"
            >
              {tabName}
            </TabsTrigger>
          ))}
        </TabsList>

        {requiredTabs.map((tabName) => (
          <TabsContent
            key={tabName}
            value={tabName}
            className="bg-white text-purple-900 p-4 border border-t-0 border-purple-800 rounded-b-md"
          >
            {tabComponents[tabName]}
          </TabsContent>
        ))}
      </Tabs>
    </Card>
  )
}

