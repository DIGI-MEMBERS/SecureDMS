import { useState } from "react";

function OTP() {
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    setError("");

    if (!otp.trim()) {
      setError("Please enter the OTP.");
      return;
    }

    if (otp.length !== 6) {
      setError("OTP must contain 6 digits.");
      return;
    }

    console.log("OTP submitted:", otp);

    // OTP verification API will be connected here.
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Verify OTP</h1>

        <p className="subtitle">
          Enter the 6-digit OTP sent to your registered device.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="otp">OTP</label>

            <input
              id="otp"
              type="text"
              inputMode="numeric"
              maxLength="6"
              placeholder="Enter 6-digit OTP"
              value={otp}
              onChange={(event) => setOtp(event.target.value)}
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit">
            Verify OTP
          </button>
        </form>
      </div>
    </div>
  );
}

export default OTP;