import { useState } from 'react'
import codematicLogo from '/codematic.svg'
import './App.css'

function App() {
  const [balance, setCount] = useState(0)

  return (
    <div className="App">
      <div>
        <a href="https://codematic.co.nz" target="_blank">
          <img src={codematicLogo} className="logo" alt="codematic logo" />
        </a>
      </div>
      <h1>Trade Simulator</h1>
      <div className="card">
        <div className="card">Balance: {balance}</div>
        <button onClick={() => setCount((balance) => balance + 1)}>
          buy
        </button>
        <button onClick={() => setCount((balance) => balance - 1)}>
          sell
        </button>
      </div>
      <p className="read-the-docs">
        Trading commodities to make profits
      </p>
    </div>
  )
}

export default App
