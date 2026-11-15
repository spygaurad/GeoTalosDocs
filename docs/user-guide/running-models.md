# Running models

A model looks at your imagery and finds things for you: palm crowns, buildings, water, mining pits. GeoTALOS runs the model inside an area of interest and puts every prediction on the map as a draft annotation for you to check.

The models available depend on what your organization has set up. In the paper, GeoTALOS uses **YOLO** for detecting objects such as palm crowns and **SAM3** for outlining features from a text description. See the list under **AI Models** in the sidebar.

## Before you start

You need:

- a map with imagery on it (see [Getting started](getting-started.md)),
- an [area of interest](../concepts/aois.md) drawn around the part you want to analyse.

Running a model only inside an AOI is faster and avoids results you do not need.

## Run a model on an AOI

1. Select your AOI on the map.
2. Open **Run Inference** in the panel on the right.
3. Choose the **Model**.
4. Choose the **Dataset** to run it on.
    - For a dataset with imagery from several dates, tick **Run on collection** to run the model on every date in the series. Each date gets its own annotation set, grouped for [temporal playback](temporal-analysis.md). This takes longer than running on the AOI's images only.
5. Fill in the model's options (below).
6. Click **Run on AOI**.

> **Screenshot:** the Run Inference panel with a model and dataset selected.

The run continues in the background, so you can keep working on the map. It appears in the list under the panel. When it finishes, its results are added to the map as a new annotation layer. Use **Show overlay on map** and **Hide overlay on map** to toggle them.

## Model options

### Prompt-based models (such as SAM3)

| Option | What to enter |
|---|---|
| **Output class** | The class every prediction gets, for example "Water body". Pick it from your annotation schema. |
| **Text prompt** (optional) | What to look for, in plain words, for example "water, pond" or "rooftop, buildings" |
| **Bbox prompts** (optional) | Example boxes you draw around a few target objects. Only the parts of the image near your boxes are sent to the model. |

Give at least a text prompt or one box.

To map several classes at once (for example buildings, water bodies and crops), run one prompt per class, each with its own **Output class**. The [Multi-prompt segmentation](../tutorials/multi-prompt-segmentation.md) tutorial does this in a workflow.

### Scanning settings

| Option | Meaning |
|---|---|
| **Scales to scan** | Object sizes to look for. Each scale scans the whole AOI, so more scales take longer. Results are merged across scales. |
| **Patch size** | How large each piece of image sent to the model is. Leave the model default unless you know the model needs another size. |
| **Stride** | How far apart the pieces are. A smaller stride overlaps pieces more and catches objects on their edges, but takes longer. |

## What you get

Every prediction becomes an annotation with a class, a **confidence** score (how sure the model is, from 0 to 1) and a link to the model run that made it.

Model results are **drafts**. Check them before using them: remove false detections, add missed ones, fix outlines. See [Reviewing annotations](reviewing-annotations.md).

## Common messages

| Message | What to do |
|---|---|
| **Draw an AOI first** | Draw and select an area of interest |
| **No dataset items in this AOI** | Move the AOI over your imagery, or add a dataset that covers it |
| **Pick a model** / **Pick a dataset** | Choose one in the form |
| **Enter a text prompt or draw at least one bbox prompt** | Prompt-based models need one of the two |
| **Failed to start inference** | The model service may be unavailable. Try again, or ask your administrator. |

## More tools in the same panel

The **Run Inference** panel also has tools for more advanced work:

- **Auto annotate**: label the AOI automatically for a class you pick, using an annotation collection.
- **Similarity search**: pick one object and find others that look like it in the AOI.
- **Anomaly detection**: flag predictions that look unlike the rest of their class.
- **Train a head**: train a model for your own class from reviewed annotations. See [Model training pipeline](../developer/training-pipeline.md).

## Run models automatically

To run the same model every time new imagery arrives, build it into a workflow. See [Building workflows](building-workflows.md) and [Automation](automation.md).
