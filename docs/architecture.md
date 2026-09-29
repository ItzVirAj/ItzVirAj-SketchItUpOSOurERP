# SketchItUp Owner OS architecture

Owner OS is a modular monolith. Domain modules own their implementations and expose small interfaces to other modules.

## Seams
- HTTP seam: authenticated FastAPI routes.
- Persistence seam: PostgreSQL adapters.
- Policy seam: centralized server-side authorization.
- Audit seam: immutable audit events.

The design follows deep-module discipline: small interfaces, high leverage, strong locality, and tests crossing the same seam as callers.
