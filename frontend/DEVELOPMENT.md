# EcoGuard Frontend Development Guide

## Overview

This document explains how to develop and integrate the modern React frontend with the existing Streamlit system.

## Current Structure

The frontend directory contains:
- `src/App.tsx` - Main application component
- `src/main.tsx` - Entry point
- `src/pages/` - Page components (Contact, Analytics)
- `src/components/` - UI components
- `src/hooks/` - Custom hooks
- `src/store/` - State management

## Development Workflow

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## Integration with Streamlit Backend

To connect the React frontend with the existing Streamlit backend:

1. Create API endpoints in the Python backend
2. Use fetch or axios to make HTTP requests from React components
3. Handle authentication tokens between systems

Example API integration:
```typescript
// Example of how to fetch forest data
const fetchForestData = async () => {
  try {
    const response = await fetch('/api/forests');
    const data = await response.json();
    // Process data in React component
  } catch (error) {
    console.error('Error fetching forest data:', error);
  }
};
```

## Component Development

When developing new components:

1. Create the component in `src/components/`
2. Use TypeScript for type safety
3. Follow the existing styling patterns
4. Test components in isolation

## Page Development

When creating new pages:

1. Create the page component in `src/pages/`
2. Add routing in the main router
3. Ensure mobile responsiveness
4. Implement proper error handling

## Styling Guidelines

- Use Tailwind CSS classes for styling
- Follow the existing color scheme
- Maintain consistent spacing and typography
- Ensure accessibility compliance

## Deployment

1. Build the production version
2. Serve the built files through the Streamlit server
3. Configure routing appropriately