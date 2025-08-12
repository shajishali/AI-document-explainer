import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Shield, 
  BarChart3, 
  Zap, 
  CheckCircle, 
  ArrowRight,
  Users,
  Clock,
  Award
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: FileText,
      title: 'Advanced Document Analysis',
      description: 'AI-powered analysis of legal documents with clause detection and risk assessment.',
      color: 'text-blue-600'
    },
    {
      icon: Shield,
      title: 'Risk Classification',
      description: 'Multi-level risk assessment with actionable recommendations and mitigation strategies.',
      color: 'text-green-600'
    },
    {
      icon: BarChart3,
      title: 'Visual Insights',
      description: 'Interactive charts and highlighted document sections for better understanding.',
      color: 'text-purple-600'
    },
    {
      icon: Zap,
      title: 'Fast Processing',
      description: 'Quick analysis with results in seconds, not hours.',
      color: 'text-orange-600'
    }
  ];

  const stats = [
    { label: 'Documents Analyzed', value: '10,000+', icon: FileText },
    { label: 'Risk Categories', value: '15+', icon: Shield },
    { label: 'Processing Time', value: '<5s', icon: Clock },
    { label: 'Accuracy Rate', value: '95%', icon: Award }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-legal-50 py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-8">
            <div className="inline-flex items-center px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium mb-6">
              <span className="w-2 h-2 bg-primary-600 rounded-full mr-2"></span>
              Phase 3 Complete - Modern Web Interface
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-legal-900 mb-6 leading-tight">
              AI-Powered
              <span className="text-primary-600 block">Legal Document</span>
              Analysis & Risk Assessment
            </h1>
            <p className="text-xl text-legal-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              Transform complex legal documents into clear insights. Our AI identifies clauses, 
              assesses risks, and provides actionable recommendations in seconds.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/analyze"
                className="btn-primary text-lg px-8 py-4 inline-flex items-center justify-center"
              >
                Start Analyzing
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/about"
                className="btn-secondary text-lg px-8 py-4"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Powerful Features for Legal Professionals
            </h2>
            <p className="text-xl text-legal-600 max-w-2xl mx-auto">
              Everything you need to analyze legal documents efficiently and accurately
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="text-center group">
                  <div className="w-16 h-16 bg-legal-100 rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-100 transition-colors duration-200">
                    <Icon className={`w-8 h-8 ${feature.color}`} />
                  </div>
                  <h3 className="text-lg font-semibold text-legal-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-legal-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-legal-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Trusted by Legal Professionals
            </h2>
            <p className="text-xl text-legal-600">
              Our platform delivers results that matter
            </p>
          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center mx-auto mb-4 shadow-legal">
                    <Icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <div className="text-3xl font-bold text-legal-900 mb-2">
                    {stat.value}
                  </div>
                  <div className="text-legal-600">
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Legal Document Analysis?
          </h2>
          <p className="text-xl text-primary-100 mb-8 leading-relaxed">
            Join thousands of legal professionals who trust our AI-powered platform 
            for accurate, fast, and comprehensive document analysis.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/analyze"
              className="bg-white text-primary-600 hover:bg-gray-50 font-semibold py-3 px-8 rounded-lg transition-colors duration-200 inline-flex items-center justify-center"
            >
              Get Started Free
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link
              to="/about"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
            >
              View Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-legal-900 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center mb-4">
                <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <span className="ml-3 text-xl font-bold">
                  AI Legal Doc Explainer
                </span>
              </div>
              <p className="text-legal-300 mb-4">
                Advanced AI-powered legal document analysis and risk assessment platform.
              </p>
              <div className="flex space-x-4">
                <div className="w-8 h-8 bg-legal-700 rounded-lg flex items-center justify-center">
                  <Users className="w-4 h-4" />
                </div>
                <div className="w-8 h-8 bg-legal-700 rounded-lg flex items-center justify-center">
                  <Shield className="w-4 h-4" />
                </div>
                <div className="w-8 h-8 bg-legal-700 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-4 h-4" />
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-legal-300">
                <li>Document Analysis</li>
                <li>Risk Assessment</li>
                <li>Clause Detection</li>
                <li>Visual Insights</li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-legal-300">
                <li>About</li>
                <li>Contact</li>
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-legal-700 mt-8 pt-8 text-center text-legal-400">
            <p>&copy; 2024 AI Legal Document Explainer. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
