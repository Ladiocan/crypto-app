import CryptoTable from "../components/CryptoTable";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center w-full min-h-screen space-y-8">
      <h1 className="text-5xl font-extrabold tracking-tight text-white">Hello Crypto World 💫</h1>
      <CryptoTable />
    </main>
  );
}
