import { useState } from "react";
import Combobox from "@/components/ComboBox";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { trainModel } from "@/api/api";
import NumberInput from "@/components/IntegerInput";
import PrimaryButton from "@/components/PrimaryButton";

const datasets_options = [
  { value: "BCIC2a", label: "BCIC2a Dataset" },
  { value: "BCIC2b", label: "BCIC2b Dataset" },
  { value: "BNCI2015_001", label: "BNCI2015_001 Dataset" },
  { value: "SMR_BCI", label: "SMR_BCI Dataset" },
  { value: "HighGamma", label: "HighGamma Dataset" },
  { value: "OpenBMI", label: "OpenBMI Dataset" },
]

const model_options = [
  { value: "Mixnet", label: "MixNet" }
]

const Train = () => {
  const [trainingLog, setTrainingLog] = useState<string[]>([
    "[2025-03-22 10:00:00] Training started...",
    "[2025-03-22 10:00:02] Loaded dataset: dataset_name (50,000 samples)",
    "[2025-03-22 10:00:05] Model: ResNet-18, Batch Size: 32, Learning Rate: 0.001",
    "[2025-03-22 10:00:08] Epoch 1/50 - Loss: 2.3456 - Accuracy: 45.3%",
    "[2025-03-22 10:00:12] Epoch 2/50 - Loss: 1.8765 - Accuracy: 52.7%",
    "[2025-03-22 10:00:16] Epoch 3/50 - Loss: 1.4321 - Accuracy: 61.2%",
    "...",
    "[2025-03-22 10:05:30] Epoch 50/50 - Loss: 0.4567 - Accuracy: 89.5%",
    "[2025-03-22 10:05:32] Training complete! Total time: 5m 32s",
  ]);

  const [selectedDataset, setSelectedDataset] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [learningEpoch, setLearningEpoch] = useState(10);
  const [kFold, setKFold] = useState(5);

  const handleTrain = async () => {
    return await trainModel({
      model_name: selectedModel,
      dataset_name: selectedDataset,
      epochs: learningEpoch,
      kfolds: kFold,
    });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="space-y-6">
        <div>
          <Label className="text-purple-800 text-lg mb-2 block">Select dataset</Label>
          <Combobox options={datasets_options} value={selectedDataset} onChange={setSelectedDataset}/>
        </div>
        <div>
          <Label className="text-purple-800 text-lg mb-2 block">Select Model</Label>
          <Combobox options={model_options} value={selectedModel} onChange={setSelectedModel}/>
        </div>

        <div className="space-y-4">
          <Label className="text-purple-800 text-lg block">Configure Parameters</Label>
          <div className="flex flex-col gap-2">
            <div>
              <Label className="text-purple-800 py-2">Learning Epoch:</Label>
              <NumberInput value={learningEpoch} onChange={setLearningEpoch} />
            </div>
            <div>
              <Label className="text-purple-800 py-2">Set k-fold:</Label>
              <NumberInput value={kFold} onChange={setKFold} />
            </div>
          </div>
        </div>

        <div className="flex gap-4 pt-4">
          <PrimaryButton onClick={handleTrain}>
            Train
          </PrimaryButton>
          <Button variant="outline" className="border-2 border-purple-300 text-purple-900">Save Model</Button>
        </div>
      </div>

      <Card className="bg-purple-100 border-purple-300">
        <CardContent className="p-4">
          <h2 className="text-purple-800 text-lg font-semibold mb-2">Training Log</h2>
          <div className="text-sm text-purple-900 whitespace-pre-line font-mono max-h-[400px] overflow-y-auto">
            {trainingLog.join("\n")}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Train;