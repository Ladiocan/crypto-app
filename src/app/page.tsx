import Head from "next/head"
import CryptoTable from "../components/CryptoTable"

export default function Home() {
  return (
    <>
      <Head>
        <title>Crypto AI Predictions 24h | ciocan.eu</title>
        <meta name="description" content="AI-based crypto price predictions for the next 24 hours. Powered by Binance data & machine learning." />
        <meta name="keywords" content="crypto predictions, AI crypto forecast, Binance AI, crypto price prediction, Bitcoin prediction, Ethereum forecast, Web3 analytics, AI trading tools, crypto signals, crypto AI app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta property="og:title" content="Crypto AI Predictions 24h" />
        <meta property="og:description" content="Real-time AI predictions for top crypto coins using Binance data." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://crypto-app.ciocan.eu" />
        <meta property="og:image" content="/opengraph-image.png" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://crypto-app.ciocan.eu" />
      </Head>

      <main className="flex flex-col items-center justify-center w-full min-h-screen px-4 pt-4 pb-12 md:pt-8 md:pb-20">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-white text-center mb-10">
          Crypto AI Predictions 24h 💫
        </h1>
        <div className="w-full max-w-6xl px-2 md:px-0">
          <CryptoTable />
        </div>
      </main>
    </>
  )
}
