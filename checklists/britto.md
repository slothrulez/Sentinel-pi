# PiSentinel — Britto (D) Checklist
**Role:** Cybersecurity Intelligence, Adaptive Defense and Forensics  
**Build window:** 21 Sep 2026 → 28 Feb 2027

## Current status
- [ ] Threat model completed
- [ ] Lab boundaries documented
- [ ] SSH decoy completed
- [ ] Web decoy completed
- [ ] Synthetic attacker-facing data completed
- [ ] Adaptive deception state machine completed
- [ ] Attack reconstruction completed
- [ ] Hash-chained evidence completed
- [ ] Response policy engine completed
- [ ] Isolation/containment tests completed
- [ ] Security validation report completed

## 21–27 Sep — Threat Model + Safety
- [ ] Write threat-model scope
- [ ] Define authorized lab boundary
- [ ] Define attacker capabilities
- [ ] Define observed behaviours
- [ ] Define excluded real-world assets
- [ ] List prohibited real credentials
- [ ] List prohibited real data
- [ ] List prohibited production systems
- [ ] Define synthetic-only rule
- [ ] Define no-unrestricted-shell rule
- [ ] Define safe lab addresses
- [ ] Define evidence-preservation rule
- [ ] Define default safe action as `OBSERVE`
- [ ] Publish threat model
- [ ] Review threat model with team

## 28 Sep–11 Oct — Decoy Design
- [ ] Define SSH decoy surface
- [ ] Define web/API decoy surface
- [ ] Define synthetic users
- [ ] Define synthetic directories
- [ ] Define synthetic configuration files
- [ ] Define synthetic API endpoints
- [ ] Define synthetic database-like records
- [ ] Define fake admin surface
- [ ] Define service ports
- [ ] Define attacker-visible behaviour
- [ ] Define decoy logging requirements
- [ ] Define decoy safety boundaries
- [ ] Produce deception state diagram

## 12–25 Oct — SSH / Web Prototypes
- [ ] Prototype SSH decoy
- [ ] Log username attempts
- [ ] Log authentication failures
- [ ] Log session time
- [ ] Log commands
- [ ] Log path/file probes
- [ ] Return synthetic responses only
- [ ] Prototype web decoy
- [ ] Log URLs
- [ ] Log methods
- [ ] Log request rate
- [ ] Log status patterns
- [ ] Log endpoint transitions
- [ ] Verify no real secrets are exposed
- [ ] Verify attacker cannot escape the decoy

## 26 Oct–8 Nov — Security Event Semantics
- [ ] Define recon event
- [ ] Define scanning event
- [ ] Define credential-attack event
- [ ] Define remote-access event
- [ ] Define file-discovery event
- [ ] Define data-discovery event
- [ ] Define service-transition event
- [ ] Define high-risk multi-stage event
- [ ] Define evidence IDs for security decisions
- [ ] Define session security state
- [ ] Test semantics with sample sessions

## 9–22 Nov — Attack-Stage Reconstruction
- [ ] Define stage model
- [ ] Define stage-transition rules
- [ ] Detect reconnaissance stage
- [ ] Detect port-scan stage
- [ ] Detect service-enumeration stage
- [ ] Detect credential-attack stage
- [ ] Detect fake-access stage
- [ ] Detect file-discovery stage
- [ ] Detect data-discovery stage
- [ ] Attach evidence IDs to stages
- [ ] Handle missing events
- [ ] Handle out-of-order timestamps
- [ ] Add monotonic sequence fallback
- [ ] Produce ordered timeline JSON

## 23 Nov–6 Dec — Adaptive Deception
- [ ] Define deception states
- [ ] Define state-entry conditions
- [ ] Define state-exit conditions
- [ ] Add recon → controlled service rule
- [ ] Add SSH enumeration → synthetic users/files rule
- [ ] Add credential attack → synthetic admin rule
- [ ] Add web enumeration → fake API expansion rule
- [ ] Add database probing → synthetic records rule
- [ ] Add file discovery → synthetic configuration tree rule
- [ ] Add high-risk → restrictive action rule
- [ ] Add cooldown timer
- [ ] Add action expiry
- [ ] Add rollback
- [ ] Log every deception decision
- [ ] Log decision reason
- [ ] Log confidence used
- [ ] Test repeated triggers
- [ ] Test oscillation prevention

## 7–20 Dec — Evidence Integrity
- [ ] Define canonical JSON serialization
- [ ] Define `previous_hash`
- [ ] Define `current_hash`
- [ ] Implement SHA-256 calculation
- [ ] Hash first event
- [ ] Link second event to first hash
- [ ] Link third event to second hash
- [ ] Store chain fields
- [ ] Write integrity verifier
- [ ] Verify valid chain
- [ ] Modify one copied event
- [ ] Detect the broken chain
- [ ] Report first broken link
- [ ] Preserve raw copy
- [ ] Generate `integrity_report.json`

## 21 Dec–10 Jan — Attack Graph
- [ ] Define graph node types
- [ ] Define graph edge types
- [ ] Add attacker node
- [ ] Add service node
- [ ] Add session node
- [ ] Add action node
- [ ] Add resource node
- [ ] Add evidence reference
- [ ] Build graph from timeline
- [ ] Link graph edges to evidence
- [ ] Export `attack_graph.json`
- [ ] Hand graph contract to C

## 11–24 Jan — Policy Engine
- [ ] Define response action vocabulary
- [ ] Define `OBSERVE`
- [ ] Define `INCREASE_DECEPTION`
- [ ] Define `RATE_LIMIT`
- [ ] Define `ISOLATE`
- [ ] Define `BLOCK`
- [ ] Define confidence thresholds
- [ ] Define risk thresholds
- [ ] Define low-risk rule
- [ ] Define medium-risk rule
- [ ] Define high-risk rule
- [ ] Define critical-risk rule
- [ ] Add action allowlist
- [ ] Add policy audit log
- [ ] Reject unsupported actions
- [ ] Reject arbitrary shell commands
- [ ] Add safe fallback to `OBSERVE`
- [ ] Build response interface for C

## 25 Jan–7 Feb — Isolation / Adversarial Testing
- [ ] Define test-network isolation
- [ ] Verify decoys cannot access production resources
- [ ] Test invalid policy action
- [ ] Test malformed ML confidence
- [ ] Test repeated credential attack
- [ ] Test multi-stage attack
- [ ] Test decoy exhaustion attempt
- [ ] Test rate limit
- [ ] Test cooldown
- [ ] Test rollback
- [ ] Test evidence chain after response
- [ ] Test AI-unavailable fallback
- [ ] Test model-uncertain fallback
- [ ] Document failures
- [ ] Document mitigations

## 8–21 Feb — Security Evaluation
- [ ] Run port-scan scenario
- [ ] Run SSH credential scenario
- [ ] Run post-access discovery scenario
- [ ] Run web enumeration scenario
- [ ] Run multi-stage scenario
- [ ] Run evidence-tampering scenario
- [ ] Record stages reconstructed
- [ ] Record decoys reached
- [ ] Record interaction depth
- [ ] Record response actions
- [ ] Record integrity detection
- [ ] Record false triggers
- [ ] Record missed triggers
- [ ] Write security validation report

## 22–28 Feb — Final
- [ ] Freeze deception rules
- [ ] Freeze policy rules
- [ ] Freeze evidence schema
- [ ] Freeze reconstruction schema
- [ ] Tag final security release
- [ ] Back up security configuration
- [ ] Back up test scenarios
- [ ] Back up evidence cases
- [ ] Complete threat-model documentation
- [ ] Complete security limitations
- [ ] Hand final interfaces to C
