import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [complaint, setComplaint] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [evidence, setEvidence] = useState([]);

  const [decision, setDecision] = useState("");
  const [decisionNote, setDecisionNote] = useState("");

  const [loadingCases, setLoadingCases] = useState(false);
  const [loadingCase, setLoadingCase] = useState(false);
  const [uploading, setUploading] = useState(false);
  const totalCases = cases.length;

  const reviewedCases = cases.filter(
   (item) => item.status === "REVIEWED"
  ).length;

  const escalatedCases = cases.filter(
   (item) => item.decision === "ESCALATE"
  ).length;

  const highRiskCases = cases.filter(
   (item) =>
     item.risk_level === "HIGH" ||
     item.risk_level === "CRITICAL"
  ).length;
  const [submittingDecision, setSubmittingDecision] = useState(false);

  // --------------------------------------------------
  // CREATE CASE
  // --------------------------------------------------

  async function createCase() {
    setMessage("");
    setError("");

    if (!complaint.trim()) {
      setError("Please enter a customer complaint.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/cases`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          complaint: complaint.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create case.");
      }

      setMessage("Case created successfully.");
      setComplaint("");

      await loadCases();
    } catch (err) {
      setError(err.message);
    }
  }

  // --------------------------------------------------
  // LOAD CASES
  // --------------------------------------------------

  async function loadCases() {
    setLoadingCases(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/cases`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to load cases.");
      }

      setCases(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingCases(false);
    }
  }

  // --------------------------------------------------
  // SELECT CASE
  // --------------------------------------------------

  async function selectCase(caseId) {
    setLoadingCase(true);
    setError("");
    setMessage("");

    try {
      const caseResponse = await fetch(
        `${API_URL}/cases/${caseId}`
      );

      const caseData = await caseResponse.json();

      if (!caseResponse.ok) {
        throw new Error(
          caseData.detail || "Failed to load case."
        );
      }

      setSelectedCase(caseData);

      const evidenceResponse = await fetch(
        `${API_URL}/cases/${caseId}/evidence`
      );

      const evidenceData = await evidenceResponse.json();

      if (!evidenceResponse.ok) {
        throw new Error(
          evidenceData.detail || "Failed to load evidence."
        );
      }

      setEvidence(evidenceData);

      // Load saved investigator decision if present
      setDecision(caseData.decision || "");
      setDecisionNote(caseData.decision_note || "");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingCase(false);
    }
  }

  // --------------------------------------------------
  // UPLOAD EVIDENCE
  // --------------------------------------------------

  async function uploadEvidence(event) {
    const file = event.target.files[0];

    if (!file || !selectedCase) {
      return;
    }

    setUploading(true);
    setError("");
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/cases/${selectedCase.case_id}/evidence`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Evidence upload failed."
        );
      }

      setMessage("Evidence uploaded successfully.");

      // Reload evidence so OCR/entities appear immediately
      await selectCase(selectedCase.case_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  // --------------------------------------------------
  // INVESTIGATOR DECISION
  // --------------------------------------------------

  async function submitDecision() {
    if (!selectedCase) {
      return;
    }

    setError("");
    setMessage("");

    if (!decision) {
      setError("Please select a decision.");
      return;
    }

    setSubmittingDecision(true);

    try {
      const response = await fetch(
        `${API_URL}/cases/${selectedCase.case_id}/decision`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            decision: decision,
            note: decisionNote,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to submit decision."
        );
      }

      setMessage("Investigator decision recorded.");

      // Update selected case immediately
      setSelectedCase((previous) => ({
        ...previous,
        status: data.status,
        decision: data.decision,
        decision_note: data.decision_note,
      }));

      // Refresh case list so status changes there too
      await loadCases();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmittingDecision(false);
    }
  }
  // --------------------------------------------------
  // INITIAL LOAD
  // --------------------------------------------------

  useEffect(() => {
    loadCases();
  }, []);

  // --------------------------------------------------
  // HELPERS
  // --------------------------------------------------

  function getStatusClass(status) {
    if (!status) return "status-default";

    return `status-${status.toLowerCase()}`;
  }

  function renderEntityList(title, values) {
    if (!values || values.length === 0) {
      return null;
    }

    return (
      <div className="entity-group">
        <span className="entity-label">{title}</span>

        <div className="entity-values">
          {values.map((value, index) => (
            <span className="entity-chip" key={`${value}-${index}`}>
              {value}
            </span>
          ))}
        </div>
      </div>
    );
  }

  function renderBooleanEntity(title, value) {
    return (
      <div className="entity-group">
        <span className="entity-label">{title}</span>

        <span
          className={
            value
              ? "indicator-badge indicator-danger"
              : "indicator-badge indicator-safe"
          }
        >
          {value ? "YES" : "NO"}
        </span>
      </div>
    );
  }

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>Secure Banking Investigation</h1>
          <p>
            AI-assisted evidence and scam investigation platform
          </p>
        </div>
      </header>

      <main className="container">

        {/* GLOBAL MESSAGE */}

        {message && (
          <div className="alert success">
            {message}
          </div>
        )}

        {error && (
          <div className="alert error">
            {error}
          </div>
        )}

{/* DASHBOARD STATS */}

<section className="dashboard-stats">

  <div className="stat-card">
    <span className="stat-label">Total Cases</span>
    <strong className="stat-value">
      {totalCases}
    </strong>
  </div>

  <div className="stat-card">
    <span className="stat-label">High Risk</span>
    <strong className="stat-value">
      {highRiskCases}
    </strong>
  </div>

  <div className="stat-card">
    <span className="stat-label">Reviewed</span>
    <strong className="stat-value">
      {reviewedCases}
    </strong>
  </div>

  <div className="stat-card">
    <span className="stat-label">Escalated</span>
    <strong className="stat-value">
      {escalatedCases}
    </strong>
  </div>

</section>

        {/* CREATE CASE */}

        <section className="card complaint-section">
          <div className="section-header">
            <div>
              <h2 className="section-title">Create Investigation Case</h2>
              <p>
                Record the customer's complaint to begin an investigation.
              </p>
            </div>
          </div>

          <textarea
            className="complaint-input"
            placeholder="Enter customer complaint..."
            value={complaint}
            onChange={(event) =>
              setComplaint(event.target.value)
            }
            rows={5}
          />

          <button
            className="primary-button"
            onClick={createCase}
          >
            Create Case
          </button>
        </section>

        {/* CASE LIST */}

        <section className="card">
          <div className="section-header">
            <div>
              <h2 className="section-title">Investigation Cases</h2>
              <p>
                Select a case to inspect its evidence.
              </p>
            </div>

            <span className="case-count">
              {cases.length} cases
            </span>
          </div>

          {loadingCases ? (
            <p className="muted">Loading cases...</p>
          ) : cases.length === 0 ? (
            <p className="muted">No cases found.</p>
          ) : (
            <div className="case-list">
              
              {cases.map((item) => (
  <button
    className={`case-item ${
      selectedCase?.case_id === item.case_id
        ? "selected"
        : ""
    }`}
    key={item.case_id}
    onClick={() => selectCase(item.case_id)}
  >

    <div className="case-item-main">

      <div className="case-item-info">

        <h3>{item.case_id}</h3>

        <p>{item.complaint}</p>

        <div className="case-meta">

          {item.risk_level && (
            <span
              className={`case-risk risk-${item.risk_level.toLowerCase()}`}
            >
              {item.risk_level} RISK
            </span>
          )}

          {item.risk_score !== null &&
            item.risk_score !== undefined && (
              <span className="case-score">
                {item.risk_score}/100
              </span>
            )}

          {item.decision && (
            <span className="case-decision">
              {item.decision}
            </span>
          )}

        </div>

      </div>


      <span
        className={`status-badge ${getStatusClass(
          item.status
        )}`}
      >
        {item.status}
      </span>

    </div>

  </button>
))}        
              
            </div>
          )}
        </section>

        {/* CASE DETAILS */}

        {loadingCase && (
          <section className="card">
            <p className="muted">
              Loading case details...
            </p>
          </section>
        )}

        {selectedCase && !loadingCase && (
          <section className="case-details">

            {/* CASE HEADER */}

            <div className="card case-header-card">
              <div>
                <span className="small-label">
                  INVESTIGATION CASE
                </span>

                <h2>{selectedCase.case_id}</h2>
              </div>

              <span
                className={`status-badge large ${getStatusClass(
                  selectedCase.status
                )}`}
              >
                {selectedCase.status}
              </span>
            </div>

            {/* COMPLAINT */}

            <div className="card">
              <h3>Customer Complaint</h3>

              <div className="complaint-box">
                {selectedCase.complaint}
              </div>
            </div>

            {/* EVIDENCE */}

            <div className="card evidence-section">
              <div className="section-header">
                <div>
                  <h3>Evidence</h3>
                  <p>
                    Uploaded documents and extracted investigation data.
                  </p>
                </div>

                <label className="upload-button">
                  {uploading
                    ? "Uploading..."
                    : "Upload Evidence"}

                  <input
                    type="file"
                    accept=".png,.jpg,.jpeg,.pdf,.txt"
                    onChange={uploadEvidence}
                    disabled={uploading}
                  />
                </label>
              </div>

              {evidence.length === 0 ? (
                <p className="muted">
                  No evidence uploaded.
                </p>
              ) : (
                <div className="evidence-list">

                  {evidence.map((item) => (
                    <div
                      className="evidence-card"
                      key={item.evidence_id}
                    >
                      {/* FILE INFO */}

                      <div className="evidence-header">
                        <div>
                          <h4>{item.filename}</h4>

                          <span className="file-type">
                            {item.file_type}
                          </span>
                        </div>

                        <span className="evidence-id">
                          {item.evidence_id}
                        </span>
                      </div>

                      {/* OCR */}

                      {item.extracted_text && (
                        <div className="ocr-section">
                          <h4>OCR Extracted Text</h4>

                          <pre className="ocr-text">
                            {item.extracted_text}
                          </pre>
                        </div>
                      )}

                      {/* ENTITIES */}

                      {item.extracted_entities && (
                        <div className="entities-section">
                          <h4>Detected Entities</h4>

                          <div className="entities">

                            {renderEntityList(
                              "URLs",
                              item.extracted_entities.urls
                            )}

                            {renderEntityList(
                              "Phone Numbers",
                              item.extracted_entities.phone_numbers
                            )}

                            {renderEntityList(
                              "Amounts",
                              item.extracted_entities.amounts
                            )}

                            {renderEntityList(
                              "Transaction IDs",
                              item.extracted_entities.transaction_ids
                            )}

                            {renderEntityList(
                              "UPI IDs",
                              item.extracted_entities.upi_ids
                            )}

                            {renderEntityList(
                              "Dates",
                              item.extracted_entities.dates
                            )}

                            {renderBooleanEntity(
                              "OTP Request",
                              item.extracted_entities.otp_request
                            )}

                            {renderBooleanEntity(
                              "PIN Request",
                              item.extracted_entities.pin_request
                            )}

                            {renderBooleanEntity(
                              "CVV Request",
                              item.extracted_entities.cvv_request
                            )}

                          </div>
                        </div>
                      )}
            
            {/* RISK ANALYSIS */}

            {item.risk_level && (
              <div className="card risk-section">
                <div className="risk-header">
                 <div>
                   <h4>Scam Risk Analysis</h4>
                   <p>
                     Risk assessment generated from the extracted evidence.
                   </p>
                 </div>

                  <div
                    className={`risk-badge risk-${item.risk_level.toLowerCase()}`}
                  >
                    {item.risk_level}
                  </div>
                 </div>

                 <div className="risk-score">
                   <span>Risk Score</span>

                   <strong>
                    {item.risk_score}/100
                   </strong>
                  </div>

                  {item.risk_indicators &&
                    item.risk_indicators.length > 0 && (
                      <div className="risk-indicators">
                        <h4>Detected Indicators</h4>

                   {item.risk_indicators.map(
            (indicator, index) => (
              <div
                className="risk-indicator"
                key={`${indicator.type}-${index}`}
              >
                <div className="indicator-top">
                  <strong>
                    {indicator.type.replaceAll(
                      "_",
                      " "
                    )}
                  </strong>

                  <span
                    className={`severity severity-${indicator.severity.toLowerCase()}`}
                  >
                    {indicator.severity}
                  </span>

                  <span className="indicator-score">
                    +{indicator.score}
                  </span>
                </div>

                <p>
                  {indicator.reason}
                </p>
              </div>
            )
          )}
        </div>
      )}
  </div>
)}


{/* AI INVESTIGATION REPORT */}

{item.investigation_report && (
  <div className="card ai-report-section">
    <div className="report-header">
      <div>
        <h3>AI Investigation Report</h3>
        <p>
          Evidence-grounded analysis generated from
          the retrieved banking knowledge.
        </p>
      </div>
    </div>

    
    
    
    <div className="report-content">
  <ReactMarkdown>
    {item.investigation_report}
  </ReactMarkdown>
   </div>
    
    
  </div>
)}
            </div>
          ))}
          </div>
              )}
              </div>

            {/* INVESTIGATOR DECISION */}

            <div className="card decision-section">
              <div className="section-header">
                <div>
                  <h3>Investigator Decision</h3>
                  <p>
                    Record the investigator's final decision for this case.
                  </p>
                </div>
              </div>

              <label className="field-label">
                Decision
              </label>

              <select
                className="decision-select"
                value={decision}
                onChange={(event) =>
                  setDecision(event.target.value)
                }
              >
                <option value="">
                  Select decision
                </option>

                <option value="APPROVE">
                  Approve
                </option>

                <option value="REJECT">
                  Reject
                </option>

                <option value="ESCALATE">
                  Escalate
                </option>
              </select>

              <label className="field-label">
                Investigator Note
              </label>

              <textarea
                className="decision-note"
                placeholder="Add investigation notes..."
                value={decisionNote}
                onChange={(event) =>
                  setDecisionNote(event.target.value)
                }
                rows={4}
              />

              <button
                className="primary-button"
                onClick={submitDecision}
                disabled={submittingDecision}
              >
                {submittingDecision
                  ? "Submitting..."
                  : "Submit Decision"}
              </button>

              {selectedCase.decision && (
                <div className="recorded-decision">
                  <strong>
                    Recorded Decision:
                  </strong>

                  <span className="decision-badge">
                    {selectedCase.decision}
                  </span>

                  {selectedCase.decision_note && (
                    <p>
                      {selectedCase.decision_note}
                    </p>
                  )}
                </div>
              )}
            </div>

          </section>
        )}

      </main>
    </div>
  );
}

export default App;