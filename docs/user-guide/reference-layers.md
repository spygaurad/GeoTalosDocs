# Reference layers

Reference layers are public maps you can switch on over your own imagery for context: where the wetlands, protected areas, mining and logging concessions and rivers are. They are the same for every organization and nobody can edit them.

## Available layers

| Layer | Shows | Covers | Source |
|---|---|---|---|
| **Ramsar Sites** | Wetlands of international importance | Worldwide | Ramsar Sites Information Service (CC BY 4.0) |
| **Amazon protected areas** | Protected areas | Amazon basin | RAISG |
| **Amazon mining** | Mining areas | Amazon basin | RAISG |
| **Mining concessions** | Mining concession boundaries | Worldwide | Global Forest Watch (CC BY 4.0) |
| **Logging concessions** | Logging concession boundaries | Worldwide | Global Forest Watch / WRI |
| **HydroRIVERS** | River network | South America | HydroSHEDS |
| **USGS mineral deposits** | Mineral deposit locations | Worldwide | USGS MRDS (public domain) |
| **Peru native communities** | Native community lands | Peru | COFOPRI via GEOCATMIN |

Licences and download links for each are in [Data sources and licences](../reference/data-sources.md). Check the publisher's terms before reusing a layer outside GeoTALOS.

## Turn a layer on

1. Open a map.
2. In the layers panel on the left, find the **Reference layers** section.
3. Switch on the layers you want. Switch a layer off the same way.

> **Screenshot:** the Reference layers section with Ramsar Sites and HydroRIVERS switched on over imagery.

Each layer's credit appears in the attribution line at the bottom of the map while it is on.

## Good to know

- **Zoom range.** Each layer is drawn only between certain zoom levels. If a layer is on but you see nothing, zoom in or out, or move to the region it covers.
- **Not saved with the map.** Which reference layers are on is remembered only while the map is open. Switch them on again after reloading the page.
- **Read only.** You cannot edit reference layers or run models on them. To compare your results with a reference layer, view both on the same map.
- **Missing layer.** If a layer is not in the list, it has not been loaded on your GeoTALOS server yet. Ask your administrator. Developers can rebuild layers with the steps in [Tiles, caching and reference layers](../developer/tiles.md).

## Example uses

- Check whether palm detections fall inside a protected area.
- See which mining concessions overlap an area where your imagery shows forest loss.
- Use HydroRIVERS to find river sections near detected mining activity.
