import React, { useState } from "react";
import "./Signin.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import Header from "../../components/Header/header";
import Footer from "../../components/Footer/footer";
import { handleError, handleSuccess } from "../../utils";

const Signin = () => {
  const navigate = useNavigate();

  const [loginInfo, setLoginInfo] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(name, value);
    const copyLoginInfo = { ...loginInfo };
    copyLoginInfo[name] = value;
    setLoginInfo(copyLoginInfo);
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const { email, password } = loginInfo;

    if (!email || !password) {
      return handleError("Email and Password both are required");
    }

    try {
      const url = `http://localhost:5501/auth/login`;

      const response = await axios.post(url, loginInfo, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = response.data;
      const {  message,success, jwtToken, userName } = result;
      if (success) {
        handleSuccess(message);
        localStorage.setItem("token", jwtToken);
        localStorage.setItem("loggedInUser", userName);
        setTimeout(() => {
          navigate("/home");
        }, 1000);
      // } else if (error) {
      //   const details = error?.details[0].message;
      //   handleError(details);
      } else if (!success) {
        handleError(message);
      }
    } catch (err) {
      handleChange(err);
    }
    console.log();
  };

  return (
    <>
      <Header />
      <div className="auth-container">
        <div className="auth-left">
          <h2>Hello, Friend!</h2>
          <p>Sign Up and begin your journey with us.</p>
          <button
            className="auth-btn"
            onClick={() => {
              navigate("/signup");
            }}
          >
            Sign Up
          </button>
        </div>
        <div className="auth-right">
          <h2 className="signinToIntelliForecast">Sign in to iStocks</h2>

          <form onSubmit={handleLogin}>
            <input
              type="email"
              placeholder="Enter email"
              name="email"
              className="input"
              value={loginInfo.email}
              onChange={handleChange}
              required
            />

            <input
              type="password"
              name="password"
              className="input"
              placeholder="Enter Password"
              value={loginInfo.password}
              onChange={handleChange}
              required
            />
            <button type="submit" className="signin-submit-btn">
              Sign In
            </button>
          </form>
          <ToastContainer />
        </div>
      </div>
      <Footer />
    </>
  );
};

export default Signin;
