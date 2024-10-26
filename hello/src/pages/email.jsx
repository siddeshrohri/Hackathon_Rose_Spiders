// src/EmailPage.js
import React, { useState } from 'react';
import './email.css'; // Ensure correct path to CSS file
import { FaBars, FaUserCircle, FaTimes } from 'react-icons/fa';

const EmailPage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState(''); // Define searchTerm and setSearchTerm here

  const emails = [
    { id: 1, sender: 'alice@example.com', subject: 'Meeting Reminder', time: '10:00 AM' },
    { id: 2, sender: 'bob@example.com', subject: 'Project Update', time: '9:45 AM' },
    { id: 3, sender: 'charlie@example.com', subject: 'Happy Birthday!', time: 'Yesterday' },
    { id: 4, sender: 'david@example.com', subject: 'Newsletter', time: '2 days ago' },
    { id: 5, sender: 'eve@example.com', subject: 'Invitation', time: '1 week ago' },
  ];

  return (
    <div className="email-page">
      <header className="header">
        <FaBars className="menu-icon" onClick={() => setIsMenuOpen(true)} />
        
        {/* Search Bar */}
        <input
          type="text"
          className="search-bar"
          placeholder="Search emails"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        <FaUserCircle className="profile-icon" onClick={() => setIsPreviewOpen(true)} />
      </header>

      {/* Sidebar */}
      <aside className={`sidebar ${isMenuOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Mail</h2>
          <FaTimes className="close-icon" onClick={() => setIsMenuOpen(false)} />
        </div>
        <ul>
          <li>Inbox</li>
          <li>Sent</li>
          <li>Drafts</li>
          <li>Spam</li>
          <li>Trash</li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="email-list">
        <h2>Inbox</h2>
        <ul>
          {emails.map((email) => (
            <li key={email.id} className="email-item">
              <div className="email-sender">{email.sender}</div>
              <div className="email-subject">{email.subject}</div>
              <div className="email-time">{email.time}</div>
            </li>
          ))}
        </ul>
      </main>

      {/* Email Preview */}
      <section className={`email-preview ${isPreviewOpen ? 'open' : ''}`}>
        <div className="preview-header">
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
