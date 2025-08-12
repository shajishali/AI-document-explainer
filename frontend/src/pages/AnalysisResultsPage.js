import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { FileText, ArrowLeft } from 'lucide-react';

const AnalysisResultsPage = () => {
  const location = useLocation();
  const { analysisResults, fileName } = location.state || {};

  if (!analysisResults) {
    return (
      <div className="min-h-screen bg-legal-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-12">
            <FileText className="w-16 h-16 text-legal-400 mx-auto mb-6" />
            <h1 className="text-2xl font-bold text-legal-900 mb-4">
              No Analysis Results Found
            </h1>
            <p className="text-legal-600 mb-8">
              Please analyze a document first to see the results.
            </p>
            <Link
              to="/analyze"
              className="btn-primary inline-flex items-center"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Analysis
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-legal-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/analyze"
            className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Analysis
          </Link>
          <h1 className="text-3xl font-bold text-legal-900 mb-2">
            Analysis Results
          </h1>
          <p className="text-legal-600">
            Document: {fileName}
          </p>
        </div>

        {/* Results Content - Placeholder */}
        <div className="bg-white rounded-xl shadow-legal border border-legal-200 p-8">
          <div className="text-center">
            <FileText className="w-16 h-16 text-legal-400 mx-auto mb-6" />
            <h2 className="text-xl font-semibold text-legal-900 mb-4">
              Analysis Results Coming Soon
            </h2>
            <p className="text-legal-600">
              This page will display comprehensive analysis results including:
            </p>
            <ul className="text-legal-600 mt-4 space-y-2">
              <li>• Document summary and key findings</li>
              <li>• Risk assessment and classification</li>
              <li>• Detected legal clauses</li>
              <li>• Interactive visualizations</li>
              <li>• Actionable recommendations</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResultsPage;
