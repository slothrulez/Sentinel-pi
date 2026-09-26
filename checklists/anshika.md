# PiSentinel — Anshika (B) Checklist
**Role:** Machine Learning, SHAP and Behavioural Intelligence  
**Build window:** 21 Sep 2026 → 28 Feb 2027

## Current status
- [ ] Final shared feature schema confirmed
- [ ] Final dataset strategy confirmed
- [ ] Final labels confirmed
- [ ] Dataset prepared
- [ ] Baseline model trained
- [ ] SHAP integrated
- [ ] Confidence/risk scoring integrated
- [ ] Edge inference validated

## 21–27 Sep — ML Contract
- [ ] Review A's candidate features
- [ ] Review C's prediction/API needs
- [ ] Review D's behavioural states
- [ ] Decide final feature list
- [ ] Decide final feature order
- [ ] Decide feature data types
- [ ] Decide feature units
- [ ] Decide missing-value rules
- [ ] Decide preprocessing rules
- [ ] Decide final label set
- [ ] Decide treatment of `normal/benign`
- [ ] Decide treatment of reconnaissance
- [ ] Decide treatment of scanning
- [ ] Decide treatment of credential attacks
- [ ] Decide treatment of remote access
- [ ] Decide treatment of file discovery
- [ ] Decide treatment of data discovery
- [ ] Document feature schema version
- [ ] Publish `feature_schema.json`
- [ ] Publish prediction JSON schema
- [ ] Define confidence field
- [ ] Define risk-level field

## 28 Sep–11 Oct — Dataset Engineering
- [ ] List suitable public IoT intrusion datasets
- [ ] Select usable public sources
- [ ] Document each source
- [ ] Identify useful behavioural fields
- [ ] Identify schema mismatches
- [ ] Define public-data transformation rules
- [ ] Define synthetic lab-session format
- [ ] Define benign-session format
- [ ] Define attack-session format
- [ ] Define scenario metadata
- [ ] Define ground-truth start time
- [ ] Define ground-truth end time
- [ ] Define stage labels
- [ ] Create dataset directory structure
- [ ] Write dataset ingestion script
- [ ] Write label-conversion script
- [ ] Validate feature columns
- [ ] Check missing labels
- [ ] Check duplicate sessions
- [ ] Check class balance
- [ ] Save dataset-version metadata

## 12–25 Oct — Feature Pipeline
- [ ] Load A's session features
- [ ] Validate column names
- [ ] Validate column order
- [ ] Validate numeric types
- [ ] Validate missing values
- [ ] Validate feature ranges
- [ ] Create train/test split
- [ ] Prevent scenario leakage across splits
- [ ] Build preprocessing pipeline
- [ ] Save preprocessing configuration
- [ ] Create training script
- [ ] Create evaluation script
- [ ] Add reproducible random seed
- [ ] Save dataset version with results

## 26 Oct–8 Nov — Baseline Models
- [ ] Train Decision Tree baseline
- [ ] Train Logistic Regression baseline
- [ ] Train Gradient Boosting baseline
- [ ] Train Random Forest baseline
- [ ] Record training time
- [ ] Record inference time
- [ ] Record RAM usage
- [ ] Calculate accuracy
- [ ] Calculate precision
- [ ] Calculate recall
- [ ] Calculate F1
- [ ] Generate confusion matrix
- [ ] Calculate false-positive rate
- [ ] Compare baseline models
- [ ] Select deployable baseline
- [ ] Save model artifact
- [ ] Save model metadata
- [ ] Record feature-schema version

## 9–22 Nov — Behavioural Intelligence
- [ ] Validate `connection_count`
- [ ] Validate `unique_ports`
- [ ] Validate `failed_login_count`
- [ ] Validate `successful_login_count`
- [ ] Validate `command_count`
- [ ] Validate `file_access_count`
- [ ] Validate `http_request_count`
- [ ] Validate `database_request_count`
- [ ] Validate `session_duration`
- [ ] Validate `service_transition_count`
- [ ] Validate `request_frequency`
- [ ] Analyze feature importance
- [ ] Check redundant features
- [ ] Check correlated features
- [ ] Test class-imbalance handling
- [ ] Test unseen behaviour
- [ ] Define minimum confidence threshold
- [ ] Define uncertainty fallback
- [ ] Document prediction-vs-fact distinction

## 23 Nov–6 Dec — Inference Contract
- [ ] Create inference function
- [ ] Accept one feature vector
- [ ] Return predicted class
- [ ] Return class probabilities
- [ ] Return confidence
- [ ] Return risk level
- [ ] Return model version
- [ ] Return feature-schema version
- [ ] Add invalid-vector handling
- [ ] Add missing-model handling
- [ ] Test on Pi-compatible data
- [ ] Hand contract to C
- [ ] Hand model artifact to A

## 7–20 Dec — SHAP
- [ ] Install SHAP in analysis environment
- [ ] Create Tree SHAP explainer
- [ ] Explain one session
- [ ] Extract top positive contributors
- [ ] Extract top negative contributors
- [ ] Store contribution values
- [ ] Store explained session ID
- [ ] Store model version
- [ ] Store feature-schema version
- [ ] Create readable explanation text
- [ ] Add suspicious-session trigger
- [ ] Ensure SHAP is not run per packet
- [ ] Measure SHAP latency
- [ ] Measure SHAP RAM
- [ ] Decide laptop/API vs Pi execution
- [ ] Publish SHAP JSON contract
- [ ] Hand SHAP contract to C

## 21 Dec–10 Jan — Confidence + Intent
- [ ] Define confidence interpretation
- [ ] Define low-confidence behaviour
- [ ] Map model outputs to intent abstraction
- [ ] Separate prediction from inferred intent
- [ ] Include evidence IDs used by a prediction
- [ ] Produce decision-trace fields
- [ ] Test ambiguous sessions
- [ ] Test mixed-behaviour sessions
- [ ] Test unknown-behaviour sessions
- [ ] Document uncertainty

## 11–24 Jan — Experiments
- [ ] Run repeated scripted scenarios
- [ ] Measure intent accuracy
- [ ] Measure precision
- [ ] Measure recall
- [ ] Measure macro F1
- [ ] Measure false-positive rate
- [ ] Measure inference latency
- [ ] Measure RAM usage
- [ ] Compare behavioural vs reduced feature sets
- [ ] Run ablation study
- [ ] Run model comparison
- [ ] Save experiment outputs
- [ ] Record failure cases

## 25 Jan–7 Feb — Edge Optimization
- [ ] Test model loading time on Pi
- [ ] Test inference time on Pi
- [ ] Test inference RAM on Pi
- [ ] Reduce model size if necessary
- [ ] Test the agreed Random Forest configuration
- [ ] Keep Pi inference single-process
- [ ] Document final model settings
- [ ] Verify reproducibility

## 8–21 Feb — Final ML Package
- [ ] Freeze dataset version
- [ ] Freeze final model
- [ ] Freeze feature schema
- [ ] Freeze preprocessing pipeline
- [ ] Freeze SHAP format
- [ ] Export metrics
- [ ] Export plots
- [ ] Export confusion matrix
- [ ] Export ablation results
- [ ] Write ML limitations
- [ ] Write unknown-behaviour limitations

## 22–28 Feb — Final
- [ ] Tag final model release
- [ ] Back up model artifacts
- [ ] Back up dataset metadata
- [ ] Back up experiment results
- [ ] Give final model package to A
- [ ] Give final API contract to C
- [ ] Give intent/risk mapping to D
- [ ] Complete ML documentation
