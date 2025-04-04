# Crypto Dashboard

A modern cryptocurrency dashboard built with Next.js and Flask, featuring real-time price tracking, AI predictions, and wallet integration.

## Features

- Real-time cryptocurrency price tracking
- Price trend indicators
- AI-powered price predictions
- 24-hour volume tracking
- Wallet integration via WalletConnect
- Beautiful and responsive UI

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS
- React Icons

### Backend
- Flask
- Pandas
- Binance API
- Scikit-learn for predictions

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd crypto-app-next
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Environment Setup:
- Copy `.env.example` to `.env`
- Fill in your API keys in `.env`:
  - `BINANCE_API_KEY` - Your Binance API key
  - `BINANCE_API_SECRET` - Your Binance API secret
  - `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` - Your WalletConnect project ID

**Important**: Never commit the `.env` file or share your API keys. The `.env` file is included in `.gitignore` for security.

## Running the Application

### Using Docker (Recommended)

1. Start the application:
```bash
docker-compose up --build
```

2. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

### Manual Start

1. Start the backend:
```bash
cd backend
python main.py
```

2. Start the frontend:
```bash
npm run dev
```

## Development

- Frontend code is in `src/` directory
- Backend code is in `backend/` directory
- Historical data is stored in `crypto_data/` directory

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT
