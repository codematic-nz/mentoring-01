import { useState } from 'react'
import codematicLogo from './assets/codematic.svg'
import './App.css'
import Trade from './Trade'

function App() {
  const [balance, setBalance] = useState(0);

  function tradeClick(text: string, amount: number){
    console.log(`${text} trade clicked`);
    setBalance(balance + amount);
  }

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
        <Trade initialText="Sell" amount={-1} onTradeClick={tradeClick}></Trade>
        <Trade initialText="Buy" amount={1} onTradeClick={tradeClick}></Trade>
      </div>
      <p className="read-the-docs">
        Trading commodities to make profits
      </p>
    </div>
  )
}

export default App
