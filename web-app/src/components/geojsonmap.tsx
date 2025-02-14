"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";

type MapProps = {
  position: [number, number];
  zoom: number;
  geojsonDataArray: any;
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
  return (
    <>
      <Map
        position={props.position}
        zoom={props.zoom}
        geojsonDataArray={props.geojsonDataArray}
      />
    </>
  );
}
