import React, { useState } from "react";
import axios from "axios";

function Login() {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [token, setToken] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/auth/login", formData);
      setToken(response.data.access_token);
      localStorage.setItem("token", response.data.access_token);
      alert("Login realizado com sucesso!");
    } catch (err) {
      setError("Usuário ou senha inválidos.");
    }
  };

  return (
    <div className="login-container">
      <h2>Login no CME System</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Usuário"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Senha"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Entrar</button>
      </form>
      {error && <p className="error">{error}</p>}
      {token && <p className="success">Token armazenado com sucesso.</p>}
    </div>
  );
}

export default Login;
