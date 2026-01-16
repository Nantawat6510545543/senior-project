import { Input } from "@/components/ui/input";

interface NumberInputProps {
  value?: number;
  placeholder?: string;
  onChange: (value: number) => void;
}

const NumberInput = ({ value, placeholder, onChange }: NumberInputProps) => (
  <div>
    <Input
      type="number"
      className="bg-purple-200 border-purple-300 text-purple-900 !text-base"
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  </div>
);

export default NumberInput;