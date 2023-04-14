import { useState } from "react";

interface TradeProps {
    initialText: string;
    amount: number;
    onTradeClick: (text: string, amount: number) => void;
}

export default function Trade({ initialText, amount, onTradeClick }: TradeProps) {
    const [text, setValue] = useState(initialText);
    return <button
        onClick={() => onTradeClick(initialText, amount)}>
        {text}
    </button>;
}