# Architecture Overview

## System Architecture Philosophy

The Anti-India Campaign Detection System is built on a **modular, layered architecture** that prioritizes scalability, maintainability, and security. The design follows enterprise software development principles while maintaining the flexibility needed for intelligence operations.

## High-Level Architecture

```mermaid
graph TB
    subgraph "External Interfaces"
        TG[Telegram Platform]
        USERS[Analysts & Operators]
        API_CLIENTS[External API Clients]
    end
    
    subgraph "Presentation Layer"
        DASH[Streamlit Dashboard]
        API[FastAPI REST API]
        ALERTS[Alert System]
    end
    
    subgraph "Application Layer"
        AUTH[Authentication Service]
        SCHED[Task Scheduler]
        WORKFLOW[Workflow Engine]
    end
    
    subgraph "Business Logic Layer"
        NLP[NLP Engine]
        ANALYSIS[Analysis Engine]
        INTEL[Intelligence Processor]
        SCORING[Threat Scoring]
    end
    
    subgraph "Data Access Layer"
        COLLECTOR[Data Collectors]
        PROCESSOR[Message Processor]
        AGGREGATOR[Data Aggregator]
    end
    
    subgraph "Data Layer"
        CACHE[(Redis Cache)]
        DB[(SQLite Database)]
        FILES[(File Storage)]
        QUEUE[(Message Queue)]
    end
    
    subgraph "Infrastructure Layer"
        MONITOR[System Monitoring]
        LOG[Logging Service]
        SECURITY[Security Framework]
    end
    
    %% Connections
    TG --> COLLECTOR
    USERS --> DASH
    API_CLIENTS --> API
    
    DASH --> AUTH
    API --> AUTH
    ALERTS --> AUTH
    
    AUTH --> WORKFLOW
    SCHED --> WORKFLOW
    
    WORKFLOW --> NLP
    WORKFLOW --> ANALYSIS
    WORKFLOW --> INTEL
    WORKFLOW --> SCORING
    
    NLP --> PROCESSOR
    ANALYSIS --> PROCESSOR
    INTEL --> AGGREGATOR
    SCORING --> AGGREGATOR
    
    COLLECTOR --> QUEUE
    PROCESSOR --> DB
    AGGREGATOR --> CACHE
    
    MONITOR --> LOG
    SECURITY --> LOG
```

## Architectural Layers

### 1. Data Collection Layer

The foundation layer responsible for gathering intelligence from multiple sources:

```mermaid
graph LR
    subgraph "Collection Sources"
        SIGINT[SIGINT Scanner]
        HUMINT[HUMINT Tipline]
        HONEYPOT[Honeypot Client]
    end
    
    subgraph "Collection Infrastructure"
        TELETHON[Telethon Clients]
        BOTAPI[Telegram Bot API]
        SCHEDULER[Collection Scheduler]
    end
    
    subgraph "Data Pipeline"
        VALIDATOR[Data Validator]
        NORMALIZER[Data Normalizer]
        ENRICHER[Metadata Enricher]
    end
    
    SIGINT --> TELETHON
    HUMINT --> BOTAPI
    HONEYPOT --> TELETHON
    
    TELETHON --> VALIDATOR
    BOTAPI --> VALIDATOR
    
    VALIDATOR --> NORMALIZER
    NORMALIZER --> ENRICHER
    
    SCHEDULER --> SIGINT
    SCHEDULER --> HONEYPOT
```

#### Components:
- **Public Scanner**: Automated monitoring of public Telegram channels
- **Tipline Bot**: Interface for crowdsourced intelligence reporting
- **Honeypot Client**: Covert intelligence gathering from private groups
- **Data Validation**: Ensures data quality and consistency
- **Metadata Enrichment**: Adds contextual information to collected data

### 2. Processing and Analysis Layer

The core intelligence engine that transforms raw data into actionable insights:

```mermaid
graph TD
    INPUT[Raw Messages] --> PIPELINE{Processing Pipeline}
    
    PIPELINE --> KEYWORD[Keyword Matcher]
    PIPELINE --> SENTIMENT[Sentiment Analyzer] 
    PIPELINE --> ENGAGEMENT[Engagement Tracker]
    PIPELINE --> NETWORK[Network Analyzer]
    
    KEYWORD --> SCORER[Threat Scorer]
    SENTIMENT --> SCORER
    ENGAGEMENT --> SCORER
    NETWORK --> SCORER
    
    SCORER --> CLASSIFIER[Threat Classifier]
    CLASSIFIER --> OUTPUT[Classified Intelligence]
    
    subgraph "NLP Components"
        TOKENIZER[Text Tokenizer]
        LEMMATIZER[Lemmatizer]
        VADER[VADER Sentiment]
        SPACY[spaCy NER]
    end
    
    SENTIMENT --> TOKENIZER
    TOKENIZER --> LEMMATIZER
    LEMMATIZER --> VADER
    SENTIMENT --> SPACY
```

#### Core Processing Components:

1. **Keyword Detection Engine**
   - Dynamic keyword matching against threat database
   - Multi-language support with translation capabilities
   - Regular expression pattern matching for complex terms
   - Contextual keyword analysis to reduce false positives

2. **Natural Language Processing Suite**
   - **Sentiment Analysis**: VADER-based emotional tone classification
   - **Named Entity Recognition**: Identification of persons, locations, organizations
   - **Language Detection**: Automatic language identification and processing
   - **Text Classification**: Automated categorization of message content

3. **Engagement Analysis Engine**
   - Forward tracking and viral spread detection
   - Influence scoring based on message reach and interaction
   - Temporal analysis of message velocity and momentum
   - Cross-channel correlation and amplification detection

### 3. Storage and Data Management Layer

Efficient and secure data management infrastructure:

```mermaid
graph LR
    subgraph "Storage Systems"
        CACHE[(Redis Cache)]
        PRIMARY[(SQLite Primary DB)]
        BACKUP[(Backup Storage)]
        FILES[(File System)]
    end
    
    subgraph "Data Management"
        ORM[SQLAlchemy ORM]
        MIGRATION[Schema Migration]
        BACKUP_MGR[Backup Manager]
    end
    
    subgraph "Data Access Patterns"
        READ[Read Operations]
        WRITE[Write Operations]
        SEARCH[Search Operations]
    end
    
    ORM --> PRIMARY
    MIGRATION --> PRIMARY
    BACKUP_MGR --> BACKUP
    
    READ --> CACHE
    CACHE --> PRIMARY
    WRITE --> PRIMARY
    SEARCH --> PRIMARY
```

#### Storage Architecture:
- **Primary Database**: SQLite for structured data storage
- **Cache Layer**: Redis for high-performance data access
- **File Storage**: Organized file system for documents and media
- **Backup System**: Automated backup and recovery mechanisms

### 4. Presentation and Interface Layer

User-facing components and external integrations:

```mermaid
graph TB
    subgraph "User Interfaces"
        DASHBOARD[Streamlit Dashboard]
        MOBILE[Mobile Interface]
        CLI[Command Line Tools]
    end
    
    subgraph "API Layer"
        REST[REST API]
        WEBHOOK[Webhook Endpoints]
        GRAPHQL[GraphQL API]
    end
    
    subgraph "Integration Points"
        SSO[Single Sign-On]
        EXTERNAL[External Systems]
        NOTIFICATIONS[Notification Services]
    end
    
    DASHBOARD --> REST
    MOBILE --> REST
    CLI --> REST
    
    REST --> SSO
    WEBHOOK --> EXTERNAL
    NOTIFICATIONS --> EXTERNAL
```

## Security Architecture

### Multi-Layer Security Model

```mermaid
graph TB
    subgraph "Perimeter Security"
        FIREWALL[Network Firewall]
        PROXY[Reverse Proxy]
        RATE_LIMIT[Rate Limiting]
    end
    
    subgraph "Application Security"
        AUTH[Authentication]
        AUTHZ[Authorization]
        SESSION[Session Management]
    end
    
    subgraph "Data Security"
        ENCRYPT[Data Encryption]
        HASH[Password Hashing]
        SANITIZE[Input Sanitization]
    end
    
    subgraph "Operational Security"
        AUDIT[Audit Logging]
        MONITOR[Security Monitoring]
        INCIDENT[Incident Response]
    end
    
    FIREWALL --> AUTH
    PROXY --> AUTH
    RATE_LIMIT --> AUTH
    
    AUTH --> ENCRYPT
    AUTHZ --> ENCRYPT
    SESSION --> ENCRYPT
    
    ENCRYPT --> AUDIT
    HASH --> AUDIT
    SANITIZE --> AUDIT
    
    AUDIT --> MONITOR
    MONITOR --> INCIDENT
```

### Security Components:
- **Authentication**: Multi-factor authentication with SSO integration
- **Authorization**: Role-based access control (RBAC) with fine-grained permissions
- **Data Protection**: End-to-end encryption for sensitive intelligence data
- **Audit Trail**: Comprehensive logging of all system activities
- **Operational Security**: Secure handling of HUMINT assets and sensitive operations

## Scalability and Performance

### Horizontal Scaling Strategy

```mermaid
graph LR
    subgraph "Load Distribution"
        LB[Load Balancer]
        API1[API Instance 1]
        API2[API Instance 2]
        API3[API Instance N]
    end
    
    subgraph "Processing Scale"
        QUEUE[Message Queue]
        WORKER1[Worker 1]
        WORKER2[Worker 2]
        WORKER3[Worker N]
    end
    
    subgraph "Data Scale"
        CACHE_CLUSTER[Redis Cluster]
        DB_SHARD[Database Sharding]
        CDN[Content Delivery]
    end
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    QUEUE --> WORKER1
    QUEUE --> WORKER2
    QUEUE --> WORKER3
    
    API1 --> CACHE_CLUSTER
    WORKER1 --> DB_SHARD
```

### Performance Optimizations:
- **Asynchronous Processing**: Non-blocking I/O for high-throughput data collection
- **Message Queuing**: Celery-based distributed task processing
- **Caching Strategy**: Multi-tier caching for frequently accessed data
- **Database Optimization**: Indexed queries and connection pooling

## Deployment Architecture

### Container-Based Deployment

```mermaid
graph TB
    subgraph "Container Orchestration"
        K8S[Kubernetes Cluster]
        INGRESS[Ingress Controller]
        SERVICE[Service Mesh]
    end
    
    subgraph "Application Containers"
        API_POD[API Pods]
        WORKER_POD[Worker Pods]
        DASHBOARD_POD[Dashboard Pods]
    end
    
    subgraph "Data Containers"
        DB_POD[Database Pod]
        CACHE_POD[Cache Pod]
        QUEUE_POD[Queue Pod]
    end
    
    subgraph "Supporting Services"
        MONITOR_POD[Monitoring]
        LOG_POD[Logging]
        BACKUP_POD[Backup]
    end
    
    K8S --> API_POD
    K8S --> WORKER_POD
    K8S --> DASHBOARD_POD
    
    INGRESS --> API_POD
    SERVICE --> DASHBOARD_POD
    
    API_POD --> DB_POD
    WORKER_POD --> CACHE_POD
    API_POD --> QUEUE_POD
```

### Infrastructure Components:
- **Containerization**: Docker containers for consistent deployment
- **Orchestration**: Kubernetes for automated scaling and management
- **Service Discovery**: Automatic service registration and discovery
- **Health Monitoring**: Comprehensive system health checks and alerting

This architecture ensures the system can handle the demanding requirements of real-time intelligence processing while maintaining security, reliability, and scalability for mission-critical operations.
