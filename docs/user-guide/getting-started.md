# Getting started

This page takes you from signing in to your first map.

New to the terms used here? Read [Key Concepts](../concepts/index.md) first.

## 1. Sign in

Open the GeoTALOS address your team gave you and sign in, or create an account. Sign-in is handled by Clerk, so you can use email or any sign-in option your team has turned on.

> **Screenshot:** the sign-in page.

## 2. Choose your organization

After signing in you see **Select your organization**.

- If your team already uses GeoTALOS, ask an admin to invite you. The organization then appears in the list.
- If you are the first person on your team, create a new organization. You become its admin.

Everything you upload or create belongs to the organization you pick here. You can switch organizations later. What you see always depends on the organization selected. See [Organizations, projects and roles](../concepts/organizations.md).

> **Screenshot:** the organization picker.

## 3. Find your way around

The sidebar on the left has three groups:

| Group | Item | What you do there |
|---|---|---|
| Explore | **Dashboard** | Quick access to common actions, such as **New map**, and your recent jobs |
| Data | **Projects** | Open or create a study |
| | **Datasets** | Upload and browse imagery |
| | **Annotation Schemas** | Define the classes you label, such as "Palm tree" or "Water body" |
| | **Annotation Sets** | Browse annotations made by people or models |
| Intelligence | **AI Models** | See the models your organization can run |

> **Screenshot:** the dashboard with the sidebar.

## 4. Create a project

A project holds one study: its imagery, maps and workflows.

1. Go to **Projects** and create a new project. Give it a name your team will recognise, for example "Palm monitoring, field site A".
2. Open it. A project has tabs for **Maps**, **Datasets**, **Automations** and **Members**.

## 5. Add imagery

1. Go to **Datasets** and create a dataset.
2. Upload your GeoTIFF files. Large files upload in parts, so a slow connection only retries the part that failed.
3. Wait until the dataset shows as **ready**. GeoTALOS checks each file and adds it to the catalogue.
4. Add the dataset to your project from the project's **Datasets** tab.

!!! tip "Name files with their date"
    Put the capture date in each file name, for example `2024-05-12_site_a.tif`. GeoTALOS uses it to order your imagery in time.

Full details: [Uploading imagery](uploading-imagery.md).

## 6. Open your first map

1. In your project, open the **Maps** tab and create a map.
2. Add your dataset as a layer. The imagery appears on the map and loads only the part you are looking at, so even very large orthomosaics stay quick.
3. Pan and zoom to your study area.

> **Screenshot:** a new map showing an orthomosaic.

From here you can draw an [area of interest](../concepts/aois.md), [run a model](running-models.md) or turn on [reference layers](reference-layers.md).

## Watch it in action

The [demo video](https://www.youtube.com/watch?v=KoLlAJi2LYg) shows the map workspace, model runs and workflows in 17 minutes.

## Next steps

- [The map workspace](map-workspace.md): every tool on the map
- [Palm crown detection](../tutorials/palm-crown-detection.md): a first full workflow, step by step
