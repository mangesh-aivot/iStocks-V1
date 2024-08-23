import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Header from '../../components/Header/header';
import Footer from '../../components/Footer/footer';
import "./SentimentAnalysis.css";

function SentimentAnalysis() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/getsentiment');
        console.log(response.data);
        setData(response.data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className='SentimentAnalysis-background'>
      <Header />
      <div className='SentimentAnalysis-content'>
        <h1 className='SentimentAnalysis-heading-text'>Sentiments</h1>
        {loading && (
          <div className='loading-spinner'>
            <div className='spinner'></div>
            <p>Loading...</p>
          </div>
        )}
        {data && (
          <table className='SentimentAnalysis-table'>
            <thead>
              <tr>
                <th>Company Name</th>
                <th>Sentiment</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  <td>{item['Company Name']}</td>
                  <td>{item['Sentiment']}</td>
                  <td>{item['Date']}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <Footer />
    </div>
  );
}

export default SentimentAnalysis;
