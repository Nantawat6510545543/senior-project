import { SubHeader } from "@/components/Fonts";
import NumberInput from "../NumberInput";


export default function PredictionTab() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <SubHeader>checkpoint_path</SubHeader>
        <NumberInput />
    </div>
  );
}
