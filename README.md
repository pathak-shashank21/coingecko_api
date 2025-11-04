#  CoinGecko API Project

A Python-based project to interact with the [CoinGecko API](https://www.coingecko.com/en/api), fetch cryptocurrency data, and perform analysis.


---------------------------------------------------------------------------------------
##  Features
- Connects securely to the CoinGecko API using environment variables
- Fetches live cryptocurrency market data
- Easily extendable for analytics and visualization
- Clean project structure with virtual environment support


--------------------------------------------------------------------------------------
##  Setup Instructions

### 1 Clone the repository
git clone git@github.com:pathak-shashank21/coingecko_api.git
cd coingecko_api

### 2 Create and activate the virtual environment
python3 -m venv crypto
source crypto/bin/activate

### 3 Install dependencies
pip install -r requirements.txt

Create a .env file
cp .env.example .env


Then add your CoinGecko API key inside .env:

COINGECKO_API_KEY=your_api_key_here

### 4 Run the main script
python main.py


Expected output:

 Connection successful: {'gecko_says': '(V3) To the Moon!'}



---------------------------------------------------------------------------------------
Project Structure
coingecko_api/
│
├── crypto/              # Virtual environment (ignored by Git)
├── main.py              # Entry point to test API connection
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore           # Git ignore file
└── README.md            # Project documentation

---------------------------------------------------------------------------------------
Requirements

Python 3.8+
CoinGecko API key (free or Pro)

---------------------------------------------------------------------------------------
Author

Shashank Pathak
pathak.shashank01@gmail.com
GitHub: pathak-shashank21

---------------------------------------------------------------------------------------
License

This project is open-source and available under the MIT License