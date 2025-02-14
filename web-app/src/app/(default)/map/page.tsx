import fs from "fs/promises";
import GeoJsonMap from "@/components/geojsonmap";
import path from "path";

export default async function MapPage() {
  const dataDir = path.join(process.cwd(), "/../data");
  const filenames = await fs.readdir(dataDir);
  const geojsonDataArray = await Promise.all(
    filenames.map(async (filename) => {
      const filePath = path.join(dataDir, filename);
      const fileContents = await fs.readFile(filePath, "utf-8");
      return JSON.parse(fileContents);
    }),
  );
  const position: [number, number] = [49.7475, 13.3776];
  const zoom = 13;
  const router_url = process.env.ROUTER_HOST ?? "";
  try {
    const route_data = await fetch(router_url);
    const route_json = await route_data.json();
    geojsonDataArray.push(route_json);
  } catch (e) {
    console.log(e);
  }
  return (
    <div>
      <GeoJsonMap
        position={position}
        zoom={zoom}
        geojsonDataArray={geojsonDataArray}
      />
    </div>
  );
}
