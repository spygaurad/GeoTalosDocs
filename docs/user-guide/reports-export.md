# Reports and export

GeoTALOS gives you results in two forms: **reports** that summarise what was found, and **GeoJSON exports** you can open in QGIS, ArcGIS or a field app.

## Reports

Reports are made by the **Generate Report** node at the end of a workflow. See [Building workflows](building-workflows.md).

### What a report contains

- A title block.
- **One section per annotation set** connected to the node, with the total count and, if turned on, a **per-class breakdown** (how many annotations of each class).
- Optionally, **one row per annotation**.
- If a quality node is connected (for example **Raster Mask Metrics**), a metrics section with an overall summary and per-class IoU, precision, recall and F1.

Connect several **Run Inference** outputs to one Generate Report node to compare their results side by side, for example one section per AOI.

### Settings

| Setting | Default | Meaning |
|---|---|---|
| **Report Title** | Annotation Report | The heading of the report |
| **Per-Class Breakdown** | on | Counts for each class |
| **Include Annotation Rows** | off | A row for every annotation. Turn it on only for small sets, since large sets make long reports. |

### View and download

1. Run the workflow.
2. Open the run from the run history.
3. Open the Generate Report step to see the report.
4. Click **Download PDF** for a formatted copy with tables, ready to share.

> **Screenshot:** a report with two AOI sections and the Download PDF button.

The [Multi-AOI palm analysis](../tutorials/multi-aoi-palm-analysis.md) tutorial builds a report like this, one section per AOI.

## GeoJSON export

GeoJSON keeps each annotation's shape, class and properties, and opens in most GIS tools.

### One annotation set, from the map

On the annotation set's layer, click **Download GeoJSON**. Do this after review, so the file contains checked results. See [Reviewing annotations](reviewing-annotations.md).

### From a workflow

| Node | Exports |
|---|---|
| **Export Annotations** | An annotation set as GeoJSON |
| **Export Dataset Items** | The selected dataset items as a downloadable GeoJSON |

After the run, open the export step in the run history and use its download link.

Combine an export node with **Filter Annotations** to export only some annotations, for example only verified palms with a confidence of at least 0.8. This is the **Filter + export annotations** recipe.

### Using the file in QGIS

1. In QGIS, open **Layer > Add Layer > Add Vector Layer**.
2. Choose the downloaded `.geojson` file.
3. The annotations appear in their real location, in WGS 84 (EPSG:4326). QGIS reprojects them to your project's coordinate system if needed.

## Sharing results

- **Within GeoTALOS:** everyone in your organization can open the same map and annotation sets. No export is needed.
- **Outside GeoTALOS:** send the PDF report for people who need the numbers, and the GeoJSON for people who need the shapes.
- **Automatically:** send results to another system with a **Send Webhook** node. See [Automation](automation.md).
