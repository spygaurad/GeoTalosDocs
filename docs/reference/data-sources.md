# Data sources and licences

This page lists where the data and models used by GeoTALOS come from, and what each licence allows. Always check the publisher's current terms before you redistribute any of it.

## Reference layers

These are served to every organization as [reference layers](../user-guide/reference-layers.md).

| Layer | Publisher | Download used | Licence and conditions |
|---|---|---|---|
| Ramsar Sites | [Ramsar Sites Information Service](https://rsis.ramsar.org/) | [WFS shapefile export](https://rsis.ramsar.org/geoserver/wfs?request=GetFeature&service=wfs&version=1.0.0&typename=ramsar_sdi%3Afeatures_published&outputformat=SHAPE-ZIP) | [CC BY 4.0](https://www.ramsar.org/licence-information) |
| Amazon protected areas, Amazon mining | [RAISG](https://www.raisg.org/en/maps/) | [ArcGIS REST services](https://geo.socioambiental.org/webadaptor2/rest/services/raisg/) | Cite RAISG as the source, following [its terms](https://www.raisg.org/en/maps/) |
| Mining concessions | [Global Forest Watch](https://data-api.globalforestwatch.org/dataset/gfw_mining_concessions) | [Public 2025 ZIP](https://gfw2-data.s3.amazonaws.com/concessions/2025/final_layers/public/gfw_global_mining_concessions_v2025_public.zip) | CC BY 4.0, except the Indonesia data |
| Logging concessions | [WRI Resource Watch](https://api.resourcewatch.org/v1/dataset/62c3d70c-d218-458f-8342-ee6a2b0ba434) | [Public Carto table](https://wri-01.carto.com/tables/gfw_logging) | Check the WRI dataset record |
| HydroRIVERS (South America) | [HydroSHEDS](https://www.hydrosheds.org/products/hydrorivers) | [Shapefile ZIP](https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_sa_shp.zip) | Check the HydroSHEDS terms |
| USGS mineral deposits | [USGS MRDS](https://www.usgs.gov/publications/mineral-resources-data-system-mrds) | [mrds-trim.zip](https://mrdata.usgs.gov/mrds/mrds-trim.zip) | Public domain |
| OpenStreetMap roads | [OpenStreetMap](https://www.openstreetmap.org/) via [Geofabrik](https://download.geofabrik.de/south-america.html) | Shapefile packages for Bolivia, northern Brazil, Colombia, Ecuador, Guyana, French Guiana, Peru, Suriname and Venezuela | [ODbL](https://www.openstreetmap.org/copyright). Credit OpenStreetMap contributors. Sharing a derived database carries share-alike terms. |
| Administrative boundaries | [GADM](https://gadm.org) | GADM 4.1 world GeoPackage, dissolved to levels 1 and 2 for the nine Amazon countries | Free for academic and other non commercial use; no redistribution ([licence](https://gadm.org/license.html)). [geoBoundaries](https://www.geoboundaries.org/) (CC BY 4.0) is the alternative if commercial use is needed. |
| Population | [Kontur](https://www.kontur.io/portfolio/population-dataset/) via [HDX](https://data.humdata.org/organization/kontur) | Per country GeoPackages, release 2023-11-01 | CC BY 4.0 |
| Threatened species records | [GBIF](https://www.gbif.org) | Occurrence search API: IUCN CR and EN, since 2000, nine countries (`fetch_gbif.py`) | Each record keeps its own licence (CC0, CC BY or CC BY-NC), stored in the tiles. Cite GBIF.org; a citable download with a DOI needs a GBIF account. |
| Peru native communities | [GEOCATMIN](https://geocatmin.ingemmet.gob.pe/geocatmin/) | [COFOPRI layer](https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_OTRAS_FUENTES/MapServer/45) | No reuse licence stated in the service metadata. Confirm terms before redistributing. |

Each layer's credit line shows on the map while the layer is on.

Layers you upload yourself under [My layers](../user-guide/my-layers.md) are your own data. GeoTALOS does not check their licence, so make sure you may use them.

## Datasets considered but not served

| Dataset | Status | Reason |
|---|---|---|
| WDPA (World Database on Protected Areas) | Not included | Its [terms](https://www.protectedplanet.net/c/terms-and-conditions) do not allow redistribution, including as downloadable map tiles, without written permission from UNEP-WCMC. |

## Models

GeoTALOS does not ship model weights. These are the models used in the paper and the training pipeline, with their official sources:

| Model | Source |
|---|---|
| YOLO | [Ultralytics](https://github.com/ultralytics/ultralytics) |
| SAM 3 | [Meta SAM 3](https://github.com/facebookresearch/sam3). The checkpoint is gated: [request access on Hugging Face](https://huggingface.co/facebook/sam3). |
| DINOv2 (training backbone) | [facebook/dinov2-small](https://huggingface.co/facebook/dinov2-small), [facebook/dinov2-base](https://huggingface.co/facebook/dinov2-base) |

Check each model's licence before using it commercially.

## Imagery used in the paper

The paper thanks the Sabin Center for Environment and Sustainability at Wake Forest University for access to the ecological data used. The multi-prompt segmentation workflow uses the ELDOR dataset (Kotsimba site) of gold mining in the Amazon. These are not distributed with GeoTALOS.

## Rebuilding the reference layers

The scripts in `scripts/reference_layers/` of [GeoTalosProd](https://github.com/spygaurad/GeoTalosProd) download these sources and rebuild the layers. See [Tiles, caching and reference layers](../developer/tiles.md).
