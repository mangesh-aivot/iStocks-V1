import React from 'react';
import Header from '../../components/Header/header';
import Footer from '../../components/Footer/footer';
import PredictionBox from '../../components/PredictionBox/PredictionBox';
import "./Predictionpage.css";
function PredictionPage() {
  return (
    <div className='predictionPageMainContainer'>
        <Header/>
        <PredictionBox/>
        <Footer/>
    </div>
  )
}

export default PredictionPage