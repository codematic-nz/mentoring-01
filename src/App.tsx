import { useState } from 'react'
import codematicLogo from './assets/codematic.svg'
import './App.css'
import TradeButton from './TradeButton'

class Trade {
  static BUY_SIDE: string = 'BUY';
  static SELL_SIDE: string = 'SELL';
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
  const [totalVol, setTotalVol] = useState(10);
  const [funds, setFunds] = useState(1000.0);
  let nextTradeId: Number = 1;
  const symbol: string = 'GOLD';
  const brokerId: number = 1;
  const traderId: number = 1;
  const clientId: number = 1;
  let price: number = 100.55;
  let volume: number = 1;

  function handleTrade(side: string) {
    console.log(`${side} trade`);
    const cost: number = price * ((side === Trade.SELL_SIDE) ? volume : (volume * -1));
    const volChange: number = (side === Trade.BUY_SIDE) ? volume : (volume * -1);
    const newFundsRounded = parseFloat((funds + cost).toFixed(2));
    setTotalVol(totalVol + volChange);
    setFunds(newFundsRounded);
    let updatedTrades = trades.slice();
    updatedTrades.push(new Trade(
      nextTradeId,
      symbol,
      new Date(),
      brokerId,
      traderId,
      clientId,
      price,
      volume,
      side
    ));
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
        <div className="card">Funds: <span data-test-id="funds">{funds}</span></div>
        <div data-test-id="total-vol" className="card">Total Vol: {totalVol}</div>
        <div data-test-id="price" className="card">Current Price: {price}</div>
        <TradeButton text="Sell" onTradeClick={() => handleTrade(Trade.SELL_SIDE)}></TradeButton>
        <TradeButton text="Buy" onTradeClick={() => handleTrade(Trade.BUY_SIDE)}></TradeButton>
      </div>
      <p className="read-the-docs">
        Trading commodities to make profits
      </p>
    </div>
  )
}

export default App
