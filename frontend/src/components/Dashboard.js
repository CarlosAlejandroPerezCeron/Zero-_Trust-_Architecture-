import React, { useEffect, useState } from "react";
import axios from "axios";

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
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
    </div>
  );
};

export default Dashboard;
