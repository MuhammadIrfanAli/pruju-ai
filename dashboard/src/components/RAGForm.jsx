import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

const RagForm = () => {
  const { ragId } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    rag_name: "",
    rag_id: "",
    retriever_name: "",
    retriever_type: "TYPE_A",
    generator_name: "",
    generator_type: "TYPE_X",
    generator_key: ""
  });

  useEffect(() => {
    if (ragId) {
      fetchRag(ragId);
    }
  }, [ragId]);

  const fetchRag = async (id) => {
    const response = await axios.get(`/api/rag_configs/${id}`);
    setFormData(response.data);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (ragId) {
      await axios.put(`/api/rag_configs/${ragId}`, formData);
    } else {
      await axios.post("/api/rag_configs/", formData);
    }
    navigate("/");
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        RAG Name:
        <input
          type="text"
          name="rag_name"
          value={formData.rag_name}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        RAG ID:
        <input
          type="text"
          name="rag_id"
          value={formData.rag_id}
          onChange={handleChange}
          required
          disabled={!!ragId}
        />
      </label>
      <label>
        Retriever Name:
        <input
          type="text"
          name="retriever_name"
          value={formData.retriever_name}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Retriever Type:
        <select
          name="retriever_type"
          value={formData.retriever_type}
          onChange={handleChange}
          required
        >
          <option value="TYPE_A">Type A</option>
          <option value="TYPE_B">Type B</option>
          <option value="TYPE_C">Type C</option>
        </select>
      </label>
      <label>
        Generator Name:
        <input
          type="text"
          name="generator_name"
          value={formData.generator_name}
          onChange={handleChange}
          required
        />
      </label>
      <label>
        Generator Type:
        <select
          name="generator_type"
          value={formData.generator_type}
          onChange={handleChange}
          required
        >
          <option value="TYPE_X">Type X</option>
          <option value="TYPE_Y">Type Y</option>
          <option value="TYPE_Z">Type Z</option>
        </select>
      </label>
      <label>
        Generator Key:
        <input
          type="text"
          name="generator_key"
          value={formData.generator_key}
          onChange={handleChange}
          required
        />
      </label>
      <button type="submit">Save</button>
    </form>
  );
};

export default RagForm;
