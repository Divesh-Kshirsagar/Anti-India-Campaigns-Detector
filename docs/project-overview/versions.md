# Project Versions

## Overview
This document outlines the simplified phased development for the Anti-India Campaign Detector prototype. The project is designed for research, focusing on data collection and queue-based automation, with SQLite as the core for queue and storage. No Redis, no cloud, no unnecessary complexity. Data processing (NLP, analysis) is not included in the initial prototype.

## Version 1.0 - Twitter Automation (Playwright)
**Objective**: Implement Twitter data collection using Playwright for browser automation. Use Twitter API as a fallback if available.

### Features
- Twitter data retrieval via Playwright (browser automation)
- Twitter API fallback for data retrieval
- Simple configuration (YAML/INI)
- Data queueing in SQLite
- Data export (CSV/JSON)

### Requirements
```bash
pip install playwright
pip install pandas
pip install requests
pip install python-dotenv
pip install configparser
pip install sqlite3
```

### Deliverables
- Twitter Playwright collector
- Twitter API fallback client
- SQLite queue for raw data
- Data export utilities

---

## Version 2.0 - Telegram Automation (Basic)
**Objective**: Implement basic Telegram data collection without tipline and honeypot features.

### Features
- Telegram Bot API integration
- Channel and group monitoring
- Message collection and queueing in SQLite
- Data export (CSV/JSON)

### Requirements
```bash
pip install python-telegram-bot
pip install asyncio
pip install aiohttp
pip install sqlite3
```

### Deliverables
- Telegram bot implementation
- Channel monitoring system
- SQLite queue for Telegram messages
- Data export utilities

---

## Version 3.0 - Telegram Tipline Integration
**Objective**: Add tipline functionality to Telegram bot for receiving user reports.

### Features
- Tipline bot commands for user reports
- Report queueing and storage in SQLite
- Simple admin interface for report management

### Requirements
```bash
pip install sqlite3
pip install datetime
pip install logging
```

### Deliverables
- Tipline bot functionality
- Report management system
- SQLite database for reports

---

## Version 4.0 - Telegram Honeypot Implementation
**Objective**: Implement honeypot functionality to attract and monitor suspicious activities.

### Features
- Honeypot channel/group creation
- Automated content posting
- Activity monitoring and logging
- Suspicious behavior detection (basic)

### Requirements
```bash
pip install schedule
pip install random
pip install time
pip install sqlite3
```

### Deliverables
- Honeypot implementation
- Activity monitoring system
- SQLite database for honeypot logs

---

## Version 5.0 - Data Processing and NLP Features
**Objective**: Implement data processing layer with NLP capabilities for sentiment analysis and basic text analysis.

### Features
- Data processing pipeline for collected messages
- Sentiment analysis using VADER and TextBlob
- Basic NLP preprocessing (tokenization, cleaning)
- Language detection for multilingual content
- Keyword extraction and frequency analysis
- Enhanced data visualization with sentiment metrics
- Processing queue management in SQLite

### Requirements
```bash
pip install nltk
pip install textblob
pip install vaderSentiment
pip install langdetect
pip install wordcloud
pip install seaborn
pip install scikit-learn
```

### Deliverables
- NLP processing pipeline
- Sentiment analysis engine
- Language detection module
- Enhanced data visualization with sentiment charts
- Processing queue for NLP tasks
- Updated tkinter GUI with NLP features

---

## Core Dependencies (All Versions)
```bash
pip install pandas
pip install sqlite3
pip install configparser
pip install logging
```

## Development Guidelines
1. **Data Collection Focus**: Only raw data collection and queueing in SQLite
2. **Simple UI**: Minimal or CLI-based interface for prototype
3. **Modular Design**: Each platform integration is modular and can be enabled/disabled
4. **Configuration Management**: All API keys and settings managed through config files
5. **Data Export**: Consistent data export formats across all platforms
6. **Error Handling**: Robust error handling and logging throughout all modules

## Notes
- No Redis, cloud, FastAPI, or Streamlit dependencies
- No NLP or analysis in prototype (future work)
- Focus on reliable data collection and SQLite-based queue/storage
- Each version builds upon the previous version's functionality