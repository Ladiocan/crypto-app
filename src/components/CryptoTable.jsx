"use client"
import React, { useEffect, useState } from "react"

export default function CryptoTable() {
  const [data, setData] = useState([])

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/update")
      .then((res) => res.json())
      .then((json) => setData(json.results || []))
      .catch((err) => console.error("Eroare la fetch:", err))
  }, [])

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Current Price</th>
            <th>Predicted</th>
            <th>RSI</th>
            <th>SMA</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {data.map((crypto, i) => (
            <tr key={i}>
              <td>{crypto.symbol}</td>
              <td>{crypto.current_price.toFixed(4)}</td>
              <td>{crypto.predicted_price?.toFixed(4) || "-"}</td>
              <td>{crypto.RSI?.toFixed(2) || "-"}</td>
              <td>{crypto.SMA?.toFixed(2) || "-"}</td>
              <td>{crypto.Recommendation || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
