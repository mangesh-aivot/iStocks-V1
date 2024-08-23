import React, { useState, useEffect } from 'react';
import './IndexCard.css';


// const IndexCard = ({ name }) => {
//   const [price, setPrice] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   const fetchPrice = async () => {
//     setLoading(true);
//     try {
//       const response = await fetch(`http://127.0.0.1:8000/indices/${name}`);
//       if (!response.ok) {
//         throw new Error('Network response was not ok');
//       }
//       const data = await response.json();
//       setPrice(data.price);
//     } catch (error) {
//       setError(error.toString());
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchPrice(); 
//     const interval = setInterval(fetchPrice, 10000); // Fetch every 10 seconds
//     return () => clearInterval(interval);
//   }, [name]);

//   return (
//     <div className="index-card">
//       <h4 className='index-name'>{name}</h4>
//       {loading && <p>Updating...</p>}
//       {error && <p>Error: {error}</p>}
//       {!loading && !error && <p className='index-price'>{price}</p>}
//     </div>
//   );
// };

// export default IndexCard;


 
const IndexCard = ({ name }) => {
  const [data, setData] = useState({ price: null, change: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
 
  const fetchPrice = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/indices/${name}`);
     
      const result = await response.json();
      setData({ price: result.price, change: result.change });
    } catch (error) {
      setError(error.toString());
    } finally {
      setLoading(false);
    }
  };
 
  useEffect(() => {
    fetchPrice();
    const interval = setInterval(fetchPrice, 5000); // Fetch every 10 seconds
    return () => clearInterval(interval);
  }, [name]);
 
  const getChangeColor = (change) => {
    // Extract the numeric part of the change string
    const changeValue = parseFloat(change.replace(/[^\d.-]/g, ''));
    return changeValue < 0 ? 'red' : 'green';
  };
 
  return (
    <div className="index-card">
      <h4>{name}</h4>
      {loading}
      {error && <p>Error: {error}</p>}
      {!loading && !error && (
        <>
          <p className='index-price'> {data.price}</p>
          <p style={{ color: getChangeColor(data.change) }} className='index-change'> {data.change}</p>
        </>
      )}
    </div>
  );
};
 
export default IndexCard;