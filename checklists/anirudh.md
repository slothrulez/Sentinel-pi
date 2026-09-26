# PiSentinel — Anirudh (A) Checklist
**Role:** Raspberry Pi / Edge Platform  
**Build window:** 21 Sep 2026 → 28 Feb 2027

Legend: `[x]` completed, `[ ]` pending, `[!]` blocked/dependency

## Current status
- [x] Raspberry Pi 4 (2 GB) prepared
- [x] Raspberry Pi OS 64-bit installed
- [x] Pi Connect skipped
- [x] SSH enabled and working
- [x] Hostname verified as `sentinel`
- [x] User verified as `pisentinel`
- [x] Ethernet SSH access verified
- [x] Wi-Fi connected to `Airtel_Saihome`
- [x] Wi-Fi IP observed as `192.168.1.25`
- [x] Laptop successfully pinged Pi over Wi-Fi
- [x] Pi successfully pinged router over Wi-Fi
- [x] Pi successfully reached `8.8.8.8`
- [x] SSH daemon verified listening on port 22
- [x] System update/full-upgrade completed
- [x] Reboot completed and SSH re-established
- [x] `aarch64` confirmed
- [x] ~1.8 GiB RAM / ~1.8 GiB swap confirmed
- [x] ~58 GB root storage confirmed
- [ ] Static/reserved IP configured
- [ ] Base development packages installed
- [ ] SSH-over-Wi-Fi login explicitly verified after final network configuration

## 21–27 Sep — Edge Foundation
- [ ] Confirm final network interface for PiSentinel
- [ ] Decide Wi-Fi vs Ethernet for experiments
- [ ] Reserve a stable DHCP address in the router
- [ ] Record the reserved IP in project docs
- [ ] Install `git`
- [ ] Install `curl`
- [ ] Install `wget`
- [ ] Install `vim`
- [ ] Install `htop`
- [ ] Install `tcpdump`
- [ ] Install `python3-venv`
- [ ] Install `python3-pip`
- [ ] Install `sqlite3`
- [ ] Verify Git
- [ ] Verify Python
- [ ] Verify tcpdump
- [ ] Verify SQLite
- [ ] Create `~/pisentinel`
- [ ] Create `edge/`
- [ ] Create `edge/collector/`
- [ ] Create `edge/features/`
- [ ] Create `edge/api/`
- [ ] Create `edge/evidence/`
- [ ] Create `data/`
- [ ] Create `logs/`
- [ ] Create Python virtual environment
- [ ] Activate the virtual environment
- [ ] Create `.gitignore`
- [ ] Clone/create the shared repository
- [ ] Add Pi setup notes to README
- [ ] Add hardware/network inventory
- [ ] Commit initial edge setup

## 28 Sep–4 Oct — Event Collection Skeleton
- [ ] Create `config.py`
- [ ] Create `.env.example`
- [ ] Create event data structure
- [ ] Add event ID generation
- [ ] Add timestamp generation
- [ ] Add source IP field
- [ ] Add destination service field
- [ ] Add event type field
- [ ] Add action field
- [ ] Add session ID field
- [ ] Add metadata field
- [ ] Add severity field
- [ ] Write one event to stdout
- [ ] Write one event to JSON
- [ ] Create SQLite connection helper
- [ ] Create `events` table
- [ ] Insert one test event
- [ ] Read one test event back
- [ ] Add basic logging
- [ ] Add collector health check
- [ ] Document event-schema version

## 5–11 Oct — Network Capture
- [ ] Identify the PiSentinel capture interface
- [ ] Test `tcpdump`
- [ ] Save a short PCAP
- [ ] Verify the PCAP opens correctly
- [ ] Write a minimal Scapy capture script
- [ ] Capture TCP packets
- [ ] Capture UDP packets
- [ ] Extract source IP
- [ ] Extract source port
- [ ] Extract destination IP
- [ ] Extract destination port
- [ ] Extract protocol
- [ ] Extract packet timestamp
- [ ] Add capture error handling
- [ ] Add capture shutdown handling
- [ ] Prevent raw packet storage from growing indefinitely
- [ ] Document capture limitations

## 12–18 Oct — Flow + Session Builder
- [ ] Define the flow key
- [ ] Record flow start time
- [ ] Record flow end time
- [ ] Count packets per flow
- [ ] Count bytes per flow
- [ ] Calculate flow duration
- [ ] Detect new connections
- [ ] Detect repeated connections
- [ ] Define the session timeout
- [ ] Group events into sessions
- [ ] Assign session IDs
- [ ] Store session start time
- [ ] Store session end time
- [ ] Store session event count
- [ ] Test one multi-event session
- [ ] Test two independent sessions
- [ ] Test session timeout
- [ ] Test out-of-order events
- [ ] Add session-builder tests

## 19–25 Oct — Feature Extraction
- [ ] Read the shared feature schema
- [ ] Confirm feature names with Anshika
- [ ] Confirm feature order with Anshika
- [ ] Confirm units with Anshika
- [ ] Confirm missing-value rules with Anshika
- [ ] Implement `connection_count`
- [ ] Implement `unique_ports`
- [ ] Implement `unique_services`
- [ ] Implement `failed_login_count`
- [ ] Implement `successful_login_count`
- [ ] Implement `command_count`
- [ ] Implement `file_access_count`
- [ ] Implement `http_request_count`
- [ ] Implement `database_request_count`
- [ ] Implement `session_duration`
- [ ] Implement `service_transition_count`
- [ ] Implement `request_frequency`
- [ ] Add feature-vector validation
- [ ] Add fixed feature ordering
- [ ] Add a known test session
- [ ] Verify the expected feature vector manually
- [ ] Export feature vectors as JSON
- [ ] Export feature vectors as CSV for B
- [ ] Document feature extraction

## 26 Oct–8 Nov — Local Storage + Health
- [ ] Create `sessions` table
- [ ] Create `predictions` table
- [ ] Create `system_metrics` table
- [ ] Create useful database indexes
- [ ] Store normalized events
- [ ] Store session records
- [ ] Store feature vectors
- [ ] Store model-prediction metadata
- [ ] Add database cleanup policy
- [ ] Add a basic backup script
- [ ] Measure CPU usage
- [ ] Measure RAM usage
- [ ] Measure disk usage
- [ ] Measure event-processing latency
- [ ] Measure network overhead
- [ ] Measure service startup time
- [ ] Record baseline idle metrics
- [ ] Record baseline collector metrics
- [ ] Write resource benchmark notes

## 9–22 Nov — Decoy Runtime Support
- [ ] Coordinate SSH decoy requirements with Britto
- [ ] Coordinate web decoy requirements with Britto
- [ ] Define service ports
- [ ] Define controlled bind addresses
- [ ] Create service start/stop scripts
- [ ] Run one decoy service
- [ ] Verify decoy logs reach collector
- [ ] Verify decoy events receive session IDs
- [ ] Verify synthetic-only data
- [ ] Verify no real secrets are exposed
- [ ] Add service health checks
- [ ] Add restart policy
- [ ] Test decoy failure recovery

## 23 Nov–6 Dec — Service Management
- [ ] Create systemd unit for collector
- [ ] Create systemd unit for decoy service(s)
- [ ] Start the service manually
- [ ] Check service status
- [ ] Check service logs
- [ ] Restart the service
- [ ] Test service after reboot
- [ ] Add dependency ordering
- [ ] Add graceful shutdown
- [ ] Add log rotation/retention
- [ ] Document deployment commands

## 7–20 Dec — ML Integration
- [ ] Agree model-artifact format with B
- [ ] Agree feature-schema version with B
- [ ] Agree prediction JSON contract with B
- [ ] Load the trained model on the Pi
- [ ] Run one local inference
- [ ] Measure inference latency
- [ ] Measure inference RAM
- [ ] Handle missing model artifact
- [ ] Handle malformed feature vector
- [ ] Store prediction result
- [ ] Expose prediction to C's API
- [ ] Verify feature → prediction flow

## 21 Dec–10 Jan — Evidence Support
- [ ] Coordinate evidence fields with Britto
- [ ] Add `previous_hash` storage
- [ ] Add `current_hash` storage
- [ ] Persist evidence records
- [ ] Add monotonic sequence number
- [ ] Verify evidence survives restart
- [ ] Export `events.jsonl`
- [ ] Export case metadata
- [ ] Provide ordered events to reconstruction layer

## 11–24 Jan — Integration + Hardening
- [ ] Test collector + decoys together
- [ ] Test collector + session builder
- [ ] Test session builder + feature extractor
- [ ] Test feature extractor + ML
- [ ] Test ML + API
- [ ] Test system after reboot
- [ ] Test Wi-Fi reconnect
- [ ] Test temporary network loss
- [ ] Test high event volume
- [ ] Test disk growth under long run
- [ ] Add rate limiting where needed
- [ ] Reduce unnecessary background services
- [ ] Measure peak RAM
- [ ] Measure peak CPU
- [ ] Fix resource bottlenecks

## 25 Jan–7 Feb — Reliability
- [ ] Create one-command setup script
- [ ] Create one-command start script
- [ ] Create one-command stop script
- [ ] Create one-command status script
- [ ] Create backup procedure
- [ ] Create restore procedure
- [ ] Test clean reinstall
- [ ] Test service-crash recovery
- [ ] Test recovery after reboot
- [ ] Document troubleshooting

## 8–21 Feb — Evaluation
- [ ] Record idle CPU
- [ ] Record idle RAM
- [ ] Record active-session CPU
- [ ] Record active-session RAM
- [ ] Record inference latency
- [ ] Record network overhead
- [ ] Record storage growth
- [ ] Record startup time
- [ ] Compare local-only vs offloaded analysis
- [ ] Save raw benchmark results
- [ ] Prepare benchmark tables

## 22–28 Feb — Final
- [ ] Freeze deployment configuration
- [ ] Tag final edge release
- [ ] Back up source code
- [ ] Back up configuration
- [ ] Back up case data
- [ ] Verify clean boot
- [ ] Verify live event collection
- [ ] Verify live session building
- [ ] Verify live feature extraction
- [ ] Verify live ML inference
- [ ] Hand final deployment package to the team
- [ ] Finish deployment documentation
