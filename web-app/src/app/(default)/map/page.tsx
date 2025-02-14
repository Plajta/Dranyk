"use client";
import dynamic from "next/dynamic";
import { useMemo } from "react";

export default function MapPage() {
  const Map = useMemo(
    () =>
      dynamic(() => import("@/components/geojsonmap"), {
        loading: () => <p>A map is loading</p>,
        ssr: false,
      }),
    [],
  );

  const position: [number, number] = [51.505, -0.09];
  const zoom = 13;

  return (
    <div>
      <Map position={position} zoom={zoom} />
      <p>map</p>
    </div>
  );
}
