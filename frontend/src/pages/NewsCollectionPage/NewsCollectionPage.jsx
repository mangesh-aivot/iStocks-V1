import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'
import Header from "../../components/Header/header"
import Footer from "../../components/Footer/footer"
import "./NewsCollectionPage.css"
function NewsCollectionPage() {
    const [news, setNews] = useState([]);

    useEffect(() => {
      fetch('http://127.0.0.1:8000/getnews')
        .then(response => response.json())
        .then(data => setNews(data.News))
        .catch(error => console.error('Error fetching news:', error));
    }, []);
  

  return (
    <>
    <Header/>
    <div className='News-body'>
      <h1 className='News-body-header'>Today's News</h1>
      {news.map((headline, index) => (
        <div className="news-card" key={index}>
          <h4>{headline}</h4>
        </div>
      ))}
    </div>
    <Footer/>
    </>
  )
}

export default NewsCollectionPage;