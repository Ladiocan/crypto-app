import CryptoTable from "../components/CryptoTable";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center w-full min-h-screen px-4 pt-4 pb-12 md:pt-8 md:pb-20">
      <h1 className="text-8xl md:text-5xl font-extrabold tracking-tight text-white text-center mb-10">
        Crypto AI Predictions 24h 💫
      </h1>
      <div className="w-full max-w-6xl px-2 md:px-0">
        <CryptoTable />
      </div>
    </main>
  );
}