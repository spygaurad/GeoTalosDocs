# Provenance

**Provenance** is the record of where a result came from. For every result, GeoTALOS keeps track of:

- the **imagery** that was used,
- the **model** that was run, and which version,
- the **workflow** and the settings of each step,
- any **intermediate outputs**,
- each **version of the annotations**, and
- the **review decisions** experts made.

## Why it matters

When a result is used to make a decision, people need to know what supports it. If an area is flagged for possible illegal mining, for example, a reviewer may need to see which image was used, which model flagged it, and who checked the result.

You do not need to do anything to collect provenance. GeoTALOS records it automatically as workflows run and annotations are reviewed.
