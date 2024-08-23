import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoutes = ({element})=>{

    const loginToken = localStorage.getItem('token');
    const loggedInUser = localStorage.getItem('loggedInUser');

    if (loginToken && loggedInUser){
        return element;
    }else{
        return < Navigate to="/signin" /> ;
    }

}

export default ProtectedRoutes;