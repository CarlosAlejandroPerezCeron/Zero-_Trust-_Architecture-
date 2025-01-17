import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Typography, Button } from "@mui/material";

const API_URL = "http://localhost:8000";

const Dashboard = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios.get(`${API_URL}/secure-endpoint`, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(response => {
      setMessage(response.data.message);
    }).catch(() => {
      setMessage("Access Denied");
    });
  }, []);

  return (
    <Container maxWidth="sm">
      <Typography variant="h3">Welcome to Zero Trust Dashboard</Typography>
      <Typography variant="h6">{message}</Typography>
      <Button variant="contained" color="secondary" onClick={() => localStorage.removeItem("token")}>Logout</Button>
    </Container>
  );
};

export default Dashboard;
