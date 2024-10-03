"use client";

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import Chatbot from './components/Chatbot';
import { Send } from "lucide-react";

export default function LandingPage() {
  const [chatOpen, setChatOpen] = useState(false);
  const [text, setText] = useState("");
  const textAreaRef = useRef(null);
  const [submittedText, setSubmittedText] = useState(""); // State to hold submitted text for chatbot

  const handleSubmit = () => {
    setSubmittedText(text);
    setChatOpen(true);
  };

  const minHeight = 48; // Set min height (2 rows * 24px line-height)
  const maxHeight = 240; // Max height constraint (10 rows)

  const handleInputChange = (e) => {
    setText(e.target.value);
    autoResizeTextArea(); // Dynamically resize based on content
  };

  const autoResizeTextArea = () => {
    const textarea = textAreaRef.current;

    textarea.style.height = `${minHeight}px`; // Reset to minHeight initially
    const scrollHeight = textarea.scrollHeight;

    if (scrollHeight <= maxHeight) {
      textarea.style.height = `${scrollHeight}px`; // Grow if within max height
    } else {
      textarea.style.height = `${maxHeight}px`; // Cap at max height
      textarea.style.overflowY = "auto"; // Enable scroll if beyond max height
    }
  };

  // Ensure the textarea starts at minHeight on the initial render
  useEffect(() => {
    const textarea = textAreaRef.current;
    textarea.style.height = `${minHeight}px`; // Initialize at minimum height
  }, []);

  if (chatOpen) {
    return <Chatbot submittedText={submittedText} />;
  }

  return (
    <div>
      <div className="landing-page">
        <video
          autoPlay
          muted
          loop
          playsinlines="true"
          className="background-video"
        >
          <source
            src="https://cmsassets.rgpub.io/sanity/files/dsfx7636/news/409ab2fc369ba5e1fe50bac10c6676d7d1365a9f.mp4"
            type="video/mp4"
          />
        </video>
        <motion.div
          className="intro-text"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.5 }}
        >
          <img src="https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/7b76209193f1bfe190d3ae6ef8728328870be9c3-736x138.png?auto=format&amp;fit=fill&amp;q=80&amp;w=300" className="valorant-logo"></img>
          <h2>FORGE YOUR TEAM</h2>
          <p>THEIR POTENTIAL IS UP TO YOU.</p>
        </motion.div>

        <motion.div
          className="chatbox"
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: "40%", opacity: 1 }} // Set width to 50% of the viewport
          transition={{ duration: .5, ease: "easeOut" }}
        >
          <div className="input-container">
            <textarea
              ref={textAreaRef}
              value={text}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="Type your requirements..."
              rows={2}
              style={{ minHeight: `${minHeight}px`, maxHeight: `${maxHeight}px` }}
            />

          </div>
          <button
            onClick={handleSubmit}
            className="p-2 bg-red-500 rounded-md transition-colors duration-200 ease-in-out hover:bg-white group focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            <Send className="w-4 h-4 text-white group-hover:text-black transition-colors duration-200 ease-in-out" />
          </button>
        </motion.div>
      </div>
    </div>

  );
}
