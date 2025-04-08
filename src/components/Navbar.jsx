"use client";
import { useAccount, useConnect, useDisconnect } from "wagmi";
import { metaMask, walletConnect, injected } from "wagmi/connectors";
import CryptoLogo from "./CryptoLogo";

export function Navbar() {
  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();

  return (
    <nav className="flex flex-col md:flex-row items-center justify-between px-4 py-4 md:px-6 md:py-6 shadow-md backdrop-blur-md bg-black/10 text-white rounded-b-lg gap-4">
      <CryptoLogo className="w-32 md:w-auto" />
      <div className="flex flex-wrap justify-center gap-3 md:gap-6">
        {isConnected ? (
          <div className="flex items-center gap-4">
            <span className="text-sm">Connected: {address.slice(0, 6)}...{address.slice(-4)}</span>
            <button onClick={() => disconnect()} className="bg-red-600 px-6 py-2 rounded-md hover:bg-red-700">Disconnect</button>
          </div>
        ) : (
          <div className="flex gap-4">
            {connectors.map((connector) => (
              <button
                key={connector.uid}
                onClick={() => connect({ connector })}
                className="px-4 py-2 rounded-md bg-white/10 text-white border border-white/20 backdrop-blur-sm shadow-md hover:bg-white/20 transition"
              >
                {connector.name}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}