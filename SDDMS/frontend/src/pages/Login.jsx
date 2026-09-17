import { useState } from "react";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");

    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }

    console.log("Login submitted");
    console.log("Username:", username);

    // Backend API will be connected here later.
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>SecureDMS</h1>

        <p className="subtitle">
          Secure Digital Document Management System
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>

            <input
              id="username"
              type="text"
              placeholder="Enter Your Username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;