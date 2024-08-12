import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardActions, Typography, Button, Grid, Container, Tabs, Tab, Box } from "@mui/material";
import RagDetails from "./RagDetails";
import LLMChat from "./LLMChat";
import Store from "./Store";

const RagList = () => {
  const [rags, setRags] = useState([]);
  const [selectedRag, setSelectedRag] = useState(null);
  const [tabIndex, setTabIndex] = useState(0);
  const navigate = useNavigate();
  const { ragId } = useParams();

  useEffect(() => {
    fetchRags();
  }, []);

  useEffect(() => {
    if (ragId) {
      setSelectedRag(ragId);
      setTabIndex(1); // Automatically switch to the "Edit" tab when a RAG is selected
    }
  }, [ragId]);

  const fetchRags = async () => {
    const response = await axios.get("http://localhost:8001/api/rag/");
    setRags(response.data);
    setSelectedRag(response.data[0]);

  };

  const deleteRag = async (id) => {
    await axios.delete(`/api/rag_configs/${id}`);
    fetchRags();
  };

  const handleRagClick = (rag) => {
    setSelectedRag(rag);
    // navigate(`/${id}`);
  };

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        RAG Configurations
      </Typography>
      {/* <Button variant="contained" color="primary" component={Link} to="/create">
        Create New RAG
      </Button> */}
      <Grid container spacing={3} style={{ marginTop: 20 }}>
        <Grid item xs={12} md={3}>
          {rags.map((rag) => (
            <Card
              key={rag.id}
              onClick={() => handleRagClick(rag)}
              style={{ cursor: "pointer", marginBottom: 20 }}
            >
              <CardContent>
                <Typography variant="h6">{rag.rag_name}</Typography>
                <Typography color="textSecondary">RAG ID: {rag.rag_id}</Typography>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary" component={Link} to={`/edit/${rag.rag_id}`}>
                  Edit
                </Button>
                <Button size="small" color="secondary" onClick={() => deleteRag(rag.rag_id)}>
                  Delete
                </Button>
              </CardActions>
            </Card>
          ))}
        </Grid>
        <Grid item xs={12} md={9}>
          <Card>
            <CardContent>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabIndex} onChange={handleTabChange} aria-label="rag details tabs">
              <Tab label="Edit" />
              <Tab label="Chat" />
              <Tab label="Store" />
              <Tab label="Evaluation" />
            </Tabs>
            </Box>
                  
            <Box p={3}>
              {
                selectedRag ? (
                  tabIndex == 0 ? <RagDetails rag={selectedRag} />: 
                  tabIndex == 1 ? <LLMChat/>:  
                  tabIndex == 2 ? <Store/>: 
                  tabIndex == 3 ? <h3>Evaluation</h3>:  null

                ) : null
              }
            </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default RagList;
