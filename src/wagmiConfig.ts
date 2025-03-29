import { createConfig, http } from 'wagmi';
import { mainnet, linea, lineaSepolia } from 'wagmi/chains';
import { injected, metaMask, walletConnect } from 'wagmi/connectors';

export const wagmiConfig = createConfig({
  chains: [mainnet, linea, lineaSepolia],
  connectors: [
    injected(),
    metaMask({
      dappMetadata: {
        name: 'Crypto Futuristic App',
        url: 'https://ciocan.eu',
      },
    }),
    walletConnect({
      projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!,
    }),
  ],
  transports: {
    [mainnet.id]: http(),
    [linea.id]: http(),
    [lineaSepolia.id]: http(),
  },
  ssr: true,
});
console.log("WalletConnect Project ID:", process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID);

