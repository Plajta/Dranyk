"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";

type MapProps = {
  position: [number, number];
  zoom: number;
  geojsondata: any;
};

export default function GeoJsonMap(props: MapProps) {
  const Map = useMemo(
    () =>
      dynamic(() => import("@/components/map"), {
        loading: () => <p>A map is loading</p>,
        ssr: false,
      }),
    [],
  );
  const position: [number, number] = [51.505, -0.09];
  const zoom = 13;

  return (
    <>
      <Map
        position={props.position}
        zoom={props.zoom}
        geojsondata={props.geojsondata}
      />
    </>
  );
}
