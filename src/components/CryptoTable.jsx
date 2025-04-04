"use client"
import React, { useEffect, useState } from "react"
import { FaArrowUp, FaArrowDown } from "react-icons/fa"
import TradePopup from "./TradePopup"
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001"

export default function CryptoTable() {
  const [symbols, setSymbols] = useState([])
  const [data, setData] = useState({})
  const [activePopup, setActivePopup] = useState(null)
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" })
  const [expandedRow, setExpandedRow] = useState(null)

  const importantOrder = ["BTCUSDC", "ETHUSDC", "BNBUSDC", "SOLUSDC", "ADAUSDC"]

  const fetchSymbolData = (symbol) => {
    fetch(`${API}/api/predict/${symbol}`)
      .then((res) => {
        if (!res.ok) throw new Error()
        return res.json()
      })
      .then((json) => {
        if (!isFinite(json.current_price) || !isFinite(json.predicted_price)) throw new Error()
        setData((prev) => ({ ...prev, [symbol]: json }))
      })
      .catch((err) => {
        console.error(`❌ Error loading ${symbol}:`, err)
        setTimeout(() => fetchSymbolData(symbol), 10000)
      })
  }

  useEffect(() => {
    const loadSymbols = () => {
      fetch(`${API}/api/symbols`)
        .then((res) => res.json())
        .then((json) => {
          if (json.symbols) {
            setSymbols((prev) => {
              const newSymbols = json.symbols.filter((s) => !prev.includes(s))
              newSymbols.forEach(fetchSymbolData)
              return [...new Set([...prev, ...newSymbols])]
            })
          }
        })
        .catch((err) => console.error("❌ Error loading symbols:", err))
    }

    loadSymbols()
    const interval = setInterval(loadSymbols, 10000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const interval = setInterval(() => {
      symbols.forEach((symbol) => {
        fetch(`${API}/api/price/${symbol}`)
          .then((res) => res.json())
          .then((json) => {
            if (!isFinite(json.price)) return
            setData((prev) => ({
              ...prev,
              [symbol]: {
                ...prev[symbol],
                current_price: json.price
              }
            }))
          })
          .catch((err) => {
            console.error(`❌ Error updating price for ${symbol}:`, err)
          })
      })
    }, 30000)
    return () => clearInterval(interval)
  }, [symbols])

  const handleTrade = (e, symbol, type) => {
    const rect = e.currentTarget.getBoundingClientRect()
    setActivePopup({
      symbol,
      type,
      data: data[symbol],
      position: { x: rect.left, y: rect.top }
    })
  }

  const closePopup = () => setActivePopup(null)

  const handleSort = (key) => {
    setSortConfig((prev) => {
      const direction = prev.key === key && prev.direction === "asc" ? "desc" : "asc"
      return { key, direction }
    })
  }

  const toggleExpand = (symbol) => {
    setExpandedRow((prev) => (prev === symbol ? null : symbol))
  }

  const sortedSymbols = [...symbols].sort((a, b) => {
    const aIndex = importantOrder.indexOf(a)
    const bIndex = importantOrder.indexOf(b)

    if (sortConfig.key && data[a] && data[b]) {
      const aVal = data[a][sortConfig.key]
      const bVal = data[b][sortConfig.key]
      if (aVal < bVal) return sortConfig.direction === "asc" ? -1 : 1
      if (aVal > bVal) return sortConfig.direction === "asc" ? 1 : -1
      return 0
    }

    if (aIndex === -1 && bIndex === -1) return a.localeCompare(b)
    if (aIndex === -1) return 1
    if (bIndex === -1) return -1
    return aIndex - bIndex
  })

  const renderSortArrow = (key) => {
    if (sortConfig.key !== key) return null
    return sortConfig.direction === "asc" ? " ↑" : " ↓"
  }

  return (
    <div className="w-full p-4 bg-black/30 backdrop-blur-md rounded-xl shadow-lg border border-white/10">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-white/90">
          <thead className="text-xs uppercase bg-white/10 text-white">
            <tr>
              <th className="px-4 py-2 cursor-pointer" onClick={() => handleSort("symbol")}>Symbol{renderSortArrow("symbol")}</th>
              <th className="px-4 py-2 cursor-pointer" onClick={() => handleSort("current_price")}>Current Price{renderSortArrow("current_price")}</th>
              <th className="px-4 py-2 cursor-pointer" onClick={() => handleSort("predicted_price")}>AI Prediction{renderSortArrow("predicted_price")}</th>
              <th className="px-4 py-2">24h Ago Prediction</th>
              <th className="px-4 py-2">Trend</th>
              <th className="px-4 py-2 cursor-pointer" onClick={() => handleSort("ai_confidence")}>Accuracy{renderSortArrow("ai_confidence")}</th>
              <th className="px-4 py-2">AI Suggestion</th>
              <th className="px-4 py-2 cursor-pointer" onClick={() => handleSort("simulated_profit")}>Profit (10$){renderSortArrow("simulated_profit")}</th>
              <th className="px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {sortedSymbols.map((symbol) => {
              const crypto = data[symbol]
              const current_price = crypto?.current_price
              const predicted_price = crypto?.predicted_price
              const ai_confidence = crypto?.ai_confidence
              const prediction_24h_ago = crypto?.prediction_24h_ago

              if (
                current_price === undefined ||
                predicted_price === undefined ||
                ai_confidence === undefined
              ) {
                return (
                  <tr key={symbol} className="border-b border-white/10">
                    <td className="px-4 py-2">{symbol}</td>
                    <td colSpan={8} className="px-4 py-2 text-white/40">Loading...</td>
                  </tr>
                )
              }

              const isUp = predicted_price > current_price
              const suggestion = isUp ? "BUY" : "SELL"
              const gain = ((predicted_price - current_price) / current_price) * 10
              const profit = isUp ? gain : -Math.abs(gain)

              return (
                <React.Fragment key={symbol}>
                  <tr onClick={() => toggleExpand(symbol)} className="border-b border-white/10 hover:bg-white/5 transition cursor-pointer">
                    <td className="px-4 py-2">{symbol}</td>
                    <td className="px-4 py-2">
                      ${current_price < 0.0001 ? current_price.toFixed(8) : current_price < 0.01 ? current_price.toFixed(6) : current_price.toFixed(2)}
                    </td>
                    <td className="px-4 py-2">
                      ${predicted_price < 0.0001 ? predicted_price.toFixed(8) : predicted_price < 0.01 ? predicted_price.toFixed(6) : predicted_price.toFixed(2)}
                    </td>
                    <td className="px-4 py-2">
                      {prediction_24h_ago !== undefined && prediction_24h_ago !== null ? (
                        `$${prediction_24h_ago < 0.0001 ? prediction_24h_ago.toFixed(8) : prediction_24h_ago < 0.01 ? prediction_24h_ago.toFixed(6) : prediction_24h_ago.toFixed(2)}`
                      ) : "-"}
                    </td>
                    <td className="px-4 py-2">
                      {isUp ? <FaArrowUp className="text-green-500" /> : <FaArrowDown className="text-red-500" />}
                    </td>
                    <td className="px-4 py-2">{ai_confidence.toFixed(1)}%</td>
                    <td className="px-4 py-2 font-semibold text-blue-400">{suggestion}</td>
                    <td className="px-4 py-2">
                      {isFinite(profit) ? profit.toFixed(2) + " $" : "0.00 $"}
                    </td>
                    <td className="px-4 py-2 space-x-2">
                      <button
                        onClick={(e) => handleTrade(e, symbol, "buy")}
                        className="px-3 py-1 text-xs bg-green-600 hover:bg-green-700 text-white rounded-lg"
                      >
                        Buy
                      </button>
                      <button
                        onClick={(e) => handleTrade(e, symbol, "sell")}
                        className="px-3 py-1 text-xs bg-red-600 hover:bg-red-700 text-white rounded-lg"
                      >
                        Sell
                      </button>
                    </td>
                  </tr>
                  {expandedRow === symbol && (
                    <tr className="bg-white/5 text-white/80">
                      <td colSpan={9} className="px-4 py-4">
                        <div className="text-sm">
                          <p><strong>Details:</strong></p>
                          <ul className="list-disc list-inside">
                            <li>Symbol: {symbol}</li>
                            <li>Price now: ${current_price}</li>
                            <li>Predicted price: ${predicted_price}</li>
                            <li>Predicted 24h ago: ${prediction_24h_ago ?? "-"}</li>
                            <li>Accuracy: {ai_confidence.toFixed(1)}%</li>
                            <li>Suggestion: {suggestion}</li>
                            <li>Estimated profit for $10: {profit.toFixed(2)} USD</li>
                          </ul>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              )
            })}
          </tbody>
        </table>
      </div>

      {activePopup && (
        <TradePopup
          symbol={activePopup.symbol}
          type={activePopup.type}
          data={activePopup.data}
          position={activePopup.position}
          onClose={closePopup}
        />
      )}
    </div>
  )
}