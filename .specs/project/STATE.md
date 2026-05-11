# State

**Last Updated:** 2026-05-11T00:00:00-03:00
**Current Work:** Project initialization — brownfield mapping

---

## Recent Decisions

### AD-001: Single .specs directory in project root (2026-05-11)

**Decision:** Place `.specs/` at project root (`/smaf/almoxarifado/.specs/`)
**Reason:** Keeps project context alongside source code, version-controlled, accessible to all tools
**Trade-off:** Adds top-level directory but stays hidden (dotfile)
**Impact:** All planning artifacts share the same repo as code

### AD-002: Brownfield mapping before feature work (2026-05-11)

**Decision:** Document existing codebase in 7 brownfield files before any feature work
**Reason:** This is an existing project with zero specs — must understand current state before adding features
**Trade-off:** Upfront documentation cost before visible feature delivery
**Impact:** Future features will reference these docs for decisions

---

## Active Blockers

None

---

## Lessons Learned

None

---

## Quick Tasks Completed

| # | Description | Date | Commit | Status |
|---|---|---|---|---|
| 001 | Initial brownfield mapping (7 files) + PROJECT.md + ROADMAP.md + STATE.md | 2026-05-11 | - | ✅ Done |

---

## Deferred Ideas

- None

---

## Todos

- [ ] User wants reports/relatórios improvement as next feature
- [ ] Data integrity (stock race condition) flagged as concern by user

---

## Preferences

**Model Guidance Shown:** never
