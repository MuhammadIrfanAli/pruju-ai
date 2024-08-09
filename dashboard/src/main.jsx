import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RagList from "./components/RAGList";
import RagForm from "./components/RAGForm";
import RagSearch from "./components/RAGSearch";
import "./index.css";

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<RagList />} />
        <Route path="/create" element={<RagForm />} />
        <Route path="/edit/:ragId" element={<RagForm />} />
        <Route path="/search" element={<RagSearch />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById("root")
);
