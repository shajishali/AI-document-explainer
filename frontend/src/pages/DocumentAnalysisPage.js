import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import DocumentUploader from '../components/DocumentUploader';
import toast from 'react-hot-toast';

const DocumentAnalysisPage = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const navigate = useNavigate();

  const handleFileAnalysis = async (file) => {
    if (!file) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);

    try {
      // Simulate analysis progress
      const progressInterval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', file);

      // Make API call to backend
      const response = await fetch('/api/analyze-document', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setAnalysisProgress(100);

      if (response.ok) {
        const result = await response.json();
        toast.success('Document analysis completed successfully!');
        
        // Navigate to results page with data
        navigate('/results', { 
          state: { 
            analysisResults: result,
            fileName: file.name 
          } 
        });
      } else {
        throw new Error('Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Document analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
      setAnalysisProgress(0);
    }
  };

  const handleTextAnalysis = async (text) => {
    if (!text.trim()) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);

    try {
      // Simulate analysis progress
      const progressInterval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 15;
        });
      }, 150);

      // Make API call to backend for text analysis
      const response = await fetch('/api/analyze-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      clearInterval(progressInterval);
      setAnalysisProgress(100);

      if (response.ok) {
        const result = await response.json();
        toast.success('Text analysis completed successfully!');
        
        // Navigate to results page with data
        navigate('/results', { 
          state: { 
            analysisResults: result,
            fileName: 'Text Analysis' 
          } 
        });
      } else {
        throw new Error('Analysis failed');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Text analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
      setAnalysisProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-legal-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-legal-900 mb-6">
            Document Analysis
          </h1>
          <p className="text-xl text-legal-600 max-w-3xl mx-auto">
            Upload your legal document or paste text content to get AI-powered analysis, 
            risk assessment, and actionable insights.
          </p>
        </div>

        {/* Analysis Progress */}
        {isAnalyzing && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-6">
              <div className="flex items-center mb-4">
                <Clock className="w-6 h-6 text-primary-600 mr-3" />
                <h3 className="text-lg font-semibold text-legal-900">
                  Analyzing Document...
                </h3>
              </div>
              
              <div className="space-y-4">
                <div className="w-full bg-legal-200 rounded-full h-3">
                  <div 
                    className="bg-primary-600 h-3 rounded-full transition-all duration-300 ease-out"
                    style={{ width: `${analysisProgress}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between text-sm text-legal-600">
                  <span>Processing...</span>
                  <span>{analysisProgress}%</span>
                </div>

                <div className="text-sm text-legal-500">
                  <p>• Extracting text and identifying clauses</p>
                  <p>• Assessing risk levels and categories</p>
                  <p>• Generating recommendations and highlights</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Document Uploader */}
        <DocumentUploader
          onFileSelect={handleFileAnalysis}
          onTextInput={handleTextAnalysis}
          isLoading={isAnalyzing}
        />

        {/* Features Overview */}
        <div className="mt-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-legal-900 mb-4">
              What You'll Get
            </h2>
            <p className="text-lg text-legal-600">
              Comprehensive analysis results with actionable insights
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-legal-900 mb-2">
                Clause Detection
              </h3>
              <p className="text-legal-600">
                Identify and categorize legal clauses with confidence scores and importance levels.
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <AlertCircle className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-legal-900 mb-2">
                Risk Assessment
              </h3>
              <p className="text-legal-600">
                Multi-level risk classification with detailed breakdowns and mitigation strategies.
              </p>
            </div>

            <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-6">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-legal-900 mb-2">
                Actionable Insights
              </h3>
              <p className="text-legal-600">
                Clear recommendations and highlighted sections for easy navigation and understanding.
              </p>
            </div>
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-20 bg-blue-50 border border-blue-200 rounded-xl p-8">
          <div className="text-center">
            <h3 className="text-2xl font-bold text-blue-900 mb-4">
              Why Choose Our AI Analysis?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">⚡</span>
                </div>
                <h4 className="font-semibold text-blue-900 mb-2">Fast Processing</h4>
                <p className="text-blue-700 text-sm">
                  Get results in seconds, not hours
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">🎯</span>
                </div>
                <h4 className="font-semibold text-blue-900 mb-2">High Accuracy</h4>
                <p className="text-blue-700 text-sm">
                  95%+ accuracy in clause detection
                </p>
              </div>
              
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">🔒</span>
                </div>
                <h4 className="font-semibold text-blue-900 mb-2">Secure & Private</h4>
                <p className="text-blue-700 text-sm">
                  Your documents are never stored permanently
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentAnalysisPage;
