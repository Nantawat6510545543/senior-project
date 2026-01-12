import { useState } from "react";
import { SubHeader } from "@/components/Fonts";
import NumberInput from "@/components/NumberInput";
import Combobox from "../ComboBox";


export default function TrainingTab() {
  const [batchSize, setBatchSize] = useState<number | undefined>();
  const [epochs, setEpochs] = useState<number | undefined>();
  const [lr, setLr] = useState<number | undefined>();
  const [device, setDevice] = useState("");
  const [target, setTarget] = useState("");

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <div>
        <SubHeader>batch_size</SubHeader>
        <NumberInput value={batchSize} onChange={(val) => setBatchSize(val)} />
      </div>

      <div>
        <SubHeader>epochs_n</SubHeader>
        <NumberInput value={epochs} onChange={(val) => setEpochs(val)} />
      </div>

      <div>
        <SubHeader>lr</SubHeader>
        <NumberInput value={lr} onChange={(val) => setLr(val)} />
      </div>

      <div>
        <SubHeader>device</SubHeader>
        <Combobox
          options={[
            { value: "auto", label: "auto" },
            { value: "cpu", label: "cpu" },
            { value: "cuda", label: "cuda" },
          ]}
          value={device}
          onChange={setDevice}
        />
      </div>

      <div>
        <SubHeader>target</SubHeader>
        <Combobox
          options={[{ value: "stimulus", label: "stimulus" }]}
          value={target}
          onChange={setTarget}
        />
      </div>
    </div>
  );
}
