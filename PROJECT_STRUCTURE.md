# EcoGuard Project Structure

## Directory Organization

```
AcousticGuardian/
├── frontend/                 # React/TypeScript frontend application
│   ├── src/                  # Source code
│   ├── public/               # Static assets
│   └── package.json          # Frontend dependencies
│
├── backend/                  # Python backend
│   ├── dashboards/          # Streamlit dashboard applications
│   ├── scripts/              # Python utility scripts
│   └── config/              # Configuration files
│
├── hardware/                 # Hardware/Arduino files
│   ├── *.ino                # Arduino sketches
│   ├── *.h                  # Header files
│   └── *.cpp                # C++ source files
│
├── data/                     # Data files
│   ├── kenya/               # Kenya forest data (CSV)
│   └── geojson/             # GeoJSON and JSON data files
│
├── scripts/                  # Batch/shell scripts
│   └── *.bat                # Windows batch files
│
├── docs/                     # Documentation
│   └── *.md                 # Markdown documentation files
│
├── requirements.txt          # Python dependencies
├── README.md                 # Main project README
└── PROJECT_STRUCTURE.md      # This file
```

## Key Files

### Frontend
- `frontend/` - React application with Vite
- Access at: http://localhost:8080

### Backend Dashboards
- `backend/dashboards/app.py` - Main Streamlit application
- `backend/dashboards/*_dashboard.py` - Various dashboard views

### Data
- `data/kenya/` - Kenya forest location and type data
- `data/geojson/` - GeoJSON forest boundaries

### Documentation
- `docs/README.md` - Main documentation
- `docs/deployment_guide.md` - Deployment instructions
- `docs/rpi_deployment_guide.md` - Raspberry Pi setup

## Running the Application

### Frontend (React)
```bash
cd frontend
npm run dev
```
Access at: http://localhost:8080

### Backend (Streamlit)
```bash
cd backend/dashboards
streamlit run app.py
```
Access at: http://localhost:8501

## Notes

- Keep `README.md` in root for GitHub visibility
- Configuration files in `backend/config/`
- All batch scripts in `scripts/` directory
- Documentation organized in `docs/` directory

