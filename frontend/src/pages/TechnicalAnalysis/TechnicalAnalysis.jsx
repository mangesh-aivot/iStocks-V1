import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Header from '../../components/Header/header';
import Footer from '../../components/Footer/footer';
import "./TechnicalAnalysis.css";

function TechnicalAnalysis() {

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/gettechnicals');
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
        <div className='TechnicalAnalysis-background'>
            <Header />
            <div className='TechnicalAnalysis-content'>
                <h1 className='TechnicalAnalysis-heading-text'>Technicals</h1>
                {loading && (
                    <div className='loading-spinner'>
                        <div className='spinner'></div>
                        <p>Loading...</p>
                    </div>
                )}
                {error && <p className='error-message'>Error: {error}</p>}
                {data && (
                    <table className='TechnicalAnalysis-table'>
                        <thead>
                            <tr>
                                <th>Company Name</th>
                                <th>Technicals</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((item, index) => (
                                <tr key={index}>
                                    <td>{item['Company Name']}</td>
                                    <td>{item['Technical']}</td>
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

export default TechnicalAnalysis;
