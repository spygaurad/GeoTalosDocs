# Multi-AOI palm analysis

Run the same palm model over several study areas at once and get one report with a section for each area. This is useful when you have no ground truth and want comparable counts across sites.

| | |
|---|---|
| **You will** | Build a workflow that detects palms in two AOIs, shows both results on one map and writes a per-AOI report |
| **You need** | An orthomosaic on a map, two or more saved AOIs, and a palm detection model (YOLO in the paper) |
| **Based on** | The multi-AOI palm analysis workflow in the GeoTALOS paper (Figure 4) |
| **Do first** | [Palm crown detection](palm-crown-detection.md) |

## How the workflow works

GeoTALOS clips the imagery to each AOI, runs the model on each clipped piece, overlays every result on the map and writes one report:

```text
Select Data Source (AOI 1) → Run Inference (YOLO) ─┐
                                                   ├→ Overlay on Map → Generate Report
Select Data Source (AOI 2) → Run Inference (YOLO) ─┘
```

> **Screenshot:** the workflow from Figure 4 of the paper.

## Step 1: Save the AOIs

On your map, draw each study area and save it, for example "AOI 1" and "AOI 2". Saved AOIs can be chosen in workflows. See [Areas of interest](../concepts/aois.md).

## Step 2: Create the pipeline

1. In your project's **Automations** tab, create a pipeline and name it, for example "Palm count by AOI".
2. Add two **Select Data Source** nodes.
3. Add two **Run Inference** nodes.
4. Add one **Overlay on Map** node and one **Generate Report** node.

## Step 3: Connect the nodes

1. Connect each **Select Data Source** node to its own **Run Inference** node: **Dataset Items** to **Dataset Items**, and **AOI / Selection** to **Area of Interest**.
2. Connect both **Run Inference** outputs (**Annotation Set**) to **Overlay on Map**.
3. Connect the **Pass-through** output of **Overlay on Map** to the **Annotation Sets** input of **Generate Report**.

## Step 4: Set each node

| Node | Setting |
|---|---|
| Select Data Source (first) | Your palm dataset, **AOI 1** |
| Select Data Source (second) | The same dataset, **AOI 2** |
| Run Inference (both) | Your palm model, for example YOLO |
| Overlay on Map | The map to show results on |
| Generate Report | **Report Title** (for example "Crown Center Detection"), **Per-Class Breakdown** on, **Include Annotation Rows** on if the areas are small |

## Step 5: Run it

Save and run. If you see **Graph validation failed**, the message names the node with a missing connection or setting.

When the run finishes:

- the map shows the detections from both AOIs, each inside its own area,
- the run history shows the report.

> **Screenshot:** the map with detections in AOI 1 and AOI 2.

## Step 6: Read the report

Open the **Generate Report** step in the run history. The report has one section per annotation set, so one per AOI, each with:

- the total number of detections,
- the count per class.

In the paper's example, the report counted 2,170 annotations, all of the class "Palm Tree".

Click **Download PDF** to share it. See [Reports and export](../user-guide/reports-export.md).

## Step 7: Review before you rely on the numbers

The counts come from unreviewed model output. Before using them in a study, review the detections in each AOI (verify true palms, delete false ones, add missed ones), then run the report again on the verified sets. See [Reviewing annotations](../user-guide/reviewing-annotations.md).

## Variations

- **More sites:** add one Select Data Source and Run Inference pair per AOI and connect each to Overlay on Map.
- **Every month:** add a **Trigger** node set to **recurring** and set the pipeline to **Active**. See [Automation](../user-guide/automation.md).
- **Area instead of count:** add **Area Calculation** after Run Inference.
