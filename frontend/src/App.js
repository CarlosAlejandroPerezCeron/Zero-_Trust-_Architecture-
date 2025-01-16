import React, { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  return token ? <Dashboard /> : <Login setToken={setToken} />;
}

export default App;

