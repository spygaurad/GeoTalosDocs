# Automation

Once a workflow works when you run it by hand, GeoTALOS can run it for you: on a timetable, or whenever something happens, such as new imagery arriving. This is how one-off analysis becomes ongoing monitoring.

Build and test the workflow first. See [Building workflows](building-workflows.md).

## Start a workflow on a timetable

Use the **Trigger** node at the start of the workflow and set **When to run**:

| Option | Runs | Settings |
|---|---|---|
| **manual** | Only when you click run | none |
| **once** | One time, at a date and time you choose | **Run At** |
| **recurring** | Repeatedly on a timetable | **Cron Expression** and **Timezone** |

### Cron expressions

A cron expression has five parts: minute, hour, day of the month, month, day of the week. Some useful ones:

| Expression | Runs |
|---|---|
| `0 0 * * *` | Every day at midnight (the default) |
| `0 9 * * 1` | Every Monday at 9:00 |
| `0 6 1 * *` | The 1st of every month at 6:00 |
| `0 */6 * * *` | Every 6 hours |

Set **Timezone** to your own (for example `America/New_York` or `Asia/Dhaka`). The default is `UTC`.

## Start a workflow when something happens

Replace the Trigger node with an event trigger:

| Node | Starts the workflow when | Optional filter |
|---|---|---|
| **On Dataset Ingested** | A dataset finishes uploading and processing | **Dataset**: only this dataset. Leave empty for any. |
| **On Annotation Created** | New annotations are added | **Schema Filter**: only sets using this annotation schema |
| **On Threshold Breach** | A measured value crosses a limit | **Metric**, **Operator** and **Value** (below) |

**On Dataset Ingested** passes the new dataset and its items to the next node, so a workflow such as "run the palm model on every new orthomosaic" needs no other input.

### Threshold breach

| Setting | Choices |
|---|---|
| **Metric** | `area_change_pct` (percentage change in area), `observation_count` (number of detections), `confidence_score` |
| **Operator** | greater than, greater or equal, less than, less or equal, equal |
| **Value** | The limit, for example `10` for a 10 percent area change |

For example, start a workflow only when a mining area has grown by more than 10 percent.

## Turn automation on

A scheduled or event workflow runs automatically only while its status is **Active**.

1. Open the project's **Automations** tab.
2. Set the pipeline to **Active**.
3. To stop it for a while, set it to **Paused**. Its settings and run history are kept.

Archiving or deleting a pipeline also stops its schedule.

## Get notified

Add a **Send Webhook** node at the end of the workflow:

| Setting | What to enter |
|---|---|
| **Webhook URL** | Where to send the results: your own server, or a service that accepts any JSON |
| **Custom Headers** | Optional, for example an authorization header your server expects |

GeoTALOS sends the previous node's results as JSON in a `POST` request. Chat apps such as Slack and Microsoft Teams expect their own message format, so send to a service that can reformat the data for them.

!!! note
    **Send Email** and **In-App Notification** appear in the node catalog but are not built yet. Use **Send Webhook** for notifications.

## Check what ran

Every automatic run appears in the pipeline's run history, the same as a manual run. Check it after the first few scheduled runs to confirm the workflow does what you expect. A **Failed** run shows which step failed and why.

## Example: weekly palm monitoring

1. **Trigger**: **recurring**, `0 9 * * 1`, your timezone.
2. **Select Data Source**: your palm dataset and AOI.
3. **Run Inference**: the palm detection model.
4. **Area Calculation**: total area of detected crowns.
5. **Send Webhook**: send the result to your server or notification service.

Set the pipeline to **Active**. Every Monday at 9:00 the latest numbers are sent, and the new detections are ready to review on the map.

This is the **Scheduled monitoring** recipe in the node catalog.
