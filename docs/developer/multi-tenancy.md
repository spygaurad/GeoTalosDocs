# Multi-tenancy

One GeoTALOS deployment serves many organizations. Each organization's data is isolated in the database, not only in application code.

## Identity: Clerk

Sign-in and organizations are handled by [Clerk](https://clerk.com). Every API request carries a Clerk JWT, and the token includes:

| Claim | Used for |
|---|---|
| `sub` | The user |
| `org_id` (v1) or `o.id` (v2) | The active organization |
| `org_role` (v1) or `o.rol` (v2) | The role in that organization: `admin`, `member` or `viewer` |

Both Clerk JWT formats are supported. A missing or unknown role is treated as `org:viewer`, the lowest role.

The first time a Clerk organization is seen, GeoTALOS creates a matching row in `organizations` automatically. The Clerk `organization.created` webhook later fills in the real name and slug.

## Request flow

```text
Request
 └── ClerkAuthMiddleware        validates the JWT
      └── get_session           opens a transaction and sets the RLS context
           └── get_current_user creates or updates the user and membership
                └── require_org_role(...)   checks organization + minimum role
```

These live in `app/api/deps.py` and `app/middleware/rls.py`.

## Row-level security

`set_rls_context` binds three PostgreSQL settings for the current transaction:

| Setting | Value |
|---|---|
| `app.current_org_id` | The organization's internal UUID |
| `app.current_user_id` | The Clerk user ID |
| `app.current_role` | `org:admin`, `org:member` or `org:viewer` |

Tenant-scoped tables have row-level security enabled, with select, insert, update and delete policies that compare each row's `organization_id` with `app.current_org_id` (migrations `019` and `020`). A query from one organization therefore cannot read or change another organization's rows, even if application code forgets a filter.

## Roles in endpoints

Endpoints declare the lowest role they accept with `require_org_role`:

```python
org_id: UUID = Depends(require_org_role("org:member"))
```

It returns the organization UUID, or responds `403` when there is no organization context or the role is too low. The ranking is `viewer < member < admin`. In the current code:

| Minimum role | Typical endpoints |
|---|---|
| `org:viewer` | Reading maps, layers, annotations and tiles |
| `org:member` | Creating and editing data, running jobs and workflows |
| `org:admin` | Deleting datasets, maps, models, projects and workflows; managing members and the organization |

## Where RLS does not apply

Two database roles carry `BYPASSRLS`, so isolation for them is enforced differently:

- **`celery_worker`** (background jobs): each job carries its organization ID, and the job code scopes its queries to that organization.
- **`martin_reader`** (vector tiles): Martin cannot see per-request RLS settings, so it is never exposed directly. Tile requests go through an authenticated API endpoint that checks the annotation set belongs to the caller's organization before forwarding to Martin. See [Tiles, caching and reference layers](tiles.md).

!!! warning
    When you add a worker task or a Martin source, add the organization check yourself. Row-level security will not catch it.
