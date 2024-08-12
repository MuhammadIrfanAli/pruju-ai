import React, { useState } from "react";
import axios from "axios";

const RagSearch = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async (event) => {
    event.preventDefault();
    const response = await axios.get(`/api/rag_configs?search=${query}`);
    setResults(response.data);
  };

  return (
    <div>
      <h1>Search RAG Configurations</h1>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name or ID"
        />
        <button type="submit">Search</button>
      </form>
      <ul>
        {results.map((rag) => (
          <li key={rag.id}>
            {rag.rag_name} ({rag.rag_id})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RagSearch;
