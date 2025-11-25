# EcoGuard Modern Frontend (Vite + React + TypeScript)

This is a modern frontend implementation for the EcoGuard Forest Protection System using Vite, React, TypeScript, and Tailwind CSS. This frontend would replace the current Streamlit interface with a more sophisticated and performant user experience.

## Features Planned for Implementation

### Authentication & Role-Based Access
- Login/logout functionality
- Role-based navigation (Forest Ranger, Regional Manager, Super User)
- User profile management
- Password security

### Dashboard Components
- Interactive forest maps with Leaflet/React-Leaflet
- Real-time sensor monitoring
- Deforestation risk analysis
- Data visualization with Recharts
- Responsive design for all device sizes

### Technical Stack
- **Framework**: Vite + React + TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: Zustand
- **Routing**: React Router
- **Data Visualization**: Recharts
- **UI Components**: shadcn/ui, Radix UI primitives
- **Form Handling**: React Hook Form + Zod validation
- **API Communication**: TanStack Query

## Current Status

This is a placeholder structure that demonstrates how the modern frontend would be organized. The actual implementation would require:

1. Installing all dependencies:
   ```bash
   npm install
   ```

2. Running the development server:
   ```bash
   npm run dev
   ```

## Architecture Overview

### Component Structure
```
src/
├── components/          # Reusable UI components
├── contexts/            # React context providers
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions and helpers
├── pages/               # Page components for routing
├── services/            # API service layer
└── types/               # TypeScript type definitions
```

### Key Features by User Role

#### Forest Ranger
- Basic monitoring access for assigned region
- Sensor status viewing
- Detection history
- Simple maps and alerts

#### Regional Manager
- Extended access with reporting capabilities
- Regional analytics
- Advanced maps and data visualization
- Report generation

#### Super User
- Full system access
- User management
- System-wide analytics
- Administrative tools

## Integration with Backend

The frontend would communicate with the existing Python backend through RESTful API endpoints that would need to be created to serve data to the React components.

## Future Enhancements

- Real-time data updates with WebSockets
- Offline capability with service workers
- Progressive Web App (PWA) support
- Advanced analytics and machine learning integration
- Mobile app version with React Native