import React, { useState } from "react";
import axios from "axios";
import { Container, Paper, Typography, Box, Divider, TextField, Button, CircularProgress } from "@mui/material";

const LLMChat = () => {
  const [messages, setMessages] = useState([
    {
      sender: "user",
      text: "Hi, can you help me understand how to use React?",
    },
    {
      sender: "assistant",
      text: "Of course! React is a JavaScript library for building user interfaces. It allows you to create reusable UI components and manage the state of your application.",
    },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    // Add user message to chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "user", text: newMessage },
    ]);

    // Clear input field and start loading
    setNewMessage("");
    setLoading(true);

    try {
      // Send message to RAG chat endpoint
      const response = await axios.post("/api/rag_chat", { message: newMessage });

      // Add assistant response to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "assistant", text: response.data.message },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
        <Typography variant="h5" component="div" gutterBottom>
          LLM Chat
        </Typography>
        <Box flex={1} overflow="auto" paddingBottom={2}>
          {messages.map((msg, index) => (
            <Box
              key={index}
              style={{
                marginBottom: 10,
                padding: 10,
                backgroundColor: msg.sender === "user" ? "#e3f2fd" : "#f1f8e9",
                borderRadius: 8,
                maxWidth: "60%",
                alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              }}
            >
              <Typography variant="body1">{msg.text}</Typography>
            </Box>
          ))}
          {loading && (
            <Box style={{ textAlign: 'center', marginTop: 20 }}>
              <CircularProgress />
            </Box>
          )}
        </Box>
        <Divider style={{ margin: "20px 0" }} />
        <Box display="flex" alignItems="center">
          <TextField
            label="Type your message..."
            variant="outlined"
            fullWidth
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSendMessage();
            }}
          />
          <Button
            variant="contained"
            color="primary"
            style={{ marginLeft: 10 }}
            onClick={handleSendMessage}
          >
            Send
          </Button>
        </Box>
        </>
  );
};

export default LLMChat;
