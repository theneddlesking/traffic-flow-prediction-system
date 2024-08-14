import { useEffect, useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState("")
  const [number1, setNumber1] = useState('');
  const [number2, setNumber2] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/hello')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  const handleAddition = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/add', {
        params: {
          a: number1,
          b: number2
        }
      });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error fetching the result:', error);
    }
  };

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
      <div>
      <p>Use endpoint <a>http://127.0.0.1:8000/api/add</a> to conduct basic arithmetic</p>
      <input
        type="number"
        value={number1}
        onChange={(e) => setNumber1(e.target.value)}
        placeholder="Enter first number"
      />
      <input
        type="number"
        value={number2}
        onChange={(e) => setNumber2(e.target.value)}
        placeholder="Enter second number"
      />
      <button onClick={handleAddition}>Add</button>
      {result !== null && (
        <div>
          <h2>Result: {result}</h2>
        </div>
      )}
    </div>
    </>
  )
}

export default App
