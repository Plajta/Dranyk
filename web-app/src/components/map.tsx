"use client";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  LayersControl,
  LayerGroup,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

const { BaseLayer, Overlay } = LayersControl;

type MapProps = {
  position: [number, number];
  zoom: number;
  geojsonDataArray: any;
};

const colors = [
  "#e6194b",
  "#3cb44b",
  "#ffe119",
  "#4363d8",
  "#f58231",
  "#911eb4",
  "#46f0f0",
  "#f032e6",
  "#bcf60c",
  "#fabebe",
];

export default function Map({ position, zoom, geojsonDataArray }: MapProps) {
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
      {geojsonDataArray.map(
        (data: any, index: any) =>
          data && (
            <GeoJSON
              key={index}
              data={data}
              style={() => ({
                color: colors[index % colors.length],
                weight: 3,
                opacity: 0.8,
                fillOpacity: 0.4,
              })}
              onEachFeature={(feature, layer) => {
                if (feature.properties?.name) {
                  layer.bindPopup(feature.properties.name);
                }
              }}
            />
          ),
      )}
    </MapContainer>
  );
}
