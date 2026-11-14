# Multi-prompt segmentation

Map several kinds of features in one area at once, such as buildings, water bodies and crops, by giving SAM3 a short text description for each. Then, if you have ground truth, measure how accurate the result is.

| | |
|---|---|
| **You will** | Build a workflow with one SAM3 branch per class, merge the results into one multi-class layer, and optionally score it against ground truth |
| **You need** | An orthomosaic or satellite scene on a map, a saved AOI, an annotation schema with your classes, and SAM3 registered as a model |
| **Based on** | The multi-prompt segmentation workflow in the GeoTALOS paper (Figure 6) |

In the paper, the image is `Kotsimba_cog.tif` from the "Kotsimba ELDOR Site" dataset, a mining site from the ELDOR dataset of gold mining in the Amazon.

## How the workflow works

One data source feeds three SAM3 branches. Each branch has its own text prompt and output class, and all three results land on one map:

```text
                     ┌→ Run Inference (SAM3: "Rooftop, Buildings" → Buildings) ─────┐
Select Data Source ──┼→ Run Inference (SAM3: "Water, pond" → Water Bodies) ─────────┼→ Overlay on Map
                     └→ Run Inference (SAM3: "Crops, Farm Crops" → Agricultural Crops)┘
```

> **Screenshot:** the workflow from Figure 6 of the paper.

## Step 1: Prepare the classes

In **Annotation Schemas**, make sure your schema has one class per feature, for example **Buildings**, **Water Bodies** and **Agricultural Crops**. Each SAM3 branch writes into one of these classes.

## Step 2: Build the workflow

1. In your project's **Automations** tab, create a pipeline.
2. Add one **Select Data Source** node. Set the dataset, the image and the AOI.
3. Add three **Run Inference** nodes and connect each to the Select Data Source node (**Dataset Items** to **Dataset Items**, **AOI / Selection** to **Area of Interest**).
4. Add one **Overlay on Map** node and connect all three **Run Inference** outputs to it.

## Step 3: Set each SAM3 branch

Choose SAM3 as the **AI Model** in all three Run Inference nodes, then give each one its own class and prompt:

| Branch | Output Class | Text prompt |
|---|---|---|
| 1 | Buildings | `Rooftop, Buildings` |
| 2 | Water Bodies | `Water, pond` |
| 3 | Agricultural Crops | `Crops, Farm Crops` |

The text prompt says what to look for; the output class is the label every result gets. Several prompts can target the same class.

!!! tip "Writing prompts"
    Use short, concrete words for what the feature looks like from above, and add a synonym or two separated by commas. If results are poor, try other words before changing anything else.

## Step 4: Run and review

Save and run. When it finishes, the map shows one layer per class, each in its class colour.

> **Screenshot:** buildings, water and crops segmented over the mining site.

Review each class: delete false shapes, draw missed ones and verify the rest. See [Reviewing annotations](../user-guide/reviewing-annotations.md).

## Step 5 (optional): Score it against ground truth

If you have a ground truth raster (a mask where each pixel value is a class), extend the workflow to measure accuracy, as in the paper:

1. **Upload the ground truth** as a dataset with the type **Segmentation mask**.
2. Add a **Rasterize Annotation Set** node. Connect the three Run Inference outputs to its **Annotation Sets** input. Set **Reference Dataset (grid)** to your ground truth so both rasters line up, and choose a **Resolution (m/pixel)**.
3. Add a **Raster Mask Metrics** node. Connect the rasterized result (**Mask Dataset**) to its **Model Output Mask** input and set **Ground Truth Dataset** to your uploaded mask.
4. Add a **Generate Report** node and connect **Metrics** to it.

```text
Run Inference (×3) → Rasterize Annotation Set → Raster Mask Metrics → Generate Report
```

The report lists, per class:

| Metric | Means |
|---|---|
| **Precision** | Of the pixels SAM3 labelled as this class, the share that were correct |
| **Recall** | Of the pixels that really are this class, the share SAM3 found |
| **F1** | Precision and recall combined in one number |
| **IoU** | How much the predicted area overlaps the true area |

It also gives the mean IoU across classes. Use these to compare prompts: change a prompt, run again, and keep the one with the higher IoU.

## Variations

- **More classes:** add another Run Inference branch per class.
- **Vector ground truth:** if your ground truth is an annotation set rather than a raster, use **Ground Truth Comparison** instead, with **Predictions** and **Ground Truth** inputs and an **IoU Threshold**.
