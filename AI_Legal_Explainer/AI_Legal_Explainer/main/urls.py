from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views
from . import multilingual_views
from . import enhanced_views
from . import phase3_views
from . import phase4_views

# Create router for API endpoints
router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'clauses', views.ClauseViewSet)
router.register(r'risk-analysis', views.RiskAnalysisViewSet)
router.register(r'summaries', views.DocumentSummaryViewSet)
router.register(r'chat', views.ChatViewSet, basename='chat')
router.register(r'legal-terms', views.LegalTermViewSet)
router.register(r'processing-logs', views.DocumentProcessingLogViewSet)
router.register(r'multilingual', multilingual_views.MultilingualViewSet, basename='multilingual')

# Enhanced functionality routers
router.register(r'risk-visualization', enhanced_views.RiskVisualizationViewSet, basename='risk_visualization')
router.register(r'what-if-simulation', enhanced_views.WhatIfSimulationViewSet, basename='what_if_simulation')
router.register(r'clause-library', enhanced_views.ClauseLibraryViewSet, basename='clause_library')

# Phase 3 functionality routers
router.register(r'offline-mode', phase3_views.OfflineModeViewSet, basename='offline_mode')
router.register(r'transparency-controls', phase3_views.TransparencyControlsViewSet, basename='transparency_controls')
router.register(r'performance-optimization', phase3_views.PerformanceOptimizationViewSet, basename='performance_optimization')
router.register(r'advanced-analytics', phase3_views.AdvancedAnalyticsViewSet, basename='advanced_analytics')

app_name = 'main'

urlpatterns = [
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    
    # Traditional Django views
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('document/<uuid:document_id>/', views.document_detail, name='document_detail'),
    path('document/<uuid:document_id>/status/', views.document_processing_status, name='document_processing_status'),
    path('glossary/', views.glossary_view, name='glossary'),
    path('upload/', views.upload_document, name='upload_document'),
    path('test-upload/', views.test_upload, name='test_upload'),
    path('debug-upload/', views.debug_upload, name='debug_upload'),
    path('simple-upload-test/', views.simple_upload_test, name='simple_upload_test'),
    path('test-upload-page/', views.test_upload_page, name='test_upload_page'),
    
    # Enhanced functionality views
    path('document/<uuid:document_id>/risk-dashboard/', enhanced_views.risk_dashboard_view, name='risk_dashboard'),
    path('clause/<uuid:clause_id>/simulation/', enhanced_views.what_if_simulation_view, name='what_if_simulation'),
    path('clause/<uuid:clause1_id>/compare/<uuid:clause2_id>/', enhanced_views.clause_comparison_view, name='clause_comparison'),
    path('clause-library/', enhanced_views.clause_library_view, name='clause_library'),
    
    # Phase 3 functionality views
    path('offline-dashboard/', phase3_views.offline_dashboard, name='offline_dashboard'),
    path('transparency-controls/', phase3_views.transparency_controls, name='transparency_controls'),
    path('performance-dashboard/', phase3_views.performance_dashboard, name='performance_dashboard'),
    path('analytics-dashboard/', phase3_views.analytics_dashboard, name='analytics_dashboard'),
    
    # Phase 4 functionality views - Security & Compliance
    path('security-dashboard/', phase4_views.security_dashboard, name='security_dashboard'),
    path('compliance-dashboard/', phase4_views.compliance_dashboard, name='compliance_dashboard'),
    path('privacy-center/', phase4_views.privacy_center, name='privacy_center'),
    path('run-security-audit/', phase4_views.run_security_audit, name='run_security_audit'),
    
    # Phase 4 functionality views - Testing & Quality Assurance
    path('testing-dashboard/', phase4_views.testing_dashboard, name='testing_dashboard'),
    path('quality-assurance/', phase4_views.quality_assurance, name='quality_assurance'),
    path('run-test-suite/', phase4_views.run_test_suite, name='run_test_suite'),
    
    # Phase 4 functionality views - Documentation & Training
    path('documentation-portal/', phase4_views.documentation_portal, name='documentation_portal'),
    path('training-portal/', phase4_views.training_portal, name='training_portal'),
    path('support-portal/', phase4_views.support_portal, name='support_portal'),
    path('create-support-ticket/', phase4_views.create_support_ticket, name='create_support_ticket'),
    
    # Phase 4 functionality views - Production Management
    path('production-dashboard/', phase4_views.production_dashboard, name='production_dashboard'),
    path('setup-monitoring/', phase4_views.setup_monitoring, name='setup_monitoring'),
    path('create-backup/', phase4_views.create_backup, name='create_backup'),
    path('setup-onboarding/', phase4_views.setup_onboarding, name='setup_onboarding'),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Additional API endpoints
    path('api/documents/<uuid:document_id>/process/', views.DocumentViewSet.as_view({'post': 'process'}), name='document_process'),
    path('api/documents/<uuid:document_id>/clauses/', views.DocumentViewSet.as_view({'get': 'clauses'}), name='document_clauses'),
    path('api/documents/<uuid:document_id>/risk-analysis/', views.DocumentViewSet.as_view({'get': 'risk_analysis'}), name='document_risk_analysis'),
    path('api/documents/<uuid:document_id>/summary/', views.DocumentViewSet.as_view({'get': 'summary'}), name='document_summary'),
    
    # Chat endpoints
    path('api/chat/ask/', views.ChatViewSet.as_view({'post': 'ask_question'}), name='chat_ask'),
    path('api/chat/history/', views.ChatViewSet.as_view({'get': 'session_history'}), name='chat_history'),
    
    # Legal terms endpoints
    path('api/legal-terms/search/', views.LegalTermViewSet.as_view({'get': 'search'}), name='legal_terms_search'),
    path('api/legal-terms/highlight/', views.LegalTermViewSet.as_view({'get': 'highlight_text'}), name='legal_terms_highlight'),
    
    # Enhanced functionality AJAX endpoints
    path('api/simulate-scenario/', enhanced_views.ajax_simulate_scenario, name='ajax_simulate_scenario'),
    path('api/compare-clauses/', enhanced_views.ajax_compare_clauses, name='ajax_compare_clauses'),
    
    # Phase 3 AJAX endpoints
    path('api/offline-status/', phase3_views.api_offline_status, name='api_offline_status'),
    path('api/transparency-preferences/', phase3_views.api_transparency_preferences, name='api_transparency_preferences'),
    path('api/performance-metrics/', phase3_views.api_performance_metrics, name='api_performance_metrics'),
    path('api/analytics-dashboard/', phase3_views.api_analytics_dashboard, name='api_analytics_dashboard'),
    
    # Phase 4 API endpoints
    path('api/security-status/', phase4_views.api_security_status, name='api_security_status'),
    path('api/testing-results/', phase4_views.api_testing_results, name='api_testing_results'),
    path('api/production-status/', phase4_views.api_production_status, name='api_production_status'),
    path('api/health-check/', phase4_views.api_health_check, name='api_health_check'),
    path('api/update-consent/', phase4_views.update_consent, name='api_update_consent'),
    
    # Multilingual endpoints
    path('language-switcher/', multilingual_views.language_switcher, name='language_switcher'),
    path('glossary/<str:language>/', multilingual_views.multilingual_glossary, name='multilingual_glossary'),
    path('glossary/', multilingual_views.multilingual_glossary, name='multilingual_glossary_default'),
]
