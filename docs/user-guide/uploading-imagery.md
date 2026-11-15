# Uploading imagery

Upload your drone orthomosaics or satellite scenes from the **Datasets** page. Each upload becomes a dataset that you can add to any map or workflow in your organization.

## What you can upload

| File | Use |
|---|---|
| `.tif`, `.tiff`, `.geotiff` | One georeferenced image |
| `.zip` | Many images at once (see [Uploading many images](#uploading-many-images)) |

To bring in existing labels (a GeoJSON FeatureCollection), import them into an annotation set instead. See [Reviewing annotations](reviewing-annotations.md).

Images must be **georeferenced** GeoTIFFs, so GeoTALOS knows where they belong on the map. Cloud Optimized GeoTIFFs (COGs) work best. A plain GeoTIFF is accepted, but it loads slowly on the map (see [Making files load fast](#making-files-load-fast)).

## Upload a file

1. Open **Datasets** in the sidebar and start an upload.
2. Choose or drag in your file.
3. Fill in the form:
    - **Dataset name**: filled in from the file name. Change it to something your team will recognise.
    - **Type**: **Imagery** for photos and satellite scenes, or **Segmentation mask** for a raster where each pixel value is a class.
    - **Tags** (optional): words to find the dataset later, for example `drone`, `2024`, `site-a`. Press Enter after each tag.
4. Start the upload. Large files go up in parts, so a slow connection only resends the part that failed.

> **Screenshot:** the upload form with name, type and tags.

## What happens next

After the upload, GeoTALOS processes the file in four stages, shown as a progress list:

| Stage | What GeoTALOS does |
|---|---|
| **COG validation** | Checks the file is a readable raster |
| **Metadata extraction** | Reads its location, coordinate system, bands and capture date |
| **STAC registration** | Adds it to the imagery catalogue so it can be searched |
| **Dataset update** | Marks the dataset ready |

When it finishes you see "Dataset ingested and ready for visualization." with two buttons: **View dataset** and **Add to map**.

> **Screenshot:** the progress list and the ready message.

If you see **Upload failed**, the file could not be read as a georeferenced raster. Check it opens in QGIS with the right location, then try again.

## Capture dates

GeoTALOS orders imagery by its capture date, which is what makes [temporal analysis](temporal-analysis.md) work. It reads the date from:

1. the start of the file name, as `YYYYMMDDTHHMMSSZ_name.tif`,
2. the date stored inside the GeoTIFF, if your software saved one,
3. a date anywhere in the file name, such as `2024-05-12`, `20240512` or `2024-05`.

If it finds none, it uses the **upload time**, and every scene then appears on the same date.

!!! tip "Put the date in the file name"
    Name each file with its capture date, for example `2024-05-12_site_a.tif`. It is the most reliable way to keep your time series in order.

## Uploading many images

Put the GeoTIFFs in a `.zip` file and upload it as one dataset.

- **All files in one folder** (or no folders): they become one dataset.
- **Several top-level folders**: each folder becomes its own dataset. Use this to upload, for example, one folder per field site in one go.

## Making files load fast

Plain GeoTIFFs are accepted, but GeoTALOS warns when a file is not tiled, has no overviews or is not compressed. Those files work but draw slowly at low zoom. To convert one to a COG:

- **QGIS**: right-click the layer, **Export > Save As...**, choose GeoTIFF and set the format option `COG`.
- **Command line**: `gdal_translate -of COG input.tif output.tif`

Then upload the converted file.

## Related

- [Datasets and the data library](../concepts/datasets.md)
- [The map workspace](map-workspace.md)
- For developers: [Data ingestion](../developer/data-ingestion.md)
