"use client";

import { useState, useEffect, useRef } from "react";
import Header from "./Header";
import { Send, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from 'framer-motion';

export default function Chatbot({ submittedText }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const isTextSubmitted = useRef(false); // Ref to track if the message has been submitted
  const textAreaRef = useRef(null);
  const messageContainerRef = useRef(null); // Ref for message container

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    autoResizeTextArea(); // Dynamically resize based on content
  };

  // Update the function that the button send calls
  const handleSendMessage = async (submittedText) => {
    let messageToSend = "";
    if (isTextSubmitted.current === false && submittedText) {
      addUserMessage(submittedText);
      isTextSubmitted.current = true;
      setInputValue("");
      messageToSend = submittedText;
    } else if (inputValue.trim()) {
      addUserMessage(inputValue);
      messageToSend = submittedText;
    }

    const textarea = textAreaRef.current;
    textarea.style.height = `${minHeight}px`;

    // Clear input immediately after submitting the message and disable text area until response
    setInputValue("");
    setIsWaitingForResponse(true);

    try {
      // After sending the message, call the backend and wait for the response
      const newSessionId = await sendMessageToBackend(messageToSend, sessionId); // Use the stored message
      if (newSessionId) {
        setSessionId(newSessionId); // Update session ID if received
      }
    } finally {
      setIsWaitingForResponse(false); // Re-enable textarea after response
    }
  };

  const addUserMessage = (text) => {
    const newMessage = { text, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
  };

  const addBotMessage = (text) => {
    // Create a new bot message
    const newMessage = { text, sender: "bot" };
    setMessages((prevMessages) => {
      return [...prevMessages, newMessage];
    });

  };

  const sendMessageToBackend = async (message, sessionId) => {
    const url = new URL('http://127.0.0.1:8000/query_agent');
    url.searchParams.append('prompt', message); // Add the user message

    // Only add session_id if it's available
    if (sessionId) {
      url.searchParams.append('session_id', sessionId); // Add the session ID
    }

    try {
      const response = await fetch(url.toString(), {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;
      let newSessionId = null; // To store the session ID from the response

      // Read the stream
      while (!done) {
        const { done: isDone, value } = await reader.read();
        done = isDone;

        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const messageData = JSON.parse(chunk);

          // Capture the session ID from the response and store
          if (messageData.session_id) {
            newSessionId = messageData.session_id;
          }

          // Append the bot message to the chat
          addBotMessage(messageData.response);
        }
      }

      return newSessionId; // Return the new session ID for future requests
    } catch (error) {
      console.error('Error sending message to backend:', error);
      // Create a new bot message for the error, don't append to previous
      addBotMessage('Sorry, something went wrong.');
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

    // Prevent new lines by explicitly clearing any leading/trailing whitespaces
    const trimmedSubmittedText = submittedText?.trim();

    if (trimmedSubmittedText && !isTextSubmitted.current) {
      setInputValue(""); // Clear the input first to prevent a new line
      handleSendMessage(trimmedSubmittedText); // Send the trimmed message
      isTextSubmitted.current = true; // Set the flag to true after the first submission
    }
  }, [submittedText]);

  useEffect(() => {
    if (!isWaitingForResponse && textAreaRef.current) {
      textAreaRef.current.focus(); // Refocus the textarea when re-enabled when receiving response
      setInputValue("");
    }
  }, [isWaitingForResponse]);

  const buttons = [
    { label: 'DEMO', link: 'https://youtube.com/' },
    { label: 'HACKATHON', link: 'https://vcthackathon.devpost.com/' },
    { label: 'REPOSITORY', link: 'https://github.com/eafdeafd/vct-hackathon' },
  ];

  const messageVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 }
  }

  return (
    <div className="fullscreen-div">
      <motion.div
        initial={{ y: -100, opacity: 0 }}   // Start off-screen above the viewport
        animate={{ y: 0, opacity: 1 }}      // Drop down to position and fade in
        transition={{ type: 'tween', stiffness: 50, damping: 10 }}  // Smooth spring animation
      >
        <Header title="VCT MANAGER" buttons={buttons} />
      </motion.div>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >

        <div className="flex flex-col h-screen dark-gray text-gray-100">
          <div ref={messageContainerRef} className="flex-1-main p-4 space-y-4 overflow-y-auto"> {/* Added flex-col for vertical stacking */}
            <AnimatePresence initial={false}>
              {messages.map((message, index) => (
                <motion.div
                  key={index}
                  variants={messageVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                  transition={{
                    type: "spring",
                    stiffness: 500,
                    damping: 50,
                    mass: 1
                  }}
                  className={`message max-w-[80%] p-3 rounded-lg ${message.sender === "user"
                    ? "self-end bg-red-600 text-white ml-auto"
                    : "self-start bg-gray-700 text-white"
                    }`}
                >
                  {message.text}
                </motion.div>
              ))}
            </AnimatePresence>
            {isWaitingForResponse && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.3 }}
                className="flex justify-center items-center p-4"
              >
                <Loader2 className="w-6 h-6 text-gray-400 animate-spin" />
              </motion.div>
            )}
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
                disabled={isWaitingForResponse}
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
              disabled={isWaitingForResponse}
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