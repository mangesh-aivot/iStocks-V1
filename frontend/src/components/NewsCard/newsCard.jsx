import React, { useEffect, useState } from 'react';
import './newsCard.css';

const NewsCard = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/getnews')
      .then(response => response.json())
      .then(data => setNews(data.News))
      .catch(error => console.error('Error fetching news:', error));
  }, []);

  return (
    <div>
      {news.map((headline, index) => (
        <div className="news-card" key={index}>
          <h4>{headline}</h4>
        </div>
      ))}
    </div>
  );
};

export default NewsCard;

