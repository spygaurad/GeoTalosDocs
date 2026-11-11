# Developer Guide

- [Architecture](architecture.md): The four tiers (client, API, execution, data and storage) and the technology stack.
- [Local setup and deployment](local-setup.md): Running the full stack with Docker Compose.
- [Multi-tenancy](multi-tenancy.md): Clerk organizations, scoped tokens and PostgreSQL row-level security.
- [Data ingestion](data-ingestion.md): Chunked uploads, COG validation and the STAC catalog.
- [API endpoints](api.md): The FastAPI endpoints and how to call them.
- [Database schema and migrations](database.md): The application schema and working with Alembic migrations.
- [Adding a model](adding-a-model.md): Registering a model and writing its output adapter.
- [Model training pipeline](training-pipeline.md): Training and retraining models from reviewed annotations.
- [The workflow engine](workflow-engine.md): Graph validation, Celery queues and long-running jobs.
- [Tiles, caching and reference layers](tiles.md): Raster tiles with titiler, annotation vector tiles, versioned caching and reference layers.
