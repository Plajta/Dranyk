import GeoJsonMap from "@/components/geojsonmap";
import { promises as fs } from "fs";

export default async function MapPage() {
  const file = await fs.readFile(
    process.cwd() + "/../data/WGS_vodni_tok.geojson",
    "utf8",
  );
  const geojsonmap = JSON.parse(file);
  const position: [number, number] = [51.505, -0.09];
  const zoom = 13;
  return (
    <div>
      <GeoJsonMap position={position} zoom={zoom} geojsondata={geojsonmap} />
    </div>
  );
}
