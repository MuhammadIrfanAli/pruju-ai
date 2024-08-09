import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Card, CardContent, Typography, TextField, Button } from "@mui/material";

const RagDetails = ({rag: initRAG}) => {
//   const { ragId } = useParams();
  const [rag, setRag] = useState({
    ... initRAG
  });

//   useEffect(() => {
//     if (ragId) {
//       fetchRagDetails(ragId);
//     }
//   }, [ragId]);

//   const fetchRagDetails = async (id) => {
//     const response = await axios.get(`/api/rag_configs/${id}`);
//     setRag(response.data);
//   };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRag((prevRag) => ({
      ...prevRag,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.put(`/api/rag_configs/${ragId}`, rag);
    // Optionally, you can add some user feedback like a success message here.
  };

  return (
<>
        <Typography variant="h5" component="div" gutterBottom>
          Edit RAG Configuration
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="RAG Name"
            name="rag_name"
            value={rag.rag_name}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="RAG ID"
            name="rag_id"
            value={rag.rag_id}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
            disabled
          />
          <TextField
            label="Retriever Name"
            name="retriever_name"
            value={rag.retriever_name}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Retriever Type"
            name="retriever_type"
            value={rag.retriever_type}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Generator Name"
            name="generator_name"
            value={rag.generator_name}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Generator Type"
            name="generator_type"
            value={rag.generator_type}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Generator Key"
            name="generator_key"
            value={rag.generator_key}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <Button type="submit" variant="contained" color="primary" style={{ marginTop: 20 }}>
            Save
          </Button>
        </form>
      </>
  );
};

export default RagDetails;
