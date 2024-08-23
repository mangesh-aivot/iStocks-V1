import React from 'react';
import './TrendCard.css';

const TrendCard = ({ title ,imgSrc}) => (
  <div className="trend-card">
    <h3 className='trend-card-text'>{title}</h3>
    <img src={imgSrc}  className="trend-card-image" />
  </div>
);

export default TrendCard;
