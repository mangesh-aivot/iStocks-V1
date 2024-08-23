import React, { useState } from 'react';
import "./Signup.css";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header/header';
import Footer from '../../components/Footer/footer';
import { handleError, handleSuccess } from '../../utils';
import { ToastContainer } from 'react-toastify';

const Signup = () => {
  const navigate = useNavigate();

    const [signupInfo, setSignupInfo] = useState({
        name: '',
        email: '',
        password: ''
    })

  const handleChange = (e) => {
    const { name, value } = e.target;
    console.log(name, value);
    const copySignupInfo = { ...signupInfo };
    copySignupInfo[name] = value;
    setSignupInfo(copySignupInfo);
  };

  const handleSignup =async (e) => {
    e.preventDefault();
    const { name, email, password } = signupInfo;
    if (!name || !email || !password) {
      return handleError('Name, Email and Password are required')
    }
    try{
      const url = `http://localhost:5501/auth/signup`;
      const response = await axios.post(url, signupInfo, {
          headers: {
              'Content-Type': 'application/json'
          }
      });
      const result = response.data;

      const { success, message, error } = result;
      if (success) {
          handleSuccess(message);
          setTimeout(() => {
              navigate('/signin')
          }, 1000)

      } else if (error){
        const details = error?.details[0].message;
        handleError(details)
      } else if(!success){
        handleError(message);
      }
    }catch(err){
      handleError(err)
    }
      console.log()
  };
  return (
    <>
    <Header/>
    <div className="auth-container">
      <div className="auth-left">
        <h2 className='SignupWelcome'>Welcome Back!</h2>
        <button className="auth-btn"   onClick={() => {navigate("/signin") }}>Sign In</button>
      </div>
      <div className="auth-right">
        <h2 className='SignupWelcome'>Create Account</h2>
        <form   onSubmit={handleSignup}>
          <input type="text" name="name" placeholder="Name" value={signupInfo.name}  onChange={handleChange} required />

          <input type="email" 
             placeholder="Email" 
             name="email"
             className="input"
             value={signupInfo.email}
             onChange={handleChange}
             required/>

          <input type="password" 
             placeholder="Password" 
             name="password"
             className="input"
             value={signupInfo.password}
             onChange={handleChange}
             required
          />
          <button type="submit" className="signup-submit-btn">Sign Up</button>
        </form>
        <ToastContainer />
      </div>
    </div>
    <Footer/>
    </>
  );
};

export default Signup;

