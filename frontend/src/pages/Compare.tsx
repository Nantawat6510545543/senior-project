import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { UploadCloud } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import ApiButton from "@/components/PrimaryButton";
import { compareModel } from "@/api/api";

const Compare = () => { 
  const compareData = [
    {
      name: 'SSL Model',
      Accuracy: 87.6,
      Precision: 88.2,
      Recall: 87.0,
      'F1 Score': 87.5,
    },
    {
      name: 'Supervised Model',
      Accuracy: 91.2,
      Precision: 92.0,
      Recall: 90.3,
      'F1 Score': 91.5,
    },
  ];

  const model1 = {
    accuracy: '87.6%',
    precision: '88.2%',
    recall: '90.5%',
    f1Score: '0.875'
  };

  const model2 = {
    accuracy: '91.2%',
    precision: '92.0%',
    recall: '86.9%',
    f1Score: '0.915'
  };

  const handleCompare = () => {
    console.log("Predicting with file:");
  }

  return (
    <div className="flex justify-center p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center w-full max-w-7xl">
        
        {/* Left sidebar with model info */}
        <div className="flex flex-col items-center gap-4">
          <Button className="bg-purple-200 text-purple-900 border border-purple-300 shadow-md">
            <UploadCloud className="mr-2 h-5 w-5" /> Upload Model 1
          </Button>
          <div className="text-purple-900 space-y-1 text-lg text-center">
            <h3 className="text-lg font-semibold">Model 1:</h3>
            <p>Accuracy: {model1.accuracy}</p>
            <p>Precision: {model1.precision}</p>
            <p>Recall: {model1.recall}</p>
            <p>F1 Score: {model1.f1Score}</p>
          </div>

          <Button className="bg-purple-200 text-purple-900 border border-purple-300 shadow-md">
            <UploadCloud className="mr-2 h-5 w-5" /> Upload Model 2
          </Button>
          <div className="text-purple-900 space-y-1 text-lg text-center">
            <h3 className="text-lg font-semibold">Model 2:</h3>
            <p>Accuracy: {model2.accuracy}</p>
            <p>Precision: {model2.precision}</p>
            <p>Recall: {model2.recall}</p>
            <p>F1 Score: {model2.f1Score}</p>
          </div>

            <ApiButton onClickApi={handleCompare} label="Compare" />
        </div>

        {/* Chart area */}
        <Card className="bg-purple-100 border-purple-300 w-full">
          <CardContent className="p-4">
            <h2 className="text-purple-800 text-lg font-semibold mb-2 text-center">Comparison Visualization</h2>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                data={compareData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis 
                  label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
                  domain={[80, 94]}
                />
                <Tooltip />
                <Legend />
                <Bar dataKey="Accuracy" fill="#F9C74F" />
                <Bar dataKey="Precision" fill="#F3722C" />
                <Bar dataKey="Recall" fill="#F94144" />
                <Bar dataKey="F1 Score" fill="#F15BB5" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default Compare;
