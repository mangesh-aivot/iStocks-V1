import React, { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import "./header.css";
import { handleSuccess } from "../../utils";
import { ToastContainer } from "react-toastify";
import Logo from "../../assets/Logo-resized.png";

const Header = () => {
  const navigate = useNavigate();
  const [isLoggedIn,setisLoggedIn] = useState(false)

  const Token = localStorage.getItem('token');
  const userName = localStorage.getItem('loggedInUser')
  // console.log('UserName:',userName);

  useEffect(()=>{
    if(Token && userName){
      setisLoggedIn(true);
    }
  },[Token,userName]);
  const handleLogout = (e) => {
    localStorage.removeItem("token");
    localStorage.removeItem("loggedInUser");
    setisLoggedIn(false);
    handleSuccess("User Loggedout");
    setTimeout(() => {
      navigate("/home");
    }, 1000);
  };

  return (
    <header className="header-container">
      <img src={Logo} className="header-logo" alt="Logo" />
      <nav className="header-nav-links">
        <li className="nav-links">
          <Link className="nav-link" to="/">
            Home
          </Link>
        </li>
        {!isLoggedIn && (
          <>
            <li className="nav-links">
              <Link className="nav-link" to="/signup">
                Signup
              </Link>
            </li>
            <li className="nav-links">
              <Link className="nav-link" to="/signin">
                Login
              </Link>
            </li>
          </>
        )}
        {isLoggedIn && (
          <>
          <li className="nav-links">
            <div onClick={handleLogout} className="nav-link">
              Logout
            </div>

          </li>
          <li className="nav-links"><p>Hi,{userName} </p></li>
          </>
        )}
      </nav>
      <ToastContainer />
    </header>
  );
};

export default Header;
