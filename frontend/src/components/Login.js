import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Typography, Container } from "@mui/material";

const API_URL = "http://localhost:8000";

const Login = ({ setToken }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mfaCode, setMfaCode] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        username,
        password,
        mfa_code: mfaCode
      });

      setToken(response.data.token);
      localStorage.setItem("token", response.data.token);
    } catch (error) {
      alert("Login failed!");
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>Zero Trust Login</Typography>
      <TextField fullWidth label="Username" onChange={(e) => setUsername(e.target.value)} />
      <TextField fullWidth type="password" label="Password" onChange={(e) => setPassword(e.target.value)} />
      <TextField fullWidth label="MFA Code" onChange={(e) => setMfaCode(e.target.value)} />
      <Button variant="contained" color="primary" fullWidth onClick={handleLogin}>Login</Button>
    </Container>
  );
};

export default Login;
