# EcoGuard Quick Start Guide

## 🚀 Running the Application

### Frontend (React Application)
The frontend development server should already be running. If not:

```bash
cd frontend
npm install
npm run dev
```

**Access the site at:** http://localhost:8080

### Backend (Streamlit Dashboards)
To run the Python backend:

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run main dashboard
cd backend/dashboards
streamlit run app.py
```

**Access at:** http://localhost:8501

Or use the batch scripts:
```bash
scripts\run_enhanced_dashboard.bat
```

## 📁 Project Structure

```
AcousticGuardian/
├── frontend/              # React/TypeScript frontend
│   └── src/              # Source code
├── backend/
│   ├── dashboards/       # Streamlit applications
│   ├── scripts/          # Python utilities
│   └── config/           # Configuration files
├── hardware/             # Arduino/ESP32 code
├── data/                 # Data files (CSV, GeoJSON)
├── scripts/              # Batch scripts
└── docs/                 # Documentation
```

## 🔐 Default Login Credentials

- **Forest Ranger**: username `ranger1`, password `password`
- **Regional Manager**: username `manager1`, password `password`
- **Super User**: username `admin`, password `password`

## 🐦 About the Digital Hummingbird

EcoGuard is inspired by Wangari Maathai's hummingbird story - small sensors doing the best they can to protect Kenya's forests.

## 📚 Documentation

See `docs/` directory for:
- Deployment guides
- Hardware setup
- API documentation
- Testing procedures

## 🛠️ Development

### Frontend
- Framework: React + TypeScript + Vite
- Styling: Tailwind CSS
- UI Components: shadcn/ui

### Backend
- Framework: Streamlit
- Data: InfluxDB, Pandas
- Visualization: Folium, Plotly

## 📞 Support

For issues or questions, see the Contact page in the application or check the documentation.

