# Temporal analysis

When you have imagery of the same place from several dates, GeoTALOS lines it up in date order so you can step through it and see what changed: forest cleared, a mining pit growing, a wetland drying out.

## What you need

- **Several images of the same area from different dates.** They can be in one dataset or several.
- **Correct capture dates.** GeoTALOS reads them from the file names or the GeoTIFF itself. If a date is missing, the image gets its upload time and lands in the wrong place on the timeline. See [Capture dates](uploading-imagery.md#capture-dates).
- **An area of interest** drawn around the place you want to follow.

## Open Temporal Playback

1. Select your AOI on the map.
2. Open **Temporal Playback** in the panel on the right.
3. Choose what to show under **Index** (below).
4. The timeline opens at the bottom of the map with every date that has imagery inside the AOI.

> **Screenshot:** the timeline under the map, with an AOI shown in NDVI colours.

## Playing through time

| Control | Does | Keyboard |
|---|---|---|
| **Play** / **Pause** | Steps through the dates automatically | Space |
| **Previous** / **Next** | Moves one date back or forward | ← / → |
| **From date** / **To date** | Limits playback to a date range | |
| **Clear filter** | Removes the date range | |
| Annotation sets toggle | Shows your annotations at each date, or hides them to see only the imagery | |
| **Close timeline** | Closes playback | |

The AOI stays in the same place on every date, so changes you see come from the land, not from a different crop of the image.

## Index: what colours mean

**RGB (true colour)** shows the imagery as a photo. The other options turn each image into a map of one property, calculated from its bands:

| Index | Shows | Needs these bands | Low end of the colours | High end |
|---|---|---|---|---|
| **NDVI** | Vegetation greenness and vigour | Near-infrared, red | Bare or stressed | Healthy canopy |
| **GNDVI** | Chlorophyll and nitrogen content | Near-infrared, green | Low chlorophyll | High chlorophyll |
| **NDRE** | Canopy stress, sees into dense canopy | Near-infrared, red edge | Stressed | Vigorous |
| **NDMI** | Canopy moisture and drought stress | Near-infrared, shortwave infrared | Dry or water-stressed | High moisture |
| **NDWI** | Open water: ponds, flooding, wetlands | Green, near-infrared | Land | Open water |
| **NBR** | Burned areas and fire severity | Near-infrared, shortwave infrared | Burned | Unburned or healthy |

A colour legend on the map explains each index's scale.

GeoTALOS tries to find the right bands on its own. If it guesses wrong, or your sensor stores bands in an unusual order, pick them by hand.

!!! note "Ordinary drone photos"
    A standard RGB drone camera records red, green and blue only, with no near-infrared. With that imagery you can use **RGB (true colour)**, but the vegetation indices need a multispectral camera or satellite data.

### Threshold

The **Threshold** slider hides values below a level you choose. On NDVI, for example, raising it hides bare ground and stressed vegetation so only healthy canopy stays coloured. Step through the dates with the same threshold to compare how much healthy canopy remains on each one.

## Other analysis on an AOI

The same AOI panel has:

- **Area Statistics**: summary values for the AOI.
- **Change Detection**: compares the AOI between dates.
- **Composite**: combines several images into one.

## Run models through time

To detect objects on every date (for example, mining pits on each image in a series), run a model with **Run on collection** ticked. Each date gets its own annotation set, and playback shows them in step with the imagery. See [Running models](running-models.md).

For a repeatable version, see the [Temporal feature mapping](../tutorials/temporal-feature-mapping.md) and [NDVI monitoring](../tutorials/ndvi-monitoring.md) tutorials.
