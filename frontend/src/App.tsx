import { useEffect, useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState("")

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/hello')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  return (
    <>
      <div className="card">
        <h1>Traffic Flow Prediction System - GUI</h1>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>Response from <a>http://127.0.0.1:8000/api/hello</a></p>
        <h3>{message}</h3>
      </div>
    </>
  )
}

export default App
