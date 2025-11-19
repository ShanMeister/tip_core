# tip_core — Threat Intelligence Platform (TIP) Core

tip_core is the core implementation for a Threat Intelligence Platform focused on global threat-data ingestion, normalization, enrichment, storage, and presentation. This README concentrates on technical design, system architecture, data contracts, and operational concerns required to run and extend the platform.

## Summary

- Collect heterogeneous threat intelligence (feeds, OSINT, sensors).
- Normalize raw items into a canonical schema.
- Enrich indicators with contextual data (GeoIP, ASN, WHOIS, reputation).
- Deduplicate and link related objects.
- Index and store data for fast search, analytics, and downstream export.

## High-level architecture

- Collectors: source-specific adapters that pull/push raw payloads and checkpoint progress.
- Message bus: Kafka or RabbitMQ to decouple ingestion and processing and provide durable buffering.
- Parsers: deterministic transforms from raw payload to canonical objects (JSON Schema / pydantic models).
- Enrichers: staged, idempotent tasks (GeoIP, ASN, passive DNS, reputation) with caching and circuit-breakers.
- Deduplicator & Linker: canonical key hashing + similarity detection to merge duplicates and create relation edges.
- Storage:
  - Search: Elasticsearch / OpenSearch for full-text search, aggregations, and analytics.
  - Relational/Graph: PostgreSQL / Neo4j for structured relationships and complex link queries.
  - Object store: S3-compatible for raw payloads and attachments.
  - Cache: Redis for enrichment TTLs and rate-limiting state.
- API: REST (FastAPI) or GraphQL exposing search, entity detail, and export endpoints.
- UI: lightweight static components for triage and exploration; dashboards driven by API queries.
- Exporters: connectors for STIX, MISP, SIEM, and SOAR.

Data flow: Source → Collector → Message Bus → Parser → Enricher(s) → Deduper/Linker → Store → API/UI/Exporters

## Canonical data model (concise)

Canonical objects follow a minimal, schema-driven design inspired by STIX2 for interoperability.

Indicator
- id: uuid
- type: ipv4 | domain | url | hash | email | asn
- value: string (normalized)
- first_seen, last_seen: ISO8601
- confidence: integer 0–100
- score: integer 0–100
- sources: [{ id, name, confidence }]
- enriched: { asn, country, whois_summary, passive_dns }
- related_ids: [uuid]

Sighting
- id, observed_at, observer, raw_payload_ref, indicator_id

ThreatActor / Campaign
- id, name, aliases, techniques, linked_indicators

Minimal indicator example:
```json
{
  "id": "uuid-1234",
  "type": "ipv4",
  "value": "203.0.113.10",
  "first_seen": "2025-11-10T12:00:00Z",
  "last_seen": "2025-11-12T09:30:00Z",
  "confidence": 70,
  "score": 85,
  "sources": [{"id":"feed-abc","confidence":60}],
  "enriched": {"asn":64500,"country":"US"}
}
```

## Key algorithms and implementation notes

- Normalization:
  - Type-specific canonicalizers (lowercase domains, punycode handling, URL parsing/normalization, hash canonical form).
  - Remove noise and ensure deterministic representation before hashing/indexing.
- Deduplication:
  - Canonical key = SHA256 of deterministic field set (type, normalized value, source fingerprint).
  - Merge policy: source-weighted aggregation of confidence/score, preserve provenance list, update timestamps.
- Similarity / Clustering:
  - Use MinHash/LSH or token-based similarity for near-duplicate detection (URLs, payload signatures).
  - Maintain lightweight clustering metadata; create relation edges when similarity > threshold.
- Enrichment:
  - Idempotent enrichers that update only missing or stale fields.
  - Cache enrichment results in Redis with configurable TTL and LRU eviction.
  - Circuit-breakers and graceful degradation when external services are rate-limited or unavailable.
- Indexing:
  - Bulk writes to Elasticsearch with backoff and retry; use refresh and routing strategies to balance freshness and throughput.
  - Separate hot/cold indices for retention and cost control.
- Backpressure and scaling:
  - Monitor message-bus lag and scale worker replicas based on lag thresholds.
  - Partition consumers for parallel processing with ordering guarantees where required.

## Operational and security considerations

- Authentication & Authorization:
  - OIDC for API and UI (Keycloak recommended).
  - RBAC with scoped roles for analysts, triage, and admins.
- Transport & Secrets:
  - TLS for all internal/external traffic; secrets in Vault or cloud secret manager.
- Data governance:
  - Retention policies that archive raw payloads to S3 and prune indices.
  - Provenance metadata for each object to support audits and takedowns.
- Hardening:
  - Input sanitization before rendering untrusted content.
  - Least privilege for service accounts accessing message bus and storage.
  - Rate-limiting for external enrichment calls and export endpoints.
- Auditing & compliance:
  - Immutable audit logs for CRUD operations on canonical objects.
  - Export controls and traceability for shared intelligence.

## Observability & monitoring

- Metrics:
  - Prometheus metrics for throughput, queue lag, parse/enrich latencies, error rates.
- Tracing:
  - OpenTelemetry tracing across collectors, workers, and API to correlate object lifecycle.
- Logs:
  - Structured JSON logs with correlation_id (object id) and worker_id.
- Dashboards & alerts:
  - Grafana dashboards for system health.
  - Alerts on queue lag, parsing error surge, enrichment failures, and indexing errors.

## Testing strategy

- Unit tests: canonicalizers, parsers, enrichment adapters, deduplication logic.
- Contract tests: JSON Schema / pydantic validation for canonical objects.
- Integration tests: local message-broker + test ES/Postgres via docker-compose.
- E2E smoke tests: ingest a sample feed and validate end-to-end object creation, enrichment, and API response.
- CI pipeline: lint, unit tests, schema validation, build UI assets, run integration smoke tests.

## Suggested technology choices

- Message bus: Kafka (throughput) or RabbitMQ (simplicity).
- Backend: Python + FastAPI or Node.js + Nest/Express.
- Search: Elasticsearch / OpenSearch.
- Relational/graph: PostgreSQL (with graph extensions) or Neo4j for heavy relationship queries.
- Cache: Redis.
- Object storage: S3-compatible.
- Orchestration: Kubernetes; use Helm charts for deployment.
- Observability: Prometheus + Grafana + OpenTelemetry.

## API examples (representative)

- Search indicators
  - GET /api/v1/indicators?q=malicious.example&type=domain&from=2025-11-01&to=2025-11-19
- Get indicator detail
  - GET /api/v1/indicators/{id}
- Export results
  - POST /api/v1/export
    - body: { "query": "...", "format": "stix" }

Example indicator detail:
```json
{
  "id": "uuid-1234",
  "type": "domain",
  "value": "malicious.example",
  "score": 92,
  "first_seen": "2025-10-01T00:00:00Z",
  "enriched": {"asn": 64500, "country": "CN", "whois": {...}},
  "sources": [{"id":"feed-xyz","confidence":80}]
}
```

## Repository layout (recommended)

- collectors/       — feed adapters and fetch scripts
- parsers/          — normalization rules and parser implementations
- enrichers/        — enrichment modules and adapters
- workers/          — pipeline workers and orchestration helpers
- api/              — backend service and API schema
- ui/               — static assets, components, demo pages
- schemas/          — JSON Schema / pydantic models
- deploy/           — Dockerfiles, k8s manifests, docker-compose
- tests/            — unit/integration/e2e tests
- docs/             — architecture and operational runbooks

## Quickstart (local prototype)

1. Clone repository:
```bash
git clone https://github.com/ShanMeister/tip_core.git
cd tip_core
```
2. Serve static UI demo:
```bash
python -m http.server 8000
# open http://localhost:8000/ui/ or demo index
```
3. Follow docs in /docs/ to run collector, parser, and a local broker + search instance with docker-compose when available.

## Contribution and license

- Follow feature-branch workflow and include tests for parsing and enrichment logic.
- Add or update JSON Schemas in /schemas/ when modifying canonical models.
- Add a LICENSE file to clarify usage and distribution terms.
