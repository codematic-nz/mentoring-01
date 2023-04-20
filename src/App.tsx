import { useState } from 'react'
import codematicLogo from './assets/codematic.svg'
import './App.css'
import TradeButton from './TradeButton'

class Trade {
  constructor(
    id: Number,
    symbol: String,
    dateTime: Date,
    brokerId: Number,
    traderId: Number,
    clientId: Number,
    price: Number,
    volume: Number,
    side: String
  ) { }
}

function App() {
  const [trades, setTrades] = useState(Array<Trade>);
  const [balance, setBalance] = useState(0);

  function handleTrade(text: string, amount: number) {
    console.log(`${text} trade clicked`);
    setBalance(balance + amount);
    let updatedTrades = trades.slice();
    updatedTrades.push(new Trade(1, 'GOLD', new Date(), 2, 3, 4, 100.55, 20, 'BUY'));
    setTrades(updatedTrades);
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
        <TradeButton text="Sell" onTradeClick={() => handleTrade('SELL', -1)}></TradeButton>
        <TradeButton text="Buy" onTradeClick={() => handleTrade('BUY', 1)}></TradeButton>
      </div>
      <p className="read-the-docs">
        Trading commodities to make profits
      </p>
    </div>
  )
}

export default App
