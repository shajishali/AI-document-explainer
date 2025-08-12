import React, { useState, useCallback } from 'react';
import { Upload, FileText, X, AlertCircle, CheckCircle } from 'lucide-react';
import { useDropzone } from 'react-dropzone';

const DocumentUploader = ({ onFileSelect, onTextInput, isLoading = false }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'text'

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const handleFileRemove = () => {
    setSelectedFile(null);
    onFileSelect(null);
  };

  const handleTextSubmit = () => {
    if (textInput.trim()) {
      onTextInput(textInput.trim());
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (tab === 'upload') {
      setTextInput('');
    } else {
      setSelectedFile(null);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-legal-100 p-1 rounded-lg mb-6">
        <button
          onClick={() => handleTabChange('upload')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200 ${
            activeTab === 'upload'
              ? 'bg-white text-primary-700 shadow-sm'
              : 'text-legal-600 hover:text-legal-900'
          }`}
        >
          <Upload className="w-4 h-4 inline mr-2" />
          Upload Document
        </button>
        <button
          onClick={() => handleTabChange('text')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors duration-200 ${
            activeTab === 'text'
              ? 'bg-white text-primary-700 shadow-sm'
              : 'text-legal-600 hover:text-legal-900'
          }`}
        >
          <FileText className="w-4 h-4 inline mr-2" />
          Paste Text
        </button>
      </div>

      {/* Upload Tab */}
      {activeTab === 'upload' && (
        <div className="space-y-6">
          {/* Drop Zone */}
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer ${
              isDragActive
                ? 'border-primary-400 bg-primary-50'
                : isDragReject
                ? 'border-red-400 bg-red-50'
                : 'border-legal-300 hover:border-primary-400 hover:bg-primary-50'
            }`}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-legal-100 rounded-full flex items-center justify-center">
                <Upload className="w-8 h-8 text-legal-400" />
              </div>
              <div>
                <p className="text-lg font-medium text-legal-900">
                  {isDragActive
                    ? 'Drop your document here'
                    : 'Drag & drop your document here'}
                </p>
                <p className="text-legal-600 mt-2">
                  or click to browse files
                </p>
              </div>
              <div className="text-sm text-legal-500">
                <p>Supported formats: PDF, DOC, DOCX, TXT</p>
                <p>Maximum size: 10MB</p>
              </div>
            </div>
          </div>

          {/* Selected File Display */}
          {selectedFile && (
            <div className="bg-white rounded-lg border border-legal-200 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <p className="font-medium text-legal-900">{selectedFile.name}</p>
                    <p className="text-sm text-legal-500">
                      {formatFileSize(selectedFile.size)} • {selectedFile.type}
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleFileRemove}
                  className="p-2 text-legal-400 hover:text-legal-600 hover:bg-legal-100 rounded-lg transition-colors duration-200"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* Upload Button */}
          {selectedFile && (
            <button
              onClick={() => onFileSelect(selectedFile)}
              disabled={isLoading}
              className="w-full btn-primary py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="loading-spinner w-5 h-5 mr-3"></div>
                  Analyzing Document...
                </div>
              ) : (
                'Analyze Document'
              )}
            </button>
          )}
        </div>
      )}

      {/* Text Input Tab */}
      {activeTab === 'text' && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg border border-legal-200 p-6">
            <label htmlFor="text-input" className="block text-sm font-medium text-legal-700 mb-3">
              Paste your legal document text here
            </label>
            <textarea
              id="text-input"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Paste your legal document text here...\n\nExample:\nThis agreement is entered into between...\nThe contractor shall provide services...\nIn case of breach, penalties may apply..."
              className="input-field h-64 resize-none"
              disabled={isLoading}
            />
            <div className="mt-3 flex items-center justify-between">
              <p className="text-sm text-legal-500">
                {textInput.length} characters
              </p>
              <button
                onClick={handleTextSubmit}
                disabled={!textInput.trim() || isLoading}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="loading-spinner w-4 h-4 mr-2"></div>
                    Analyzing...
                  </div>
                ) : (
                  'Analyze Text'
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <CheckCircle className="h-5 w-5 text-blue-400" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-800">
              How it works
            </h3>
            <div className="mt-2 text-sm text-blue-700">
              <p>1. Upload a document or paste text content</p>
              <p>2. Our AI analyzes the document for legal clauses and risks</p>
              <p>3. Get detailed insights with highlighted sections and recommendations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUploader;
