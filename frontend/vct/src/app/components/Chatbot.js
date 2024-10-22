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
  const textAreaRef = useRef(null);
  const messageContainerRef = useRef(null); // Ref for message container

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    autoResizeTextArea(); // Dynamically resize based on content
  };

  const handleSendMessage = async (submittedText) => {
    if (isTextSubmitted.current === false && submittedText) {
      addUserMessage(submittedText);
      isTextSubmitted.current = true;
    } else if (inputValue.trim()) {
      addUserMessage(inputValue);
    }

    const textarea = textAreaRef.current;
    textarea.style.height = `${minHeight}px`;

    // After sending the message, call the backend and wait for the response
    const response = await sendMessageToBackend(inputValue);
    addBotMessage(response);

    setInputValue(""); // Clear input after sending
  };

  const addUserMessage = (text) => {
    const newMessage = { text, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  const addBotMessage = (text) => {
    const newMessage = { text, sender: "bot" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  const sendMessageToBackend = async (message) => {
    try {
      const response = await fetch('YOUR_BACKEND_API_URL', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }), // Adjust the body structure as per backend
      });
      const data = await response.json(); // Assuming the response is in JSON format
      return data.reply; // Adjust according to backend response structure
    } catch (error) {
      console.error('Error sending message to backend:', error);
      return 'Sorry, something went wrong.';
    }
  };

  const minHeight = 48; // Set min height (2 rows * 24px line-height)
  const maxHeight = 240; // Max height constraint (10 rows)

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

  // Scroll to bottom when a new message is added
  useEffect(() => {
    const container = messageContainerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight; // Scroll to bottom
    }
  }, [messages]);

  useEffect(() => {
    const textarea = textAreaRef.current;
    textarea.style.height = `${minHeight}px`; // Initialize at minimum height
    if (submittedText && submittedText.trim() && !isTextSubmitted.current) {
      handleSendMessage(submittedText);
      isTextSubmitted.current = true; // Set the flag to true after the first submission
    }
  }, [submittedText]);

  const buttons = [
    { label: 'ABOUT US' },
    { label: 'SERVICES' },
    { label: 'CONTACT' },
  ];

  return (
    <div className="fullscreen-div">
      <motion.div
        initial={{ y: -100, opacity: 0 }}   // Start off-screen above the viewport
        animate={{ y: 0, opacity: 1 }}      // Drop down to position and fade in
        transition={{ type: 'tween', stiffness: 50, damping: 10 }}  // Smooth spring animation
      >
        <Header title="RIOT GAMES" buttons={buttons} />
      </motion.div>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >

        <div className="flex flex-col h-screen dark-gray text-gray-100">
          <div ref={messageContainerRef} className="flex-1-main p-4 space-y-4 overflow-y-auto"> {/* Added flex-col for vertical stacking */}
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message max-w-[80%] self-start p-3 rounded-lg ${message.sender === "user" ? "self-end bg-red-600" : "bg-gray-700"
                  }`} // Use self-start for received and self-end for sent
              >
                {message.text}
              </div>
            ))}
          </div>
          <motion.div
            className="chatbox-main fixed bottom-0 left-0 right-0 w-full mx-auto mb-4" // Fixed position to bottom
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: "40%", opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <div className="input-container-main">
              <textarea
                ref={textAreaRef}
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={(e) => {
                  if (e.key === "Enter") {
                    if (e.shiftKey) {
                      // Allow new line when Shift + Enter is pressed
                      return;
                    } else {
                      e.preventDefault(); // Prevent new line on submit
                      handleSendMessage(inputValue);
                    }
                  }
                }}
                placeholder="Type your requirements..."
                rows={2}
                style={{ minHeight: `${minHeight}px`, maxHeight: `${maxHeight}px` }}
              />
            </div>
            <button
              onClick={() => handleSendMessage(inputValue)}
              className="p-2 bg-red-500 rounded-md transition-colors duration-200 ease-in-out hover:bg-white group focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              <Send className="w-4 h-4 text-white group-hover:text-black transition-colors duration-200 ease-in-out" />
            </button>
          </motion.div>
        </div>

      </motion.div>
    </div>

  )
}