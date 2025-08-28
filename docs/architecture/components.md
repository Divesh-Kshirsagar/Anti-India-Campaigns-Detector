# System Components

## Component Architecture Overview

The Anti-India Campaign Detection System is composed of interconnected modules that work together to provide comprehensive threat detection and analysis capabilities. Each component is designed for modularity, testability, and independent scaling.

```mermaid
graph TB
    subgraph "Data Collection Components"
        SC[Scanner Client]
        IC[Instagram Client]
        TC[Twitter Client]
        TL[Tipline Bot]  
        HP[Cross-Platform Honeypot]
        DV[Data Validator]
    end
    
    subgraph "Processing Components"
        KM[Keyword Matcher]
        SA[Sentiment Analyzer]
        EA[Engagement Analyzer]
        NA[Network Analyzer]
    end
    
    subgraph "Intelligence Components"
        TS[Threat Scorer]
        TC[Threat Classifier]
        IG[Intelligence Generator]
        AR[Alert Router]
    end
    
    subgraph "Storage Components"
        DM[Data Manager]
        CM[Cache Manager]
        FM[File Manager]
        BM[Backup Manager]
    end
    
    subgraph "Interface Components"
        DB[Dashboard]
        API[API Gateway]
        WH[Webhook Handler]
        CLI[CLI Tools]
    end
    
    subgraph "Infrastructure Components"
        AS[Auth Service]
        LS[Logging Service]
        MS[Monitoring Service]
        NS[Notification Service]
    end
    
    %% Data Flow
    SC --> DV
    IC --> DV
    TC --> DV
    TL --> DV
    HP --> DV
    DV --> KM
    KM --> SA
    SA --> EA
    EA --> NA
    NA --> TS
    TS --> TC
    TC --> IG
    IG --> AR
    AR --> NS
    
    %% Storage Flow
    DV --> DM
    IG --> DM
    DM --> CM
    DM --> FM
    DM --> BM
    
    %% Interface Flow
    DB --> API
    WH --> API
    CLI --> API
    API --> AS
    
    %% Infrastructure Flow
    AS --> LS
    MS --> LS
    NS --> LS
```

## Data Collection Components

### Scanner Client (SIGINT)

**Purpose**: Automated monitoring and data collection from public Telegram channels.

```mermaid
classDiagram
    class ScannerClient {
        -telethon_client: TelegramClient
        -channel_list: List[str]
        -collection_config: Config
        +start_monitoring()
        +stop_monitoring()
        +add_channel(channel_id)
        +remove_channel(channel_id)
        +get_channel_history(channel_id, limit)
        -process_message(message)
        -handle_connection_error()
    }
    
    class ChannelMonitor {
        -channel_id: str
        -last_message_id: int
        -monitoring_active: bool
        +collect_new_messages()
        +update_last_position()
        +get_channel_info()
    }
    
    class MessageHandler {
        +validate_message(message)
        +extract_metadata(message)
        +normalize_content(message)
        +enqueue_for_processing(message)
    }
    
    ScannerClient --> ChannelMonitor
    ScannerClient --> MessageHandler
```

**Key Features**:
- **Concurrent Channel Monitoring**: Simultaneous monitoring of multiple channels
- **Rate Limit Management**: Intelligent API rate limiting to avoid restrictions
- **Connection Recovery**: Automatic reconnection and error recovery
- **Message Deduplication**: Prevention of duplicate message processing
- **Metadata Extraction**: Complete message metadata capture

**Configuration Example**:
```yaml
scanner:
  channels:
    - "@channel1"
    - "@channel2"
  rate_limit:
    requests_per_second: 10
    burst_limit: 20
  retry_policy:
    max_retries: 3
    backoff_multiplier: 2
```

### Tipline Bot (HUMINT)

**Purpose**: Crowdsourced intelligence collection through user submissions.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> ReceiveTip: User sends message
    ReceiveTip --> ValidatingTip: Parse submission
    ValidatingTip --> ProcessingTip: Validation passed
    ValidatingTip --> RequestingClarification: Validation failed
    RequestingClarification --> ReceiveTip: User provides clarification
    ProcessingTip --> StoringTip: Processing complete
    StoringTip --> SendingConfirmation: Storage complete
    SendingConfirmation --> Idle: Confirmation sent
    
    note right of ValidatingTip: Check format, content, authenticity
    note right of ProcessingTip: Enrich with metadata, categorize
    note right of StoringTip: Store in intelligence database
```

**Key Features**:
- **Anonymous Submissions**: Secure, anonymous tip submission system
- **Content Validation**: Automated validation of submitted intelligence
- **Multi-format Support**: Text, images, URLs, and document submissions
- **Feedback Loop**: Confirmation and follow-up with submitters
- **Priority Classification**: Automatic prioritization of high-value tips

### Honeypot Client (Advanced HUMINT)

**Purpose**: Covert intelligence collection from private groups and channels.

```mermaid
sequenceDiagram
    participant HC as Honeypot Client
    participant TG as Telegram
    participant PG as Private Group
    participant DB as Database
    
    HC->>TG: Authenticate as persona
    HC->>PG: Request to join group
    PG->>HC: Accept/Reject invitation
    
    loop Monitoring Phase
        PG->>HC: New messages
        HC->>HC: Filter for intelligence value
        HC->>DB: Store high-value intelligence
        HC->>HC: Maintain operational security
    end
    
    Note over HC: Periodic persona maintenance
    HC->>PG: Post credible content
    HC->>PG: Engage in discussions
```

**Operational Security Features**:
- **Persona Management**: Maintains credible cover identities
- **Behavioral Patterns**: Human-like interaction patterns
- **Content Filtering**: Selective intelligence extraction
- **Operational Security**: Maintains cover and avoids detection
- **Evidence Chain**: Maintains evidence integrity for legal proceedings

### Instagram Client (Visual SIGINT)

**Purpose**: Automated Instagram monitoring and intelligence collection using real account automation.

```mermaid
classDiagram
    class InstagramClient {
        -instagrapi_client: Client
        -selenium_driver: WebDriver
        -account_pool: List[Account]
        -proxy_manager: ProxyManager
        +monitor_stories(targets: List[str])
        +track_posts(hashtags: List[str])
        +automated_engagement(strategy: EngagementStrategy)
        +extract_story_content(story_id: str)
        +analyze_user_network(username: str)
        -rotate_account()
        -handle_challenges()
        -maintain_human_behavior()
    }
    
    class AccountManager {
        -active_accounts: Dict[str, Account]
        -rotation_schedule: Dict[str, datetime]
        +get_available_account(): Account
        +mark_account_active(account_id: str)
        +handle_account_restriction(account_id: str)
        +validate_account_health(account_id: str)
    }
    
    class StoryIntelligence {
        +capture_expiring_content(user_id: str)
        +perform_ocr_analysis(image_url: str)
        +extract_story_metadata(story: Story)
        +track_story_viewers(story_id: str)
    }
    
    class EngagementBot {
        +strategic_likes(posts: List[Post])
        +follow_target_accounts(usernames: List[str])
        +comment_intelligence(post_id: str)
        +direct_message_campaigns(targets: List[str])
    }
    
    InstagramClient --> AccountManager
    InstagramClient --> StoryIntelligence
    InstagramClient --> EngagementBot
```

**Advanced Capabilities**:
- **Story Archiving**: 24-hour window story capture and analysis
- **Private Account Infiltration**: Automated follow request campaigns
- **Visual Content Analysis**: OCR and image recognition for threat detection
- **Engagement Intelligence**: Strategic interaction to maintain account credibility
- **Network Mapping**: Follower/following relationship analysis for influence tracking

**Anti-Detection Measures**:
```python
class InstagramSafetyProtocol:
    def human_like_behavior(self):
        """Implement human-like interaction patterns"""
        delay_range = random.uniform(2, 8)  # Random delays between actions
        scroll_patterns = self.random_scroll()  # Realistic scrolling behavior
        interaction_variety = self.mixed_actions()  # Varied action sequences
        
    def account_health_monitoring(self):
        """Monitor account status for restrictions"""
        challenge_detection = self.check_challenges()
        rate_limit_tracking = self.monitor_api_limits()
        engagement_rate_analysis = self.track_success_rates()
```

### Twitter Client (Real-time SIGINT)

**Purpose**: Comprehensive Twitter monitoring and automated intelligence operations.

```mermaid
classDiagram
    class TwitterClient {
        -tweepy_client: tweepy.Client
        -selenium_driver: WebDriver
        -stream_handler: StreamHandler
        -account_pool: List[TwitterAccount]
        +monitor_realtime_stream(keywords: List[str])
        +track_user_timelines(usernames: List[str])
        +analyze_hashtag_campaigns(hashtags: List[str])
        +extract_thread_conversations(tweet_id: str)
        +monitor_twitter_spaces(space_ids: List[str])
        -handle_rate_limits()
        -switch_to_selenium_backup()
    }
    
    class StreamMonitor {
        -filtered_stream: tweepy.StreamRule
        +setup_keyword_filters(keywords: List[str])
        +process_realtime_tweets(tweet: Tweet)
        +detect_viral_content(engagement_metrics: Dict)
        +identify_bot_networks(user_patterns: List[User])
    }
    
    class ThreadAnalyzer {
        +extract_conversation_tree(root_tweet_id: str)
        +map_user_interactions(thread: List[Tweet])
        +detect_coordinated_responses(thread: List[Tweet])
        +analyze_sentiment_flow(conversation: List[Tweet])
    }
    
    class AutomationEngine {
        +strategic_retweets(tweets: List[Tweet])
        +targeted_following(accounts: List[str])
        +dm_intelligence_campaigns(targets: List[str])
        +list_management(categories: Dict[str, List[str]])
    }
    
    TwitterClient --> StreamMonitor
    TwitterClient --> ThreadAnalyzer
    TwitterClient --> AutomationEngine
```

**Real-time Intelligence Features**:
- **Filtered Stream Processing**: Live tweet capture with advanced filtering
- **Viral Content Detection**: Early identification of trending anti-India content
- **Coordinated Behavior Analysis**: Detection of bot networks and information operations
- **Space Intelligence**: Twitter Spaces monitoring with audio transcription
- **Thread Reconstruction**: Complete conversation thread analysis

**Backup Systems**:
```python
class TwitterFailoverSystem:
    def api_to_selenium_fallback(self):
        """Seamless fallback to web scraping when API limits hit"""
        if self.api_rate_limited():
            self.selenium_driver = self.create_stealth_browser()
            self.continue_monitoring_via_web()
            
    def multi_account_rotation(self):
        """Rotate between multiple Twitter accounts"""
        current_account = self.get_next_available_account()
        self.switch_authentication(current_account)
        self.continue_operations()
```

**Cross-Platform Correlation Engine**:
```mermaid
graph TB
    subgraph "Data Sources"
        TG[Telegram Messages]
        IG[Instagram Content]
        TW[Twitter Posts]
    end
    
    TG --> CORRELATION[Cross-Platform Correlator]
    IG --> CORRELATION
    TW --> CORRELATION
    
    CORRELATION --> TIMELINE[Timeline Analysis]
    CORRELATION --> CONTENT[Content Similarity]
    CORRELATION --> ACCOUNT[Account Linking]
    CORRELATION --> PATTERN[Pattern Recognition]
    
    TIMELINE --> UNIFIED_INTEL[Unified Intelligence Report]
    CONTENT --> UNIFIED_INTEL
    ACCOUNT --> UNIFIED_INTEL
    PATTERN --> UNIFIED_INTEL
```

**Multi-Platform Intelligence Fusion**:
- **Account Cross-Referencing**: Linking accounts across Telegram, Instagram, and Twitter
- **Campaign Timeline Reconstruction**: Coordinated narrative tracking across platforms
- **Content Propagation Analysis**: Following information flow between platforms
- **Influence Network Mapping**: Cross-platform relationship analysis
- **Attribution and Source Identification**: Identifying campaign originators

## Processing Components

### Keyword Matcher

**Purpose**: Initial content filtering based on threat-related keywords and phrases.

```mermaid
graph LR
    subgraph "Keyword Database"
        KB[(Keywords DB)]
        PATTERNS[Regex Patterns]
        CONTEXT[Context Rules]
    end
    
    subgraph "Matching Engine"
        TOKENIZER[Text Tokenizer]
        MATCHER[Pattern Matcher]
        SCORER[Match Scorer]
    end
    
    subgraph "Output"
        FLAGGED[Flagged Messages]
        SCORE[Relevance Score]
        METADATA[Match Metadata]
    end
    
    KB --> MATCHER
    PATTERNS --> MATCHER
    CONTEXT --> SCORER
    
    TOKENIZER --> MATCHER
    MATCHER --> SCORER
    SCORER --> FLAGGED
    SCORER --> SCORE
    SCORER --> METADATA
```

**Keyword Categories**:
- **Geographic Terms**: India-specific locations and regions
- **Political Keywords**: Government, policy, and political terms
- **Religious/Cultural**: Terms related to religious and cultural tensions
- **Violence Indicators**: Terms suggesting potential violence or unrest
- **Propaganda Markers**: Common propaganda and disinformation indicators

### Sentiment Analyzer

**Purpose**: Emotional tone analysis to prioritize hostile content.

```mermaid
classDiagram
    class SentimentAnalyzer {
        -vader_analyzer: VaderSentiment
        -language_detector: LanguageDetector
        -preprocessing_pipeline: Pipeline
        +analyze_sentiment(text): SentimentScore
        +batch_analyze(texts): List[SentimentScore]
        +get_emotion_breakdown(text): EmotionVector
        -preprocess_text(text): str
        -handle_multilingual(text): str
    }
    
    class SentimentScore {
        +positive: float
        +negative: float
        +neutral: float
        +compound: float
        +confidence: float
        +language: str
    }
    
    class EmotionVector {
        +anger: float
        +fear: float
        +joy: float
        +sadness: float
        +surprise: float
        +disgust: float
    }
    
    SentimentAnalyzer --> SentimentScore
    SentimentAnalyzer --> EmotionVector
```

**Analysis Capabilities**:
- **Multi-language Support**: Hindi, English, and regional language analysis
- **Context Awareness**: Understanding of cultural and regional context
- **Emotion Detection**: Beyond sentiment to specific emotional states
- **Confidence Scoring**: Reliability assessment for each analysis
- **Batch Processing**: Efficient processing of large message volumes

### Engagement Analyzer

**Purpose**: Tracking message spread, influence, and viral potential.

```mermaid
graph TB
    subgraph "Engagement Metrics"
        VIEWS[View Counts]
        FORWARDS[Forward Counts]
        REPLIES[Reply Counts]
        REACTIONS[Reaction Counts]
    end
    
    subgraph "Influence Calculation"
        REACH[Message Reach]
        VELOCITY[Spread Velocity]
        INFLUENCE[Influence Score]
        VIRAL[Viral Potential]
    end
    
    subgraph "Network Analysis"
        NODES[Account Nodes]
        EDGES[Interaction Edges]
        CLUSTERS[Cluster Detection]
        CENTRALITY[Centrality Measures]
    end
    
    VIEWS --> REACH
    FORWARDS --> VELOCITY
    REPLIES --> INFLUENCE
    REACTIONS --> VIRAL
    
    REACH --> NODES
    VELOCITY --> EDGES
    INFLUENCE --> CLUSTERS
    VIRAL --> CENTRALITY
```

**Engagement Metrics**:
- **Reach Analysis**: Total audience exposure calculation
- **Velocity Tracking**: Speed of message propagation
- **Influence Scoring**: Author and message influence assessment
- **Network Effects**: Cross-channel amplification detection
- **Viral Prediction**: Early viral spread prediction algorithms

## Intelligence Components

### Threat Scorer

**Purpose**: Quantitative threat assessment combining multiple analysis factors.

```mermaid
graph TD
    subgraph "Input Factors"
        KW_SCORE[Keyword Score]
        SENT_SCORE[Sentiment Score]
        ENG_SCORE[Engagement Score]
        NET_SCORE[Network Score]
        HIST_SCORE[Historical Score]
    end
    
    subgraph "Weighting System"
        WEIGHTS[Dynamic Weights]
        CONTEXT[Context Factors]
        TEMPORAL[Temporal Factors]
    end
    
    subgraph "Scoring Algorithm"
        NORMALIZE[Score Normalization]
        COMBINE[Weighted Combination]
        THRESHOLD[Threshold Evaluation]
    end
    
    subgraph "Output"
        THREAT_LEVEL[Threat Level]
        CONFIDENCE[Confidence Score]
        JUSTIFICATION[Score Justification]
    end
    
    KW_SCORE --> NORMALIZE
    SENT_SCORE --> NORMALIZE
    ENG_SCORE --> NORMALIZE
    NET_SCORE --> NORMALIZE
    HIST_SCORE --> NORMALIZE
    
    WEIGHTS --> COMBINE
    CONTEXT --> COMBINE
    TEMPORAL --> COMBINE
    
    NORMALIZE --> COMBINE
    COMBINE --> THRESHOLD
    THRESHOLD --> THREAT_LEVEL
    THRESHOLD --> CONFIDENCE
    THRESHOLD --> JUSTIFICATION
```

**Scoring Algorithm**:
$$ThreatScore = \sum_{i=1}^{n} w_i \times f_i \times c_i \times t_i$$

Where:
- $w_i$ = Weight for factor $i$
- $f_i$ = Factor score (normalized 0-1)
- $c_i$ = Context multiplier
- $t_i$ = Temporal multiplier

### Threat Classifier

**Purpose**: Categorical classification of threats based on type and severity.

```mermaid
graph LR
    subgraph "Classification Categories"
        PROP[Propaganda]
        DISINFO[Disinformation]
        INCITE[Incitement]
        COORD[Coordinated Campaign]
        FOREIGN[Foreign Influence]
    end
    
    subgraph "Severity Levels"
        CRITICAL[Critical]
        HIGH[High]
        MEDIUM[Medium]
        LOW[Low]
        INFO[Informational]
    end
    
    subgraph "Action Categories"
        IMMEDIATE[Immediate Action]
        PRIORITY[Priority Review]
        MONITOR[Monitor]
        ARCHIVE[Archive]
    end
    
    PROP --> CRITICAL
    DISINFO --> HIGH
    INCITE --> MEDIUM
    COORD --> LOW
    FOREIGN --> INFO
    
    CRITICAL --> IMMEDIATE
    HIGH --> PRIORITY
    MEDIUM --> MONITOR
    LOW --> ARCHIVE
    INFO --> ARCHIVE
```

## Storage Components

### Data Manager

**Purpose**: Centralized data access and persistence management.

```mermaid
classDiagram
    class DataManager {
        -db_connection: SQLAlchemy
        -cache_client: Redis
        -file_storage: FileSystem
        +store_message(message): bool
        +retrieve_message(id): Message
        +query_messages(criteria): List[Message]
        +store_analysis(analysis): bool
        +get_analytics(timeframe): Analytics
        -ensure_data_integrity()
        -optimize_queries()
    }
    
    class Message {
        +id: str
        +content: str
        +timestamp: datetime
        +channel_id: str
        +metadata: dict
        +analysis_results: dict
    }
    
    class Analytics {
        +threat_summary: dict
        +channel_statistics: dict
        +temporal_trends: dict
        +top_influencers: list
    }
    
    DataManager --> Message
    DataManager --> Analytics
```

### Cache Manager

**Purpose**: High-performance data caching for frequently accessed information.

**Caching Strategy**:
- **Hot Data**: Recent messages and active threats (Redis)
- **Warm Data**: Historical analysis results (Database with indexing)
- **Cold Data**: Archived messages and reports (File system)

**Cache Patterns**:
- **Write-through**: Immediate cache update on data modification
- **Read-aside**: Cache population on cache miss
- **TTL-based Expiration**: Automatic cache invalidation
- **Cache Warming**: Proactive cache population for predictable access patterns

## Interface Components

### Dashboard Component

**Purpose**: Interactive web interface for threat visualization and analysis.

```mermaid
graph TB
    subgraph "Dashboard Modules"
        OVERVIEW[Overview Dashboard]
        THREATS[Threat Analysis]
        CHANNELS[Channel Monitoring]
        REPORTS[Intelligence Reports]
        ADMIN[System Administration]
    end
    
    subgraph "Visualization Components"
        CHARTS[Interactive Charts]
        TABLES[Data Tables]
        MAPS[Geographic Maps]
        TIMELINES[Temporal Timelines]
        NETWORKS[Network Diagrams]
    end
    
    subgraph "User Interface"
        AUTH[Authentication]
        NAV[Navigation]
        FILTERS[Data Filters]
        SEARCH[Search Interface]
        EXPORT[Data Export]
    end
    
    OVERVIEW --> CHARTS
    THREATS --> TABLES
    CHANNELS --> MAPS
    REPORTS --> TIMELINES
    ADMIN --> NETWORKS
    
    AUTH --> NAV
    NAV --> FILTERS
    FILTERS --> SEARCH
    SEARCH --> EXPORT
```

**Dashboard Features**:
- **Real-time Updates**: Live data streaming and automatic refresh
- **Interactive Visualizations**: Plotly-based charts and graphs
- **Customizable Views**: User-configurable dashboard layouts
- **Export Capabilities**: PDF, Excel, and CSV export options
- **Mobile Responsive**: Optimized for desktop and mobile access

### API Gateway

**Purpose**: Centralized API management and external system integration.

**API Endpoints**:
- **Authentication**: `/api/v1/auth/*`
- **Messages**: `/api/v1/messages/*`
- **Analysis**: `/api/v1/analysis/*`
- **Alerts**: `/api/v1/alerts/*`
- **Reports**: `/api/v1/reports/*`
- **Administration**: `/api/v1/admin/*`

**API Features**:
- **RESTful Design**: Standard HTTP methods and status codes
- **OpenAPI Documentation**: Comprehensive API documentation
- **Rate Limiting**: Request throttling and quota management
- **Authentication**: JWT-based authentication with role-based access
- **Versioning**: Backward-compatible API versioning

This comprehensive component architecture ensures the system's modularity, scalability, and maintainability while providing the robust functionality needed for effective threat detection and intelligence analysis.
