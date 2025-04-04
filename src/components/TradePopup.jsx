"use client"
import React, { useState, useEffect, useRef } from "react"

export default function TradePopup({ symbol, type, data, onClose, position }) {
  const [amount, setAmount] = useState(10)
  const popupRef = useRef(null)
  const [show, setShow] = useState(false)

  if (!data || !position) return null

  const { current_price, predicted_price } = data
  const quantity = amount / current_price
  const value_future = quantity * predicted_price
  const profit = value_future - amount

  const popupStyle = {
    position: "absolute",
    top: position.y + 10 + "px",
    left: position.x - 300 + "px",
    zIndex: 1000
  }

  useEffect(() => {
    setTimeout(() => setShow(true), 10)
    function handleClickOutside(event) {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        onClose()
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [onClose])

  return (
    <div
  ref={popupRef}
  style={{
    ...popupStyle,
    backgroundColor: "#a855f7",
    backdropFilter: "blur(8px)"
  }}
  className={`transform transition-all duration-300 ease-out text-white rounded-xl p-4 shadow-2xl border border-white/10 w-80 ${show ? "translate-x-0 opacity-100" : "translate-x-4 opacity-0"}`}
>
      <button
        onClick={onClose}
        className="absolute top-2 right-3 text-white/70 hover:text-white text-lg"
      >
        &times;
      </button>
      <h2 className="text-lg font-bold mb-2">
        Simulated {type === "buy" ? "Buy" : "Sell"}: {symbol}
      </h2>
      <p className="mb-1">Current Price: <strong>${current_price.toFixed(4)}</strong></p>
      <p className="mb-1">Predicted Price: <strong>${predicted_price.toFixed(4)}</strong></p>
      <div className="mb-2">
        <label className="block text-sm font-medium text-white/80">Amount in $:</label>
        <input
          type="number"
          value={amount}
          min={1}
          onChange={(e) => setAmount(Number(e.target.value))}
          className="mt-1 block w-full px-3 py-2 bg-zinc-800 border border-white/20 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-white"
        />
      </div>
      <p className="mb-2">Quantity: <strong>{quantity.toFixed(4)} {symbol.replace("USDC", "")}</strong></p>
      <p className="mb-4">
        Estimated {type === "buy" ? "Profit" : "Loss"}: {" "}
        <span className={profit >= 0 ? "text-green-400" : "text-red-400"}>
          {profit >= 0 ? "+" : "-"}${Math.abs(profit).toFixed(2)}
        </span>
      </p>
      <button
        onClick={onClose}
        className="w-full px-4 py-2 rounded-md bg-white/10 text-white border border-white/20 backdrop-blur-sm shadow-md hover:bg-white/20 transition"
      >
        Buy/Sell
      </button>
    </div>
  )
}
