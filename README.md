#PC Price Tracker

A python-based web scraper that tracks Pc part prices from Newegg and stores historical pricing data. 

## Features

- Scrapes product information (title, price, stock status) from Newegg
- Stores price history with timestamps in JSON format
- Tracks price changes over time
- Monitors stock availability
- Error handling for network issues and corrupted data

## Tech Stack

- **Python 3.13**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **JSON** - Data storage

## Installation

1. **Clone the repository**
```bash
   git clone https://github.com/datrell23/pcPriceTracker.git
   cd pcPriceTracker
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows Git Bash
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

The script will:
1. Fetch the product page from Newegg
2. Extract title, price, and stock status
3. Save the data to `price_history.json` with a timestamp
4. Display the results in the terminal

### Automated Price Tracking

Run the automated tracker to check prices at regular intervals:

```bash
python automated_tracker.py
```

By default, it checks every 6 hours. Modify `CHECK_INTERVAL_HOURS` in `automated_tracker.py` to customize.

To stop: Press `Ctrl+C`



## Roadmap

- [x] Automate price checks (scheduled runs)
- [ ] Support multiple products
- [x] Discord bot integration for price alerts
- [ ] Add more retailers (Amazon, Best Buy, Micro Center)
- [ ] Price drop notifications
- [ ] Cloud deployment for 24/7 uptime.

##
- **Retailer bot protection:** Newegg and other large retailers may block automated requests (for example, returning HTTP 403). The scraper cannot guarantee access, and I chose not to work around these protections.
- **Fragile selectors:** The scraper depends on the page's HTML structure (class names like `price-current`). If a retailer redesigns its page, the selectors will need updating.
- **Single product, single site:** Currently tracks one Newegg product. Multi-product and multi-retailer support are on the roadmap.
- **Local storage:** Price history is stored in a local JSON file, which is fine for one product but won't scale to many.
- **Runs only while the bot is running:** The bot and its scheduled scrape need a machine that stays on. Cloud hosting is a planned improvement.

### Failure handling

If a scrape fails (blocked request, network error, timeout), the error is logged and the bot keeps running. It skips that cycle and tries again on the next scheduled run instead of crashing.



## What I Learned

- Web scraping with BeautifulSoup
- HTML parsing and CSS selectors
- JSON file handling and data persistence
- Error handling and edge cases
- Clean code organization with functions
- Git version control best practices

## Contributing

This is a personal learning project, but suggestions are welcome! Feel free to open an issue.

## License

MIT License - feel free to use this code for your own projects!

## Author

Datrell Williams
- GitHub: [Datrell23](https://github.com/datrell23)
- Working toward: Backend Developer role at a big tech company
