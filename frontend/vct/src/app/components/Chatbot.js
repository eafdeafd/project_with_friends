"use client";

import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import Header from "./Header";
import { Send } from "lucide-react";
import { motion } from 'framer-motion';

export default function Chatbot({ submittedText }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const isTextSubmitted = useRef(false); // Ref to track if the message has been submitted

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = (submittedText) => {
    if (isTextSubmitted.current == false) {
      const newMessage = { text: submittedText, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setInputValue("");
    } else if (String(inputValue).trim()) {
      const newMessage = { text: inputValue, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setInputValue("");
    }
  };

  useEffect(() => {
    if (submittedText && submittedText.trim() && !isTextSubmitted.current) {
      handleSendMessage(submittedText);
      isTextSubmitted.current = true; // Set the flag to true after the first submission
    }
  }, [submittedText]);

  const buttons = [
    { label: 'ABOUT US', onClick: () => alert('About Us clicked!') },
    { label: 'SERVICES', onClick: () => alert('Services clicked!') },
    { label: 'CONTACT', onClick: () => alert('Contact clicked!') },
  ];

  return (
    <div>
      <motion.div
        initial={{ y: -100, opacity: 0 }}   // Start off-screen above the viewport
        animate={{ y: 0, opacity: 1 }}      // Drop down to position and fade in
        transition={{ type: 'tween', stiffness: 50, damping: 10 }}  // Smooth spring animation
        style={{ position: 'fixed', top: 0, width: '100%', zIndex: 1 }}  // Fix the header at the top
      >
        <Header title="RIOT GAMES" buttons={buttons} />
      </motion.div>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div className="flex flex-col h-screen light-gray text-gray-100 header-padding">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`max-w-[80%] p-3 rounded-lg ${message.sender === "user" ? "ml-auto bg-red-600" : "bg-gray-700"
                  }`}
              >
                {message.text}
              </div>
            ))}
          </div>
          <div className="p-4 dark-gray">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Type your requirements..."
                className="flex-1 p-2 light-gray text-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-200"
              />
              <button
                onClick={handleSendMessage}
                className="p-2 bg-red-500 rounded-md transition-colors duration-200 ease-in-out hover:bg-white group focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <Send className="w-6 h-6 text-white group-hover:text-black transition-colors duration-200 ease-in-out" />
              </button>
            </div>
          </div>
        </div>
      </motion.div>
    </div>

  )
}