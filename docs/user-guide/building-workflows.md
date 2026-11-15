# Building workflows

A workflow (called a **pipeline** in the app) saves a procedure you would otherwise repeat by hand: choose imagery, run a model, put the results on a map, write a report. Build it once by connecting boxes, then run it again whenever you need, or automatically.

Workflows live in a project. Open the project and go to the **Automations** tab.

## The pipelines list

The **Automations** tab lists your project's pipelines with their status and trigger.

| Status | Meaning |
|---|---|
| **Draft** | Being built, not running automatically |
| **Active** | Runs on its schedule or event |
| **Paused** | Kept, but not running automatically for now |
| **Archived** | Kept for reference |

| Trigger | Starts when |
|---|---|
| **Manual** | You click run |
| **Schedule** | A set time, such as every Monday |
| **Event** | Something happens, such as a new dataset finishing ingestion |

Use **Search pipelines...** to find one, and **Rename**, **Duplicate** or **Delete** to manage them. Deleting needs the admin role.

## The editor

Opening a pipeline shows the editor:

- **Node catalog** (left): every node you can add, grouped by category, with a **Search...** box.
- **Canvas** (centre): your workflow. **Zoom in**, **Zoom out** and **Fit to view** are in the toolbar.
- **Run history**: open it with **Toggle run history**.

Click the pipeline's name to rename it.

> **Screenshot:** the editor with the node catalog, a three-node workflow and the run history.

## Build a workflow

1. **Add nodes** in any of three ways: drag from the catalog onto the canvas, right-click the canvas, or use the toolbar's add button.
2. **Connect them** by dragging from an output on one node to an input on the next. A **solid** line passes data; a **dashed** line is an event trigger.
3. **Set each node's options** by selecting it, for example which **Dataset**, **Saved AOI**, **Model**, **Annotation Set** or **Classes** to use.
4. **Save.** When you save or run, GeoTALOS checks the workflow. If something is missing, such as an unconnected required input or a missing setting, you see **Graph validation failed** with the reason. Nothing runs until it passes.
5. **Run** it. The status changes to **Running...** and the run appears in the run history.

## Node groups

| Group | Use for | Examples |
|---|---|---|
| Triggers | Starting a workflow | Trigger, On Dataset Ingested, On Annotation Created, On Threshold Breach |
| Data source | Choosing what to work on | Select Data Source, Select Annotation Set, STAC Search, AOI Filter |
| ML annotation | Running models | Run Inference |
| Map overlay | Showing and exporting results | Overlay on Map, Overlay Dataset on Map, Export Annotations, Export Dataset Items |
| Analysis | Measuring | Area Calculation, Timeseries Analysis, Zonal Statistics, Change Detection, Anomaly Detection |
| Data operations | Cleaning annotations | Filter Annotations, Merge Annotation Sets |
| Quality | Checking against ground truth | Ground Truth Comparison, IoU Threshold Gate, Duplicate Detection |
| Output | Sharing results | Generate Report, Send Webhook |

Some nodes in the catalog are not built yet, such as Send Email and the Advanced group. The developer page [The workflow engine](../developer/workflow-engine.md) lists which ones.

## Start from a recipe

The catalog shows recipes: common workflows with the nodes to connect.

| Recipe | Does | Nodes, in order |
|---|---|---|
| **Inference on an AOI** | Runs a model on an AOI and shows the results | Select Data Source, Run Inference, Overlay on Map |
| **Overlay dataset on map** | Adds imagery to a map | Trigger, Select Data Source, Overlay Dataset on Map |
| **Export dataset items** | Exports items as GeoJSON | Trigger, Select Data Source, Export Dataset Items |
| **STAC search + AOI filter** | Finds catalogue imagery for an area | Trigger, STAC Search, AOI Filter, Export Dataset Items |
| **Ground truth QA** | Compares predictions with ground truth | Select Annotation Set (twice), Ground Truth Comparison, IoU Threshold Gate, Export Annotations |
| **Filter + export annotations** | Keeps annotations by label or confidence | Select Annotation Set, Filter Annotations, Export Annotations |
| **Duplicate cleanup** | Finds duplicate annotations | Select Annotation Set, Duplicate Detection, Export Annotations |
| **Merge annotation sets** | Combines sets on a map | Select Annotation Set (twice), Merge Annotation Sets, Overlay on Map |
| **Scheduled monitoring** | Weekly inference with an area report | Trigger, Select Data Source, Run Inference, Area Calculation, Send Webhook |
| **Auto-overlay on ingest** | Adds new datasets to the map automatically | On Dataset Ingested, Overlay Dataset on Map, Send Webhook |
| **Change detection alert** | Compares two dates and reports changes | Trigger, Select Annotation Set (twice), Change Detection, Generate Report, Send Email |

!!! note
    The **Change detection alert** recipe ends with Send Email, which is not built yet. Use Send Webhook instead to get notified.

## Check the results

Open a run from the run history to see:

- its status (**Pending**, **Running**, **Completed**, **Failed** or **Cancelled**), **Started** time and **Duration**,
- each step's **Config**, **Outputs** and **Previews**, and any **Error**.

Results such as new annotation sets also appear on the map you chose.

## Next

- [Automation](automation.md): run workflows on a schedule or from events
- [Reports and export](reports-export.md)
- [Multi-AOI palm analysis](../tutorials/multi-aoi-palm-analysis.md): a full workflow, step by step
