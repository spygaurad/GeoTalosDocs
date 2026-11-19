# Temporal feature mapping

Map the same feature on every date in an image series, then step through time to see how it changed: a mining pit growing, a river shifting, forest being cleared.

| | |
|---|---|
| **You will** | Run a model on every image in a date-ordered series inside one AOI, play the results through time and measure the change |
| **You need** | Several images of the same area from different dates, with correct capture dates, a saved AOI and a segmentation or detection model |
| **Based on** | The temporal feature mapping workflow in the GeoTALOS paper (Figure 7) |

In the paper, the series runs from December 2023 to August 2025, and segmentation is applied to each date to follow landscape change at a mining site.

## How it works

```text
Date-ordered images → clip each to the AOI → segment each date → one layer per date → temporal map view
```

Each derived layer stays linked to the capture date of its source image, so the map can play them in order.

## Step 1: Check your dates

Upload the images and confirm each one has the right capture date. Name files with their date, such as `2024-05-12_site.tif`, so GeoTALOS orders them correctly. See [Capture dates](../user-guide/uploading-imagery.md#capture-dates).

## Step 2: Draw the AOI

Draw and save an AOI around the area you want to follow. It must sit over all the images, so every date is cut to the same area. Then differences between dates come from the land, not from a different crop.

## Step 3: Segment every date

### On the map

1. Select the AOI and open **Run Inference**.
2. Choose the model, for example SAM3 with a text prompt such as `open pit, bare soil`, and the output class.
3. Choose the dataset and tick **Run on collection**. This runs the model on every date in the series, each clipped to the AOI. The option only appears for a dataset with images from several dates.
4. Click **Run on AOI**.

Each date gets its own annotation set, grouped for playback. This takes longer than a single run, since every image is processed.

### As a workflow

For a repeatable version:

1. **Load Saved AOI Timeline**: set **Map** and **Saved AOI**. It returns the AOI's images in date order.
2. **Run Inference**: connect **Dataset Items** to **Dataset Items** and **Map Selection** to **Area of Interest**, and set the model.
3. **Overlay on Map**: show the results.

## Step 4: Play it through time

1. Select the AOI and open **Temporal Playback**.
2. Keep the index on **RGB (true colour)** to see the imagery, with your annotation layers on top.
3. Press **Play** (or Space), or step with **Previous** and **Next** (← and →).
4. Use **From date** and **To date** to focus on one period.

Watch for features that appear, grow or disappear. See [Temporal analysis](../user-guide/temporal-analysis.md).

## Step 5: Measure the change

Add analysis nodes to the workflow to put numbers on what you saw:

| Node | Settings | Gives |
|---|---|---|
| **Timeseries Analysis** | **Metric**: count, area or confidence. **Group By**: day, week or month. | The metric for each period, for example the mapped area per month |
| **Change Detection** | **Before Annotation Set** and **After Annotation Set**; **Detection Method** (geometry difference or raster threshold); **Overlap Threshold**; **Minimum Change Area (sq m)** | The areas that changed between two dates, and change metrics |

Connect either to **Generate Report** to get a table you can share. See [Reports and export](../user-guide/reports-export.md).

!!! tip
    Set **Minimum Change Area** above the size of small segmentation errors, so the report shows real change instead of noise along edges.

## Rule-based instead of a model

For vegetation, water or burned areas, you may not need a model at all. Spectral indices such as NDVI and NDWI show change directly on multispectral imagery. See [NDVI monitoring](ndvi-monitoring.md).
