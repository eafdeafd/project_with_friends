"use client";

import Image from "next/image";
import { useState } from "react";
import Header from "./components/Header";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      setMessages([...messages, inputValue]);
      setInputValue("");
    }
  };

  const buttons = [
    { label: 'About Us', onClick: () => alert('About Us clicked!') },
    { label: 'Services', onClick: () => alert('Services clicked!') },
    { label: 'Contact', onClick: () => alert('Contact clicked!') },
  ];

  return (
    <div className="home-container">
      <Header title="Welcome to Our Company" buttons={buttons}></Header>
      {/* Chatbox */}
      <div className="chatbox">
        {messages.map((message, index) => (
          <div key={index} className="message">
            {message}
          </div>
        ))}
      </div>

      {/* Textbox at the bottom */}
      <div className="textbox-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Hello Gamers"
          className="input-box"
        />
        <button onClick={handleSendMessage} className="send-button">
          Send
        </button>
      </div>
    </div>
  );
}
