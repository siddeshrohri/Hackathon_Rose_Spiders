import React, { useState } from "react";
import "./emaildropdown.css";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";

const EmailDropdown = ({ email }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isReportVisible, setIsReportVisible] = useState(false);
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleToggle = () => {
    setIsOpen(!isOpen);
    setIsReportVisible(false);
    setIsAnalyzed(false);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: email.content, // Analyze full email content
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const results = await response.json();
      setAnalysisResults(results);
      setIsAnalyzed(true);
    } catch (error) {
      console.error("Error during analysis:", error);
      alert("Failed to analyze email. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReportToggle = () => {
    setIsReportVisible(!isReportVisible);
  };

  return (
    <div className="email-dropdown">
      <div className="email-summary" onClick={handleToggle}>
        <h3>{email.subject}</h3>
        {isOpen ? <FaChevronUp /> : <FaChevronDown />}
      </div>
      {isOpen && (
        <div className="email-content">
          <p>{email.content}</p>
          <div className="buttons">
            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={isLoading}
            >
              {isLoading ? "Analyzing..." : "Analyze"}
            </button>

            {isAnalyzed && (
              <button className="report-button" onClick={handleReportToggle}>
                {isReportVisible ? "Hide Report" : "Show Report"}
              </button>
            )}
          </div>
          {isReportVisible && analysisResults && (
            <div className="sticky-note">
              <h3>Analysis Report</h3>
              <p>
                <strong>Toxicity Score:</strong>{" "}
                {analysisResults.toxic_score.toFixed(3)}
              </p>
              <p>
                <strong>Status:</strong> {analysisResults.reason}
              </p>

              {/* Additional categories section */}
              {analysisResults.is_microaggression &&
                analysisResults.categories &&
                Object.keys(analysisResults.categories).length > 0 && (
                  <div className="categories-section">
                    <h4>Detected Categories:</h4>
                    {Object.entries(analysisResults.categories).map(
                      ([category, details]) => (
                        <div key={category} className="category-item">
                          <p className="category-name">{category}:</p>
                          <p className="category-detail">
                            Confidence: {(details.confidence * 100).toFixed(1)}%
                          </p>
                          <p className="category-detail">
                            Terms: {details.matching_terms.join(", ")}
                          </p>
                        </div>
                      )
                    )}
                  </div>
                )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EmailDropdown;
