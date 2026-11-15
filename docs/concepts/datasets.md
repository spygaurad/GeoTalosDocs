# Datasets and the data library

A **dataset** is a collection of imagery, for example all drone orthomosaics from one field site. Each image inside it is a **dataset item**.

## What counts as imagery

GeoTALOS works with georeferenced raster imagery: satellite scenes, drone orthomosaics and other aerial images. Images are stored as **Cloud Optimized GeoTIFFs (COGs)**, a GeoTIFF format that lets GeoTALOS read only the part of the image on screen instead of loading the whole file.

## What happens when you upload

When you upload a new image, GeoTALOS:

1. Uploads the file in parts, so large files can be sent reliably and a failed part is retried.
2. Checks that the image is a valid COG.
3. Reads its location, extent and bands.
4. Adds it to the **data library**, where you and your team can search for it and use it in workflows.

See [Uploading imagery](../user-guide/uploading-imagery.md) for the steps.

## The data library

The data library is the catalogue of every dataset in your organization. You can search it by area, select dataset items and add them to a map or a workflow. Because the original images stay in storage and are shown on demand, even very large orthomosaics stay quick to pan and zoom.

## Dates matter

Each dataset item keeps its acquisition date. GeoTALOS uses these dates to order imagery in time, which is what makes [temporal analysis](../user-guide/temporal-analysis.md) possible.
