import { Input } from "@/components/ui/input";

interface NumberInputProps {
  value: number;
  onChange: (value: number) => void;
}

const NumberInput = ({ value, onChange }: NumberInputProps) => (
  <div>
    <Input
      type="number"
      className="bg-purple-200 border-purple-300"
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  </div>
);

export default NumberInput;