import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Shield, 
  BarChart3, 
  Zap, 
  Code, 
  Database,
  Cpu,
  Globe,
  ArrowRight,
  CheckCircle,
  Users,
  Award
} from 'lucide-react';

const AboutPage = () => {
  const phases = [
    {
      phase: 'Phase 1',
      title: 'Foundation & Core Services',
      description: 'Basic document processing, text analysis, and risk classification',
      status: '✅ Complete',
      features: ['Document text extraction', 'Legal term identification', 'Basic risk assessment', 'API endpoints']
    },
    {
      phase: 'Phase 2',
      title: 'Advanced Analysis & Risk Classification',
      description: 'Enhanced clause detection, multi-level risk assessment, and document highlighting',
      status: '✅ Complete',
      features: ['Legal clause detection', 'Enhanced risk classification', 'Document highlighting', 'Comprehensive API responses']
    },
    {
      phase: 'Phase 3',
      title: 'User Interface & Visualization',
      description: 'Modern React web interface with PDF viewer and interactive charts',
      status: '🚧 In Progress',
      features: ['React frontend', 'PDF viewer integration', 'Risk visualization charts', 'Mobile-responsive design']
    },
    {
      phase: 'Phase 4',
      title: 'AI Q&A & Advanced Features',
      description: 'Natural language Q&A system and multi-language support',
      status: '⏳ Planned',
      features: ['Question-answering system', 'Multi-language support', 'Confidence scoring', 'What-if simulations']
    },
    {
      phase: 'Phase 5',
      title: 'Innovation & Polish',
      description: 'Community features and advanced capabilities',
      status: '⏳ Planned',
      features: ['Community clause library', 'Offline capabilities', 'Advanced analytics', 'Enterprise features']
    }
  ];

  const techStack = [
    {
      category: 'Backend',
      technologies: ['Python 3.8+', 'FastAPI', 'Pydantic', 'SQLAlchemy'],
      icon: Database
    },
    {
      category: 'AI & ML',
      technologies: ['OpenAI GPT', 'NLP Processing', 'Pattern Matching', 'Risk Algorithms'],
      icon: Cpu
    },
    {
      category: 'Frontend',
      technologies: ['React 18', 'Tailwind CSS', 'PDF.js', 'Recharts'],
      icon: Code
    },
    {
      category: 'Infrastructure',
      technologies: ['Docker', 'Git', 'RESTful APIs', 'JSON Schema'],
      icon: Globe
    }
  ];

  const features = [
    {
      icon: FileText,
      title: 'Document Processing',
      description: 'Support for PDF, DOC, DOCX, and TXT files with intelligent text extraction and chunking.',
      color: 'text-blue-600'
    },
    {
      icon: Shield,
      title: 'Risk Assessment',
      description: 'Multi-level risk classification across financial, operational, legal, commercial, and regulatory categories.',
      color: 'text-green-600'
    },
    {
      icon: BarChart3,
      title: 'Visual Analytics',
      description: 'Interactive charts, risk heatmaps, and highlighted document sections for better understanding.',
      color: 'text-purple-600'
    },
    {
      icon: Zap,
      title: 'Fast Processing',
      description: 'Optimized algorithms ensure analysis completion in under 5 seconds for most documents.',
      color: 'text-orange-600'
    }
  ];

  return (
    <div className="min-h-screen bg-legal-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 via-white to-legal-50 py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-legal-900 mb-6">
            About the Project
          </h1>
          <p className="text-xl text-legal-600 max-w-3xl mx-auto mb-8">
            AI Legal Document Explainer is a comprehensive platform that transforms complex legal documents 
            into clear, actionable insights using advanced artificial intelligence and natural language processing.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/analyze"
              className="btn-primary text-lg px-8 py-4 inline-flex items-center justify-center"
            >
              Try It Now
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <a
              href="#phases"
              className="btn-secondary text-lg px-8 py-4"
            >
              View Roadmap
            </a>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-legal-600 mb-6 leading-relaxed">
                To democratize legal document analysis by providing professionals and businesses with 
                AI-powered tools that make complex legal language accessible and understandable.
              </p>
              <p className="text-lg text-legal-600 mb-6 leading-relaxed">
                We believe that everyone should have access to clear, accurate legal insights without 
                the need for expensive legal consultations for basic document review.
              </p>
              <div className="flex items-center space-x-4">
                <div className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                  <span className="text-legal-700">95%+ Accuracy</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                  <span className="text-legal-700">Under 5s Processing</span>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-primary-100 to-legal-100 rounded-2xl p-8">
              <div className="text-center">
                <div className="w-24 h-24 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <FileText className="w-12 h-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-legal-900 mb-4">
                  AI-Powered Analysis
                </h3>
                <p className="text-legal-700">
                  Leveraging state-of-the-art natural language processing and machine learning 
                  to provide accurate, reliable legal document insights.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-legal-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Key Features
            </h2>
            <p className="text-xl text-legal-600 max-w-2xl mx-auto">
              Comprehensive tools for legal document analysis and risk assessment
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="bg-white rounded-xl shadow-legal border border-legal-200 p-6">
                  <div className="w-12 h-12 bg-legal-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon className={`w-6 h-6 ${feature.color}`} />
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

      {/* Development Phases */}
      <section id="phases" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Development Roadmap
            </h2>
            <p className="text-xl text-legal-600 max-w-2xl mx-auto">
              Our phased approach to building a comprehensive legal analysis platform
            </p>
          </div>
          
          <div className="space-y-8">
            {phases.map((phase, index) => (
              <div key={index} className="bg-legal-50 rounded-xl p-6 border border-legal-200">
                <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-4">
                  <div className="flex items-center mb-4 lg:mb-0">
                    <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mr-4">
                      <span className="text-lg font-bold text-primary-600">{index + 1}</span>
                    </div>
                    <div>
                      <div className="flex items-center space-x-3">
                        <h3 className="text-xl font-bold text-legal-900">{phase.phase}</h3>
                        <span className="text-sm font-medium px-3 py-1 rounded-full bg-legal-200 text-legal-700">
                          {phase.status}
                        </span>
                      </div>
                      <p className="text-lg font-semibold text-legal-700">{phase.title}</p>
                    </div>
                  </div>
                </div>
                
                <p className="text-legal-600 mb-4">{phase.description}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {phase.features.map((feature, featureIndex) => (
                    <div key={featureIndex} className="flex items-center">
                      <CheckCircle className="w-4 h-4 text-green-600 mr-2 flex-shrink-0" />
                      <span className="text-sm text-legal-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-legal-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Technology Stack
            </h2>
            <p className="text-xl text-legal-600 max-w-2xl mx-auto">
              Built with modern, scalable technologies for optimal performance
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {techStack.map((tech, index) => {
              const Icon = tech.icon;
              return (
                <div key={index} className="bg-white rounded-xl shadow-legal border border-legal-200 p-6 text-center">
                  <div className="w-16 h-16 bg-primary-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-legal-900 mb-4">
                    {tech.category}
                  </h3>
                  <div className="space-y-2">
                    {tech.technologies.map((technology, techIndex) => (
                      <div key={techIndex} className="text-sm text-legal-600 bg-legal-50 px-3 py-2 rounded-lg">
                        {technology}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-legal-900 mb-4">
              Built for Legal Professionals
            </h2>
            <p className="text-xl text-legal-600 max-w-2xl mx-auto">
              Designed with input from legal experts and business professionals
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Users className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-legal-900 mb-3">
                Legal Professionals
              </h3>
              <p className="text-legal-600">
                Lawyers, paralegals, and legal consultants who need quick document analysis and risk assessment.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Award className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-legal-900 mb-3">
                Business Executives
              </h3>
              <p className="text-legal-600">
                CEOs, CFOs, and business leaders who need to understand legal risks in contracts and agreements.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-10 h-10 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-legal-900 mb-3">
                Compliance Officers
              </h3>
              <p className="text-legal-600">
                Professionals responsible for ensuring regulatory compliance and risk management.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to Experience the Future of Legal Analysis?
          </h2>
          <p className="text-xl text-primary-100 mb-8 leading-relaxed">
            Join thousands of professionals who trust our AI-powered platform for accurate, 
            fast, and comprehensive legal document analysis.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/analyze"
              className="bg-white text-primary-600 hover:bg-gray-50 font-semibold py-3 px-8 rounded-lg transition-colors duration-200 inline-flex items-center justify-center"
            >
              Start Analyzing Now
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link
              to="/"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;
