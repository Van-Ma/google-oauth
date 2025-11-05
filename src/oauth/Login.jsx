import { useEffect, useState } from "react";
import "../oauth/Login.scss";

function Login() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/user", {
      credentials: "include", 
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.error) setUser(data);
      });
  }, []);

  return (
    <div className="user-authentication-page">
      <div className="login-container">
        {user ? (
          <h2 className="welcome-text">Welcome {user.name}!</h2>
        ) : (
          <>
            <h2 className="sign-in-text">Sign in</h2>
            <button
              className="login-btn"
              onClick={() =>
                (window.location.href = "http://localhost:5000/login/google")
              }
            >
              <img src="/google.png" alt="Google" /> Sign in with Google
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default Login;
