import { useEffect, useState } from "react";
import axios from "axios";
import React from "react";
import "./PredictionBox.css";

function PredictionBox() {
  const [data, setData] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const formatTime = (date) => {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? "0" + minutes : minutes;
    const strTime = hours + ":" + minutes + " " + ampm;
    return strTime;
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(
          "http://localhost:8000/get-predictions"
        );
        console.log("Response from API:", response.data);

        if (response.data.Message) {
          setMessage(response.data.Message);
          setData([]);
        } else {
          setData(response.data);
          setMessage("");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        setMessage("Error fetching data");
        setData([]);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  const RefreshPredictions = () => {
    window.location.reload();
  };

  return (
    <div className="predictionBoxContainer">
      <div className="stockToBuy">
        <p className="stockToBuyText"> Stocks To Buy </p>
        <button
          onClick={RefreshPredictions}
          className="refreshButtonPredictions"
        >
          Refresh
        </button>
      </div>
      <div className="predictionBoxDateTimeContainer">
        <p className="predictionBoxTimeDate">
          Date: {time.toLocaleDateString()}
        </p>
        <p className="predictionBoxTimeDate">Time: {formatTime(time)}</p>
      </div>
      <div className="predictionTableContainer">
        {loading ? (
          <div className="loader">Please wait, data is being loaded.</div>
        ) : message ? (
          <p>{message}</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Company Name</th>
                <th>
                  TP<sub>1</sub>
                </th>
                <th>
                  TP<sub>2</sub>
                </th>
                <th>
                  TP<sub>3</sub>
                </th>
                <th>Buy at</th>
                <th>Stop Loss</th>
                <th>Time</th>
                <th>CMP</th>
                <th>Volume</th>
                <th>Technicals</th>
                <th>Fundamental</th>
                <th>Sentiment</th>
                <th>News</th>
              </tr>
            </thead>

            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  <td>{row["Company Name"]}</td>
                  <td>{row["TP1"]}</td>
                  <td>{row["TP2"]}</td>
                  <td>{row["TP3"]}</td>
                  <td>{row["Buy at"]}</td>
                  <td>{row["SL"]}</td>
                  <td>{row["Time"]}</td>
                  <td>{row["CMP"]}</td>
                  <td>{row["Volume"]}</td>
                  <td>{row["Technical"]}</td>
                  <td>{row["Fundamental"]}</td>
                  <td>{row["Sentiment"]}</td>
                  <td>
                    <div className="newsBox">
                      {row["News"].split('", "').map((news, i) => (
                        <div key={i} className="newsItem">
                          {news.replace(/^"|"$/g, "")}
                        </div>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
            {/* </div> */}
          </table>
        )}
      </div>
    </div>
  );
}

export default PredictionBox;
