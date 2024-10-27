import React, { useState } from 'react';
import './emaildropdown.css'; // Import your CSS file for styling
import { FaChevronDown, FaChevronUp } from 'react-icons/fa'; // Make sure this line is included

const EmailDropdown = () => {
    const [isOpen, setIsOpen] = useState(false); // State to manage dropdown visibility
    const [isReportVisible, setIsReportVisible] = useState(false); // State for sticky note visibility
    const [isAnalyzed, setIsAnalyzed] = useState(false); // State to track if analyze has been pressed


    const handleToggle = () => {
        setIsOpen(!isOpen); // Toggle dropdown visibility
        setIsReportVisible(false); // Reset report visibility when toggling the dropdown
        setIsAnalyzed(false); // Reset analyze state when closing the dropdown
    };

    const handleAnalyze = () => {
        // Handle analyze functionality here (e.g., API call)
        console.log('Analyzing email content...');
        setIsAnalyzed(true); // Set analyze state to true when Analyze is pressed
    };

    const handleReportToggle = () => {
        setIsReportVisible(!isReportVisible); // Toggle report visibility
    };

    return (
        <div className="email-dropdown">
            <div className="email-summary" onClick={handleToggle}>
                <h3>Email Subject</h3>
                {isOpen ? <FaChevronUp /> : <FaChevronDown />} {/* Up/Down arrow icons */}
            </div>
            {isOpen && (
                <div className="email-content">
                    <p>This is the full content of the email. Here you can add more details.</p>
                    <div className='buttons'>
                    <button className="analyze-button" onClick={handleAnalyze}>
                        Analyze
                    </button>
                    {isAnalyzed && ( // Show the Report button only if Analyze has been pressed
                            <button className="report-button" onClick={handleReportToggle}>
                                {isReportVisible ? 'Hide Report' : 'Show Report'}
                            </button>
                        )}
                    </div>
                    {/* {isReportVisible && ( // Show report content if the report button is toggled
                        <div className="report-content">
                            <p>This is the report content for the email.</p>
                        </div>
                        )} */}
                    

                </div>
            )}
         {/* Sticky Note for Analysis Report */}
         {isReportVisible  && (
                <div className="sticky-note">
                    <h3>Analysis Report</h3>
                    <p>Your analysis details will go here...</p>
                </div>
            )}
        </div>
    );
};

export default EmailDropdown;
