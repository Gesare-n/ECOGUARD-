// Map component for EcoGuard - displays forest sensors on an interactive map
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect, useRef } from 'react';

// Fix for default marker icons in React-Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const ForestMap = () => {
  // Sample sensor data - in a real app this would come from an API
  const sensors = [
    { id: 1, name: 'Karura Forest Sensor 1', lat: -1.2728, lng: 36.8219, status: 'active', lastDetection: '2 hours ago' },
    { id: 2, name: 'Karura Forest Sensor 2', lat: -1.2700, lng: 36.8250, status: 'active', lastDetection: '5 hours ago' },
    { id: 3, name: 'Uhuru Park Sensor 1', lat: -1.2800, lng: 36.8100, status: 'warning', lastDetection: '1 hour ago' },
    { id: 4, name: 'Ngong Forest Sensor 1', lat: -1.3500, lng: 36.7000, status: 'active', lastDetection: '1 day ago' },
  ];

  // Map center (Nairobi, Kenya)
  const center: [number, number] = [-1.2921, 36.8219];
  
  // Google Maps API key from backend config
  const googleMapsApiKey = 'AIzaSyACApQn1JG2iuLby7b5rMvkLaho383a42s';
  
  const mapRef = useRef<any>(null);
  
  useEffect(() => {
    if (mapRef.current) {
      mapRef.current.setView(center, 11);
    }
  }, []);
  
  return (
    <div className="h-96 w-full rounded-lg overflow-hidden">
      <MapContainer 
        style={{ height: '100%', width: '100%' }}
        ref={mapRef}
      >
        <TileLayer
          url={`https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}&key=${googleMapsApiKey}`}
        />
        {sensors.map(sensor => (
          <Marker 
            key={sensor.id} 
            position={[sensor.lat, sensor.lng]}
          >
            <Popup>
              <div className="text-sm">
                <h3 className="font-bold">{sensor.name}</h3>
                <p>Status: 
                  <span className={`ml-1 px-2 py-1 rounded text-xs ${
                    sensor.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {sensor.status}
                  </span>
                </p>
                <p>Last detection: {sensor.lastDetection}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default ForestMap;