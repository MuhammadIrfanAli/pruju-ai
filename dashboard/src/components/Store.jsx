import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Container, Paper, Typography, Box, Divider, TextField, Button, CircularProgress, Card, CardContent, Grid } from "@mui/material";
import { Feder } from '@zilliz/feder';
import * as d3 from 'd3';

const API_URL = 'http://localhost:8001/api'


const Store = () => {
  // const [chunks, setChunks] = useState()

  const [query, setQuery] = useState('');
  // const [results, setResults] = useState([]);
  // const [queryVector, setQueryVector] = useState([]);
  const [loading, setLoading] = useState(false);
  const [feder, setFeder] = useState();



  useEffect(()=>{
    getChunks()
  }, [])


    const handleSearch = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/rag/1/search/?query=${query}`);
            const data = await response.json();
            document.getElementById('feder-store').innerHTML = ''
            feder.setSearchParams({ nprobe: 12 }).searchRandTestVec(data.query_vector);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
        setLoading(false);
    };

    const initFeder = (chunks) => {
      const mediaCallback = (rowId) =>
        rowId in chunks
          ? chunks[rowId]
          : null;

      const feder_module = new Feder({
        filePath: `${API_URL}/rag/1/ivfflat1.index`,
        source: "faiss",
        domSelector: '#feder-store', // attach dom to render
        viewParams: {
          mediaType: "text",
          mediaCallback,
          projectSeed: 1235,
          projectMethod: "umap"
        }
      })
      return feder_module
    }

    const getChunks = async () => {
      try {
          const response = await fetch(`${API_URL}/rag/1/chunks`);
          const data = await response.json();
          const feder_module = initFeder(data.documents);
          feder_module.setSearchParams({ nprobe: 22 }).searchRandTestVec();
          setFeder(feder_module);
      } catch (error) {
          console.error('Error fetching search results:', error);
      }
  };

    return (
        <>
          <Typography variant="h5" gutterBottom>
            Search
          </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={8}>
            <TextField
              label="Search"
              variant="outlined"
              fullWidth
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </Grid>
          <Grid item xs={4}>
            <Button
              variant="contained"
              color="primary"
              fullWidth
              onClick={handleSearch}
            >
              Search
            </Button>
          </Grid>
        </Grid>
            <div id="feder-store"></div>
        </>
    );

};

export default Store;
