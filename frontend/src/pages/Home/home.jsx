import React from 'react';
import './home.css';
import TrendCard from '../../components/TrendCard/TrendCard';
import IndexCard from '../../components/IndexCard/IndexCard';
import NewsCard from '../../components/NewsCard/newsCard';
import Header from '../../components/Header/header';
import Footer from '../../components/Footer/footer';
import { Link } from 'react-router-dom';
import newsArt from '../../assets/newsArt-resized.png'
import TechnicalAnalysisArt from '../../assets/TechnicalAnalysisArt-resized.png'
import sentimentArt from '../../assets/sentimentArt-resized.png'
import Logo from '../../assets/Logo-resized.png'
const Main = () => (

  <main className="main-container">
    <Header/>
    <section className="welcome-section">
      <div className="welcome-section-logo">
        <img src={Logo}  className='Logo-in-homepage'></img>

      </div>
      <div className='GoToDailyPredictions'>
        <Link className='GoToDailyPredictionsLink' to ="/prediction">Daily Predictions</Link>
      </div>

    </section>
      <div className='welcome-paragraph'>At iStock, we leverage key news insights, sentiment analysis, and technical analysis to provide you with comprehensive and actionable stock market information.</div>
    <section className="trends-section">
      <Link  to="/newscollection"  className='trends-section-links'> <TrendCard title="News Collection"  imgSrc={newsArt} />  </Link>
      <Link  to="/sentimentanalysis"  className='trends-section-links'><TrendCard title="Sentiment Analysis" imgSrc={sentimentArt} />  </Link>
      <Link  to="/technicalanalysis"  className='trends-section-links'> <TrendCard title="Technical Analysis" imgSrc={TechnicalAnalysisArt} />  </Link>
    </section>
    <div className='index-and-news'>

    <section className="index-section">
      <h2>Indices</h2>
      <IndexCard name="Nifty"   />
      <IndexCard name="Sensex"   />
      <IndexCard name="Bank Nifty"   />
    </section>

    <section className="news-section">
      <h2>Latest News</h2>
      <NewsCard />
    </section>
    
    </div>
    <Footer/>
  </main>

);

export default Main;
