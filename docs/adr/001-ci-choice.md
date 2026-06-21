# ADR 001 — CI Tooling: Jenkins + GitHub Actions in Parallel

## Status
Accepted

## Context
SecureTaskFlow needs CI/CD that builds, tests, and security-gates every change.
Beyond the technical need, this project is a portfolio piece: a prior interview
exposed a gap in CI tool comparison and pipeline internals. One CI tool would
meet the build/test need but not the comparison need. The goal is to demonstrate
understanding of CI *paradigms*, not familiarity with a single product.

Two models were considered:
- Self-hosted, server-based CI (Jenkins)
- Managed, config-as-code CI native to the code host (GitHub Actions)

## Decision
Run Jenkins and GitHub Actions in parallel against the same codebase, with the
same stages (Checkout -> Build -> Test -> Lint -> Push). Jenkins is primary; the
GitHub Actions workflow mirrors it.

## Consequences
- Two pipeline definitions must be kept in sync — real maintenance overhead.
  Accepted, because maintaining both is itself the portfolio signal: it proves
  understanding of both paradigms rather than one tool.
- Jenkins gives full control (self-hosted agent, Docker socket, explicit Groovy
  stages, credentials binding) at the cost of owning the server and its upkeep.
  It suits enterprise, regulated, and air-gapped environments.
- GitHub Actions gives zero-infra, YAML config-as-code, marketplace actions, and
  matrix builds, at the cost of less control and vendor coupling.
- Known limitation: the Jenkins job currently checks out from a local
  file:///home/admin/securetaskflow repository (a Day-1 local-checkout holdover),
  not the GitHub remote. Follow-up: point Jenkins at the GitHub remote and add a
  webhook so pushes trigger builds, matching how GHA already behaves.
- If forced to pick one for a real team: GitHub Actions for a GitHub-hosted
  project (lower ops burden); Jenkins where self-hosting or complex
  orchestration is required.

## Related
- docs/jenkins-vs-gha.md — detailed side-by-side comparison and build-time data
