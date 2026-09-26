# PiSentinel — Amala (C) Checklist
**Role:** Backend, Dashboard and Integration  
**Build window:** 21 Sep 2026 → 28 Feb 2027

## Current status
- [ ] FastAPI skeleton complete
- [ ] Database access layer complete
- [ ] Mock-event mode complete
- [ ] Dashboard shell complete
- [ ] Live API integration complete
- [ ] Timeline view complete
- [ ] Incident report generation complete
- [ ] Demo/simulation mode complete
- [ ] Integration tests complete

## 21–27 Sep — Application Contract
- [ ] Create backend module
- [ ] Create API specification file
- [ ] Review A's event schema
- [ ] Review B's prediction schema
- [ ] Review D's deception/evidence schema
- [ ] Define API error format
- [ ] Define health response
- [ ] Define event response schema
- [ ] Define session response schema
- [ ] Define prediction response schema
- [ ] Define evidence response schema
- [ ] Define response-action schema
- [ ] Define dashboard refresh strategy
- [ ] Document API version

## 28 Sep–11 Oct — FastAPI Skeleton
- [ ] Create FastAPI app
- [ ] Add `/health`
- [ ] Add `/events`
- [ ] Add `/sessions`
- [ ] Add `/sessions/{id}`
- [ ] Add `/system/status`
- [ ] Add OpenAPI tags
- [ ] Add request validation
- [ ] Add response validation
- [ ] Add API logging
- [ ] Add exception handler
- [ ] Add CORS configuration
- [ ] Add configuration loading
- [ ] Add local run command

## 12–25 Oct — Database Layer
- [ ] Create database module
- [ ] Create event repository
- [ ] Create session repository
- [ ] Create prediction repository
- [ ] Create evidence repository
- [ ] Create system-metrics repository
- [ ] Add event lookup by ID
- [ ] Add event lookup by session
- [ ] Add session-list query
- [ ] Add prediction lookup
- [ ] Add evidence lookup
- [ ] Add database error handling
- [ ] Add repository tests

## 26 Oct–8 Nov — Mock / Demo Data
- [ ] Create mock event generator
- [ ] Create mock session generator
- [ ] Create mock prediction generator
- [ ] Create mock SHAP output
- [ ] Create mock evidence record
- [ ] Create mock system metrics
- [ ] Create multi-stage demo case
- [ ] Create tampered-evidence demo case
- [ ] Add `DEMO_MODE` configuration
- [ ] Verify demo mode needs no live attacker

## 9–22 Nov — Dashboard Shell
- [ ] Create dashboard project
- [ ] Create overview page
- [ ] Create navigation
- [ ] Create system-health card
- [ ] Create active-session card
- [ ] Create event-count card
- [ ] Create threat/risk card
- [ ] Create active-services card
- [ ] Create CPU card
- [ ] Create RAM card
- [ ] Create session table
- [ ] Create event table
- [ ] Connect overview to mock API

## 23 Nov–6 Dec — Session Investigation
- [ ] Create session-detail page
- [ ] Show source IP
- [ ] Show accessed services
- [ ] Show session duration
- [ ] Show failed logins
- [ ] Show commands
- [ ] Show file access
- [ ] Show HTTP activity
- [ ] Show database-like activity
- [ ] Show predicted intent
- [ ] Show confidence
- [ ] Show risk level
- [ ] Show SHAP summary
- [ ] Show evidence integrity status

## 7–20 Dec — Timeline + Graph
- [ ] Add session timeline component
- [ ] Add event ordering
- [ ] Add attack-stage labels
- [ ] Add evidence IDs to timeline
- [ ] Add service transitions
- [ ] Add attack-graph data model
- [ ] Render graph nodes
- [ ] Render graph edges
- [ ] Link graph nodes to evidence
- [ ] Add risk progression view
- [ ] Test with multi-stage case

## 21 Dec–10 Jan — Reports
- [ ] Define incident-report schema
- [ ] Add incident ID
- [ ] Add time range
- [ ] Add source IP
- [ ] Add accessed services
- [ ] Add observed actions
- [ ] Add predicted intent
- [ ] Add risk level
- [ ] Add SHAP explanation
- [ ] Add attack timeline
- [ ] Add evidence integrity
- [ ] Add bounded recommended action
- [ ] Generate JSON report
- [ ] Generate HTML report
- [ ] Generate PDF report if selected
- [ ] Add evidence-ID references

## 11–24 Jan — Integration
- [ ] Connect A's event stream
- [ ] Connect A's sessions
- [ ] Connect B's predictions
- [ ] Connect B's SHAP outputs
- [ ] Connect D's deception state
- [ ] Connect D's evidence integrity
- [ ] Connect D's timeline/graph data
- [ ] Handle D unavailable
- [ ] Add static-deception fallback
- [ ] Add observe-only fallback
- [ ] Add API integration tests
- [ ] Add end-to-end demo test

## 25 Jan–7 Feb — Demo Mode + Reliability
- [ ] Create one-click demo mode
- [ ] Create deterministic demo scenario
- [ ] Create multi-stage demo scenario
- [ ] Add demo reset
- [ ] Add case reset
- [ ] Add API health indicator
- [ ] Add backend reconnect behaviour
- [ ] Add dashboard empty-state handling
- [ ] Add API timeout handling
- [ ] Add malformed-event handling
- [ ] Test repeated demo runs

## 8–21 Feb — Hardening
- [ ] Add authentication if required by lab deployment
- [ ] Validate API inputs
- [ ] Remove debug secrets
- [ ] Review CORS configuration
- [ ] Add structured logs
- [ ] Complete integration-test suite
- [ ] Add frontend error handling
- [ ] Document backend startup
- [ ] Document dashboard deployment
- [ ] Capture final screenshots
- [ ] Record demo video if required

## 22–28 Feb — Final
- [ ] Freeze API version
- [ ] Freeze dashboard version
- [ ] Tag final application release
- [ ] Back up source code
- [ ] Back up mock/demo cases
- [ ] Back up screenshots
- [ ] Complete API documentation
- [ ] Complete user guide
- [ ] Complete deployment guide
- [ ] Verify final end-to-end demo
