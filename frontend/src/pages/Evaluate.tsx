import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { UploadCloud } from "lucide-react";
import { XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, ResponsiveContainer } from 'recharts';

const Evaluate = () => {
  const metrics = {
    accuracy: 87.6,
    precision: 88.2,
    recall: 90.5,
    f1: 0.875,
  };

  const data = Array.from({ length: 50 }, (_, i) => ({
    epoch: i + 1,
    loss: Math.max(0.05, 0.9 - i * 0.02 + Math.random() * 0.1),
    accuracy: Math.min(1, 0.5 + i * 0.01 + Math.random() * 0.05),
  }));

  return (
    <div className="flex justify-center p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center w-full max-w-7xl">
        <div className="flex flex-col items-center gap-4">
          <Button className="bg-purple-200 text-purple-900 border border-purple-300 shadow-md">
            <UploadCloud className="mr-2 h-5 w-5" /> Upload Model
          </Button>
          <div className="text-purple-900 space-y-1 text-lg text-center">
            <p>Accuracy: {metrics.accuracy}%</p>
            <p>Precision: {metrics.precision}%</p>
            <p>Recall: {metrics.recall}%</p>
            <p>F1 Score: {metrics.f1}</p>
          </div>
          <Button className="bg-purple-800 text-white px-6 py-2 rounded-md shadow hover:bg-purple-700">
            Evaluate
          </Button>
        </div>

        <Card className="bg-purple-100 border-purple-300 w-full">
          <CardContent className="p-4">
            <h2 className="text-purple-800 text-lg font-semibold mb-2 text-center">Visualization</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="epoch" label={{ value: "Epochs", position: "insideBottomRight", offset: 0 }} />
                <YAxis yAxisId="left" domain={[0, 1]} label={{ value: "Loss", angle: -90, position: "insideLeft" }} />
                <YAxis yAxisId="right" orientation="right" domain={[0.5, 1]} label={{ value: "Accuracy", angle: 90, position: "insideRight" }} />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="loss" stroke="red" name="Loss" />
                <Line yAxisId="right" type="monotone" dataKey="accuracy" stroke="blue" name="Accuracy" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Evaluate;
