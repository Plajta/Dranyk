"use client";
import { MapContainer, Marker, Popup, TileLayer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";

type MapProps = {
  position: [number, number];
  zoom: number;
  geojsondata: any;
};

export default function Map({ position, zoom, geojsondata }: MapProps) {
  return (
    <MapContainer
      center={position}
      zoom={zoom}
      scrollWheelZoom={true}
      style={{ height: "700px", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openmaptiles.org/">OpenMapTiles</a> | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url={`https://api.maptiler.com/maps/dataviz/{z}/{x}/{y}.png?key=${process.env.NEXT_PUBLIC_MT_API_KEY}`}
      />
      <GeoJSON
        data={geojsondata}
        onEachFeature={(feature, layer) => {
          if (feature.properties?.name) {
            layer.bindPopup(feature.properties.name);
          }
        }}
      />
    </MapContainer>
  );
}
