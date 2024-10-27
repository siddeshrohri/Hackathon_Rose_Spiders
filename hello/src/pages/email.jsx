import React, { useState } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import "./email.css";
import { FaBars, FaUserCircle, FaTimes } from "react-icons/fa";
import EmailDropdown from "./emaildropdown";

const EmailPage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const emails = [
    {
      id: 1,
      subject: "Meeting Reminder",
      content:
        "Just a reminder that we have a meeting scheduled for today at 2 PM.",
    },
    {
      id: 2,
      subject: "Project Update",
      content:
        "The latest update on the project includes a completed review of the codebase.",
    },
    {
      id: 3,
      subject: "Happy Birthday!",
      content:
        "Wishing you a very happy birthday! Hope you have an amazing day!",
    },
    {
      id: 4,
      subject: "Newsletter",
      content:
        "Here is our latest newsletter with updates on the latest industry trends.",
    },
    {
      id: 5,
      subject: "Invitation",
      content: "You are a very beautiful lady indeed.",
    },
    {
      id: 6,
      subject: "Feedback Required",
      content: "Honestly, I thought we agreed on this. Are you kind of dumb?",
    },
    {
      id: 7,
      subject: "Get Your Act Together",
      content: "This is absolute garbage. How can you even call this work?",
    },
    {
      id: 8,
      subject: "What a Joke",
      content: "You must be completely clueless. This is pathetic!",
    },
    {
      id: 9,
      subject: "Get It Together",
      content: "I'm sick of your incompetence. You're dragging everyone down!",
    },
  ];

  return (
    <div className="email-page">
      <header className="header">
        <FaBars className="menu-icon" onClick={() => setIsMenuOpen(true)} />

        <input
          type="text"
          className="search-bar"
          placeholder="Search emails"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <FaUserCircle
          className="profile-icon"
          onClick={() => setIsPreviewOpen(true)}
        />
      </header>

      <aside className={`sidebar ${isMenuOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h2>Mail</h2>
          <FaTimes
            className="close-icon"
            onClick={() => setIsMenuOpen(false)}
          />
        </div>
        <ul>
          <li>
            <Link to="/dashboard">Admin Dashboard</Link>
          </li>{" "}
          {/* New Admin Dashboard link */}
          <li>Inbox</li>
          <li>Sent</li>
          <li>Drafts</li>
          <li>Spam</li>
          <li>Trash</li>
        </ul>
      </aside>

      <main className="email-list">
        <h2>Inbox</h2>
        <ul>
          {emails.map((email) => (
            <li key={email.id} className="email-item">
              <EmailDropdown email={email} /> {/* Pass full email object */}
            </li>
          ))}
        </ul>
      </main>

      <section className={`email-preview ${isPreviewOpen ? "open" : ""}`}>
        <div className="preview-header">
          <FaTimes
            className="close-icon"
            onClick={() => setIsPreviewOpen(false)}
          />
          <h2>Email Preview</h2>
        </div>
        <div className="preview-options">
          <p>Email</p>
          <p>Account Preferences</p>
          <p>Settings</p>
          <p>Logout</p>
        </div>
      </section>
    </div>
  );
};

export default EmailPage;
