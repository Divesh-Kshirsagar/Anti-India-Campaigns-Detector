# Development Setup Guide

## Prerequisites and Environment Setup

This guide provides step-by-step instructions for setting up a complete development environment for the Anti-India Campaign Detection System.

## System Requirements

### Hardware Requirements

**Minimum Requirements**:
- **CPU**: 4 cores, 2.5GHz+ (Intel i5 or AMD Ryzen 5 equivalent)
- **RAM**: 8GB DDR4
- **Storage**: 100GB available space (SSD recommended)
- **Network**: Broadband internet connection (>10 Mbps)

**Recommended Requirements**:
- **CPU**: 8 cores, 3.0GHz+ (Intel i7 or AMD Ryzen 7 equivalent)
- **RAM**: 16GB+ DDR4
- **Storage**: 500GB+ NVMe SSD
- **GPU**: NVIDIA GPU with 4GB+ VRAM (for advanced NLP models)
- **Network**: High-speed internet (>50 Mbps)

### Operating System Support

| OS | Version | Status | Notes |
|----|---------|--------|-------|
| **Ubuntu** | 20.04 LTS+ | ✅ Primary | Recommended for production |
| **Windows** | 10/11 | ✅ Supported | WSL2 recommended |
| **macOS** | 12.0+ | ✅ Supported | Intel and Apple Silicon |
| **CentOS/RHEL** | 8+ | ✅ Supported | Enterprise environments |

## Development Environment Setup

### 1. Python Environment

#### Install Python 3.9+

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv python3.11-dev

# macOS (using Homebrew)
brew install python@3.11

# Windows (using chocolatey)
choco install python311
```

#### Create Virtual Environment

```bash
# Create project directory
mkdir anti-india-campaign-detector
cd anti-india-campaign-detector

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate

# Windows
.\venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### 2. Project Setup

#### Clone Repository

```bash
# Clone the repository
git clone https://github.com/security-intel/anti-india-campaign-detector.git
cd anti-india-campaign-detector

# Install development dependencies
pip install -e ".[dev,docs,testing]"
```

#### Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration file
nano .env
```

**Environment Variables Configuration**:

```bash
# .env file
# =============================================================================
# Telegram API Configuration
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Database Configuration
DATABASE_URL=sqlite:///./data/aicd.db
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
ENCRYPTION_KEY=your-encryption-key-here

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_FILE=logs/aicd.log

# NLP Configuration
SPACY_MODEL=en_core_web_sm
NLTK_DATA_PATH=./nltk_data

# Development Configuration
DEBUG=true
ENVIRONMENT=development
```

### 3. Database Setup

#### Install and Configure SQLite

```bash
# Ubuntu/Debian
sudo apt install sqlite3 libsqlite3-dev

# macOS
brew install sqlite

# Create data directory
mkdir -p data logs

# Initialize database
python -c "
from src.anti_india_campaign_detector.database import init_db
init_db()
print('Database initialized successfully')
"
```

#### Install and Configure Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Start Redis service
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew services start redis

# Test Redis connection
redis-cli ping
```

### 4. External Service Setup

#### Telegram API Setup

1. **Create Telegram Application**:
   - Visit [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application
   - Note down `api_id` and `api_hash`

2. **Create Bot Account**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command
   - Follow instructions to create bot
   - Note down the bot token

3. **Configure API Keys**:
```bash
# Update .env file with your credentials
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 5. NLP Models Setup

#### Install Required NLP Libraries

```bash
# Install spaCy and download models
pip install spacy
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg

# Install NLTK and download data
python -c "
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
print('NLTK data downloaded successfully')
"

# Install additional ML libraries
pip install transformers torch torchvision
```

### 6. Development Tools Setup

#### Code Quality Tools

```bash
# Install pre-commit hooks
pre-commit install

# Run initial code formatting
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# Run type checking
mypy src/
```

#### Testing Framework

```bash
# Run test suite
pytest tests/ -v --cov=src/

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v

# Generate coverage report
pytest --cov=src/ --cov-report=html tests/
```

## IDE and Editor Configuration

### Visual Studio Code Setup

#### Required Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.test-adapter-converter",
    "ms-vscode.extension-test-runner",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-json",
    "ms-toolsai.jupyter",
    "bierner.markdown-mermaid",
    "davidanson.vscode-markdownlint"
  ]
}
```

#### VS Code Settings

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### PyCharm Configuration

#### Project Settings

1. **Interpreter Configuration**:
   - File → Settings → Project → Python Interpreter
   - Add interpreter → Existing environment
   - Select `./venv/bin/python`

2. **Code Style Setup**:
   - File → Settings → Editor → Code Style → Python
   - Import settings from `pyproject.toml`

3. **Run Configurations**:
```python
# Dashboard
Name: Dashboard
Script path: src/anti_india_campaign_detector/dashboard.py
Parameters: --debug --port 8501
Working directory: $PROJECT_DIR$

# API Server
Name: API Server  
Script path: src/anti_india_campaign_detector/api.py
Parameters: --host 0.0.0.0 --port 8000 --reload
Working directory: $PROJECT_DIR$

# Scanner
Name: Scanner
Script path: src/anti_india_campaign_detector/scanner.py
Parameters: --config config/scanner.yaml
Working directory: $PROJECT_DIR$
```

## Docker Development Environment

### Docker Setup

#### Dockerfile for Development

```dockerfile
# Dockerfile.dev
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    sqlite3 \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy source code
COPY . .

# Install package in development mode
RUN pip install -e ".[dev,docs,testing]"

# Expose ports
EXPOSE 8000 8501 6379

# Default command
CMD ["bash"]
```

#### Docker Compose for Development

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - ./data:/app/data
      - ./logs:/app/logs
    ports:
      - "8000:8000"  # API
      - "8501:8501"  # Dashboard
    environment:
      - DATABASE_URL=sqlite:///./data/aicd.db
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
      - DEBUG=true
    depends_on:
      - redis
      - postgres
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: aicd
      POSTGRES_USER: aicd_user  
      POSTGRES_PASSWORD: aicd_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

#### Start Development Environment

```bash
# Build and start services
docker-compose -f docker-compose.dev.yml up --build

# Run in detached mode
docker-compose -f docker-compose.dev.yml up -d

# Access development container
docker-compose -f docker-compose.dev.yml exec app bash

# Stop services
docker-compose -f docker-compose.dev.yml down
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Telegram API Connection Issues

**Problem**: `ConnectionError: Cannot connect to Telegram servers`

**Solutions**:
```bash
# Check network connectivity
ping api.telegram.org

# Verify API credentials
python -c "
from telethon import TelegramClient
client = TelegramClient('test', API_ID, API_HASH)
print('Credentials valid:', client.is_connected())
"

# Check firewall settings
sudo ufw status
```

#### 2. Database Connection Problems

**Problem**: `sqlite3.OperationalError: unable to open database file`

**Solutions**:
```bash
# Check file permissions
ls -la data/
chmod 755 data/
chmod 644 data/aicd.db

# Create database directory if missing
mkdir -p data
python -c "from src.database import init_db; init_db()"
```

#### 3. NLP Model Loading Issues

**Problem**: `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solutions**:
```bash
# Download spaCy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully')"
```

#### 4. Memory Issues with Large Datasets

**Problem**: `MemoryError: Unable to allocate array`

**Solutions**:
```bash
# Increase virtual memory
sudo sysctl vm.overcommit_memory=1

# Use batch processing
export BATCH_SIZE=100
export MAX_WORKERS=2

# Monitor memory usage
htop
```

### Performance Optimization

#### Database Optimization

```sql
-- Create indexes for better query performance
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_messages_channel_id ON messages(channel_id);
CREATE INDEX idx_messages_threat_score ON messages(threat_score);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Analyze query performance
EXPLAIN QUERY PLAN SELECT * FROM messages WHERE threat_score > 0.7;
```

#### Redis Configuration

```bash
# Optimize Redis for development
echo "maxmemory 512mb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf

# Monitor Redis performance
redis-cli info memory
redis-cli monitor
```

## Next Steps

After completing the setup:

1. **Run Initial Tests**:
```bash
# Verify installation
pytest tests/test_setup.py -v

# Run smoke tests
python -c "from src.anti_india_campaign_detector import __version__; print(f'Version: {__version__}')"
```

2. **Start Desktop Application**:
```bash
# Run the main tkinter application
python src/anti_india_campaign_detector/main.py

# Or run with configuration file
python src/anti_india_campaign_detector/main.py --config config/settings.ini
```

3. **Application Features**:
   - **Main GUI**: Desktop interface with tabbed platform modules
   - **Dashboard**: http://localhost:8501
   - **Redis CLI**: `redis-cli`
   - **Database**: `sqlite3 data/aicd.db`

Your development environment is now ready for contributing to the Anti-India Campaign Detection System!
