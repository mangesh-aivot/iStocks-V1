import { Navigate, Route, Routes } from 'react-router-dom';
import './App.css';



import ProtectedRoutes from "./components/ProtectedRoutes/ProtectedRoutes"


import Home from './pages/Home/home'
import Login from './pages/SignIn/Signin';
import Signup from './pages/Signup/Signup';
import PredictionPage from './pages/PredictionPage/Predictionpage';
import NewsCollectionPage from './pages/NewsCollectionPage/NewsCollectionPage';
import SentimentAnalysis from './pages/SentimentAnalysis/SentimentAnalysis';
import TechnicalAnalysis from './pages/TechnicalAnalysis/TechnicalAnalysis';


function App() {


  return (
    <div className="App">
     
      <Routes>

        <Route path="/" element={<Home/>} />
        <Route path="/home" element={<Home/>} />
        <Route path="/signin" element={<Login/>} />
        <Route path="/signup" element={<Signup/>} />
        <Route path="/newscollection" element={<NewsCollectionPage/>} />
        <Route path="/sentimentanalysis" element={<SentimentAnalysis/>}/>
        <Route path="/technicalanalysis" element={<TechnicalAnalysis/>}/>

        <Route path="/prediction" element={<ProtectedRoutes element={<PredictionPage />} />} />
      </Routes>
    </div>
  );
}

export default App;
