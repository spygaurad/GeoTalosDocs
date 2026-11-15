# The map workspace

The map is where most work in GeoTALOS happens: you look at imagery, draw study areas, run models, review results and compare dates, all on one screen.

Open a map from your project's **Maps** tab. **Back to project** returns you to the project.

> **Screenshot:** the full map workspace with the left panel, map and right panel.

## Layout

| Area | What it holds |
|---|---|
| **Toolbar** (top) | Pan and select, drawing tools, define an AOI, the data library, the basemap picker |
| **Layers panel** (left) | Every layer on this map, plus reference layers |
| **Map** (centre) | Your imagery and annotations |
| **Information panel** (right) | Details of whatever you select: location, properties, dataset info, annotation sets, visualization and model inference |

## Adding data

Open the **Library** ("add datasets & data sources") to add imagery from your organization's datasets. Use **Add annotation layer** to show an existing annotation set on the map.

Imagery loads only for the part of the map you are looking at, so large orthomosaics stay quick to pan and zoom.

## Layers panel

Each layer has a menu (**Layer actions**) with:

| Action | Does |
|---|---|
| **Zoom to layer** | Moves the map to the layer's extent |
| **Rename** | Changes the name shown in the panel |
| **Edit style** | Fill colour, stroke colour, line width, line style (solid, dashed, dotted, long dash) and fill opacity, for annotation layers |
| **Layer opacity** | Makes imagery partly transparent so you can compare it with what is underneath |
| **Remove from map** | Takes the layer off this map. The data itself is not deleted. |

Turn a layer on and off with its visibility toggle, and **drag to reorder** layers.

### Reference layers

The **Reference layers** section adds public context layers, such as Ramsar wetlands, protected areas, mining and logging concessions and rivers. See [Reference layers](reference-layers.md).

## Basemaps

Choose the background map from the basemap picker, for example **Voyager**.

## Drawing and measuring

The drawing tools create shapes on the map: **Point**, **Line**, **Polygon**, **Rectangle** and **Circle**.

Select a shape to see its measurements in the information panel: **Area**, **Perimeter**, **Length**, **Vertices**, and for circles the **Center**, **Radius** and **Diameter**.

Shapes are used for two things:

- **Areas of interest (AOIs):** saved study areas that focus searches, model runs and reports. See [Areas of interest](../concepts/aois.md).
- **Annotations:** labelled shapes such as a palm crown or a water body. See [Reviewing annotations](reviewing-annotations.md).

> **Screenshot:** drawing a polygon AOI, with its area and perimeter in the information panel.

## Selecting a feature

Click an annotation to see its properties: **Class**, **Label**, **Confidence**, **Source**, **Status**, and its location in **Longitude** and **Latitude**.

## Viewing imagery

With an image selected, the **Visualization** settings in the information panel change how it is drawn:

- **Bands**: choose which bands to show, for example natural colour or false colour.
- **Composite**: band combinations for multispectral imagery.
- **NDVI**: shows vegetation health from the red and near-infrared bands. It needs imagery with a near-infrared band.

The dataset info shows technical details such as the coordinate system (**CRS**) and ground sample distance (**GSD**, the size of one pixel on the ground).

## Comparing dates

When an AOI has imagery from several dates, **Temporal Playback** steps through them in date order, so you can watch change happen. See [Temporal analysis](temporal-analysis.md).

## Running a model from the map

The **Run Inference** panel runs a model on the imagery inside an AOI and adds the results as a new annotation layer. See [Running models](running-models.md).

## Analysis on an AOI

Select an AOI to open its analysis tools, such as **Area Statistics** and **Change Detection**.
