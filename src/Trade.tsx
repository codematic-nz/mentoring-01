import { useState } from "react";

interface TradeProps {
    buySell: string;
    amount: number;
    onTradeClick: (text: string, amount: number) => void;
}

export default function Trade({ buySell: buySell, amount, onTradeClick }: TradeProps) {
    const [text, setValue] = useState(buySell);
    return <button
        onClick={() => onTradeClick(buySell, amount)}>
        {text}
    </button>;
}