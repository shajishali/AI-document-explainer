# AI Legal Document Explainer - Frontend

**Phase 3: User Interface & Visualization**

A modern, responsive React web application for the AI Legal Document Explainer platform. This frontend provides an intuitive interface for uploading documents, viewing analysis results, and exploring risk assessments with interactive visualizations.

## 🚀 Features

### **Core Functionality**
- **Document Upload**: Drag & drop file upload with support for PDF, DOC, DOCX, and TXT
- **Text Input**: Direct text input for quick analysis without file uploads
- **Real-time Processing**: Live progress indicators and status updates
- **Responsive Design**: Mobile-first design that works on all devices

### **User Experience**
- **Modern UI**: Clean, professional interface built with Tailwind CSS
- **Interactive Navigation**: Smooth routing with React Router
- **Toast Notifications**: User feedback for actions and errors
- **Loading States**: Engaging loading animations and progress bars

### **Technical Features**
- **React 18**: Latest React features with hooks and modern patterns
- **Tailwind CSS**: Utility-first CSS framework for rapid development
- **Responsive Grid**: Flexible layouts that adapt to screen sizes
- **Component Library**: Reusable UI components with consistent styling

## 🛠️ Technology Stack

- **Frontend Framework**: React 18.2.0
- **Routing**: React Router DOM 6.8.0
- **Styling**: Tailwind CSS 3.3.0
- **Icons**: Lucide React
- **Charts**: Recharts (planned for results visualization)
- **PDF Viewer**: PDF.js (planned for document display)
- **Build Tool**: Create React App
- **Package Manager**: npm

## 📱 Responsive Design

The application is built with a **mobile-first approach** and includes:

- **Mobile**: Optimized for small screens with touch-friendly interactions
- **Tablet**: Adaptive layouts for medium-sized devices
- **Desktop**: Full-featured experience with expanded navigation
- **Breakpoints**: Responsive grid systems and flexible components

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ and npm
- Backend API running on `http://localhost:5000`

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
│   ├── index.html         # Main HTML file
│   └── favicon.ico        # App icon
├── src/                   # Source code
│   ├── components/        # Reusable UI components
│   │   ├── Navbar.js      # Navigation component
│   │   └── DocumentUploader.js # File upload component
│   ├── pages/             # Page components
│   │   ├── HomePage.js    # Landing page
│   │   ├── DocumentAnalysisPage.js # Analysis interface
│   │   ├── AnalysisResultsPage.js # Results display
│   │   └── AboutPage.js   # Project information
│   ├── utils/             # Utility functions
│   ├── App.js             # Main app component
│   ├── index.js           # App entry point
│   └── index.css          # Global styles and Tailwind
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js      # PostCSS configuration
```

## 🎨 Design System

### **Color Palette**
- **Primary**: Blue shades for main actions and branding
- **Legal**: Gray shades for professional, legal theme
- **Risk Levels**: Color-coded risk indicators (Critical, High, Medium, Low, Minimal)
- **Status**: Success, warning, and error colors

### **Typography**
- **Font Family**: Inter (Google Fonts) for modern readability
- **Monospace**: JetBrains Mono for code and technical content
- **Responsive**: Scalable text sizes across devices

### **Components**
- **Buttons**: Primary, secondary, and variant styles
- **Cards**: Consistent card layouts with shadows
- **Forms**: Input fields with focus states and validation
- **Navigation**: Responsive navigation with mobile menu

## 🔧 Configuration

### **Tailwind CSS**
The project uses a custom Tailwind configuration with:
- Extended color palette for legal theme
- Custom animations and keyframes
- Responsive design utilities
- Component-specific styles

### **API Integration**
- **Proxy**: Configured to proxy API calls to backend
- **Endpoints**: RESTful API integration planned
- **Error Handling**: Comprehensive error states and user feedback

## 📱 Mobile Responsiveness

### **Breakpoints**
- **Mobile**: `sm:` (640px+)
- **Tablet**: `md:` (768px+)
- **Desktop**: `lg:` (1024px+)
- **Large Desktop**: `xl:` (1280px+)

### **Mobile Features**
- Touch-friendly button sizes
- Swipe gestures for navigation
- Optimized form inputs
- Collapsible navigation menu

## 🚧 Development Status

### **Completed (Phase 3)**
- ✅ React application structure
- ✅ Responsive navigation
- ✅ Document upload interface
- ✅ Home page with features
- ✅ About page with roadmap
- ✅ Mobile-responsive design
- ✅ Tailwind CSS styling

### **In Progress**
- 🔄 Analysis results page
- 🔄 PDF viewer integration
- 🔄 Risk visualization charts
- 🔄 Interactive highlights

### **Planned**
- 📋 Real-time API integration
- 📋 Advanced chart components
- 📋 PDF.js integration
- 📋 Performance optimization

## 🧪 Testing

### **Run Tests**
```bash
npm test
```

### **Test Coverage**
- Component rendering tests
- User interaction tests
- Responsive design tests
- API integration tests

## 🚀 Deployment

### **Build Process**
1. Run `npm run build`
2. Deploy `build/` folder to web server
3. Configure server for React Router (SPA routing)

### **Environment Variables**
- `REACT_APP_API_URL`: Backend API endpoint
- `REACT_APP_ENVIRONMENT`: Development/Production mode

## 🤝 Contributing

1. Follow the existing code style
2. Ensure mobile responsiveness
3. Test across different screen sizes
4. Update documentation for new features

## 📄 License

This project is part of the AI Legal Document Explainer platform.

## 🔗 Related Links

- **Backend API**: Python FastAPI backend
- **Documentation**: Project requirements and implementation plan
- **Testing**: Phase 2 testing suite and validation

---

**Phase 3 Status**: 🚧 In Progress - Core UI components complete, results visualization in development
