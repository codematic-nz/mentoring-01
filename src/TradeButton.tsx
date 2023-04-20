import { useState } from "react";

interface TradeButtonProps {
    text: string;
    onTradeClick: () => void;
}

export default function TradeButton({ text: text, onTradeClick }: TradeButtonProps) {
    return <button
        onClick={() => onTradeClick()}>
        {text}
    </button>;
}