import React, { useState } from 'react';
import { Upload, Leaf, Activity, AlertCircle, CheckCircle } from 'lucide-react';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setIsAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      // Connect to your running Python Server
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Server error. Is the Python backend running?");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800">
      
      {/* Header */}
      <header className="bg-green-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex items-center space-x-3">
          <Leaf className="h-8 w-8" />
          <h1 className="text-2xl font-bold">AgroVision AI</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-10 max-w-4xl">
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* LEFT: Upload Section */}
          <div className="bg-white p-6 rounded-xl shadow-md border border-slate-100">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Upload className="w-5 h-5 mr-2 text-green-600" /> 
              Upload Plant Leaf
            </h2>

            {/* Drag & Drop Area */}
            <div className="relative border-2 border-dashed border-green-200 bg-green-50/30 rounded-xl h-64 flex flex-col items-center justify-center hover:bg-green-50 transition cursor-pointer">
              <input 
                type="file" 
                accept="image/*"
                onChange={handleImageChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              
              {preview ? (
                <img 
                  src={preview} 
                  alt="Preview" 
                  className="h-full w-full object-contain rounded-xl p-2" 
                />
              ) : (
                <div className="text-center p-4">
                  <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Leaf className="text-green-600 w-6 h-6" />
                  </div>
                  <p className="text-green-800 font-medium">Click to select Image</p>
                  <p className="text-sm text-green-600/70 mt-1">Supports JPG, PNG</p>
                </div>
              )}
            </div>

            <button
              onClick={analyzeImage}
              disabled={!selectedImage || isAnalyzing}
              className={`w-full mt-6 py-3 rounded-lg font-bold text-lg transition-all flex items-center justify-center
                ${!selectedImage 
                  ? 'bg-slate-200 text-slate-400 cursor-not-allowed' 
                  : isAnalyzing 
                    ? 'bg-green-800 text-green-100'
                    : 'bg-green-600 hover:bg-green-700 text-white shadow-lg hover:shadow-xl'
                }`}
            >
              {isAnalyzing ? (
                <>
                  <Activity className="animate-spin mr-2" /> Processing...
                </>
              ) : (
                "Analyze Disease"
              )}
            </button>

            {error && (
              <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center text-sm">
                <AlertCircle className="w-4 h-4 mr-2 flex-shrink-0" />
                {error}
              </div>
            )}
          </div>

          {/* RIGHT: Results Section */}
          <div className="space-y-6">
            {!result && (
              <div className="h-full flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl p-8 bg-slate-50/50">
                <Activity className="w-16 h-16 mb-4 opacity-20" />
                <p>Upload and analyze an image to see results here.</p>
              </div>
            )}

            {result && (
              <div className="bg-white rounded-xl shadow-lg border border-slate-100 overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
                {/* Result Header */}
                <div className={`p-6 ${result.status === 'healthy' ? 'bg-green-600' : 'bg-red-500'} text-white`}>
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="opacity-90 text-sm font-medium uppercase tracking-wider mb-1">Diagnosis</p>
                      <h3 className="text-3xl font-bold">{result.disease.replace(/_/g, ' ')}</h3>
                    </div>
                    {result.status === 'healthy' ? (
                      <CheckCircle className="w-10 h-10 opacity-80" />
                    ) : (
                      <AlertCircle className="w-10 h-10 opacity-80" />
                    )}
                  </div>
                </div>

                {/* Details */}
                <div className="p-6 space-y-6">
                  {/* Confidence Bar */}
                  <div>
                    <div className="flex justify-between text-sm font-medium mb-2">
                      <span className="text-slate-600">AI Confidence Score</span>
                      <span className="text-green-700">{(result.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-3">
                      <div 
                        className={`h-3 rounded-full ${result.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`} 
                        style={{ width: `${result.confidence * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Treatment Plan */}
                  <div className="bg-slate-50 p-5 rounded-xl border border-slate-200">
                    <h4 className="font-bold text-slate-800 mb-2 flex items-center">
                      📋 Recommended Action
                    </h4>
                    <p className="text-slate-600 leading-relaxed">
                      {result.treatment}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;