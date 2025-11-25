// Map component for EcoGuard - displays forest sensors on an interactive map
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

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
  
  return (
    <div className="h-96 w-full rounded-lg overflow-hidden">
      <MapContainer center={center} zoom={11} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
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