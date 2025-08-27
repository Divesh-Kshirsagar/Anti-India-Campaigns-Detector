# UML Diagrams

## System Architecture UML Diagrams

This section provides comprehensive UML diagrams that illustrate the structural and behavioral aspects of the Anti-India Campaign Detection System.

## Class Diagrams

### Core System Classes

```mermaid
classDiagram
    class SystemManager {
        -config: SystemConfig
        -logger: Logger
        -components: Dict[str, Component]
        +initialize_system()
        +start_monitoring()
        +stop_monitoring()
        +get_system_status(): SystemStatus
        +handle_shutdown()
    }
    
    class ComponentManager {
        <<abstract>>
        -name: str
        -status: ComponentStatus
        -config: Config
        +start()
        +stop()
        +restart()
        +get_health(): HealthStatus
    }
    
    class DataCollector {
        -channels: List[Channel]
        -api_client: TelegramClient
        -message_queue: Queue
        +add_channel(channel: Channel)
        +remove_channel(channel_id: str)
        +collect_messages()
        +validate_message(message: Message): bool
    }
    
    class MessageProcessor {
        -nlp_engine: NLPEngine
        -threat_scorer: ThreatScorer
        -classifier: ThreatClassifier
        +process_message(message: Message): ProcessedMessage
        +batch_process(messages: List[Message]): List[ProcessedMessage]
        +update_processing_rules()
    }
    
    class ThreatAnalyzer {
        -keyword_matcher: KeywordMatcher
        -sentiment_analyzer: SentimentAnalyzer
        -engagement_tracker: EngagementTracker
        +analyze_threat(message: Message): ThreatAssessment
        +calculate_threat_score(factors: ThreatFactors): float
        +classify_threat_type(assessment: ThreatAssessment): ThreatType
    }
    
    class IntelligenceStore {
        -database: Database
        -cache: CacheManager
        -file_system: FileStorage
        +store_message(message: ProcessedMessage)
        +retrieve_messages(criteria: SearchCriteria): List[ProcessedMessage]
        +store_analysis(analysis: ThreatAssessment)
        +get_analytics(timeframe: TimeRange): Analytics
    }
    
    class DashboardService {
        -web_server: WebServer
        -auth_manager: AuthenticationManager
        -visualization_engine: VisualizationEngine
        +render_dashboard(): Dashboard
        +handle_user_request(request: UserRequest): Response
        +generate_report(criteria: ReportCriteria): Report
    }
    
    SystemManager --> ComponentManager
    ComponentManager <|-- DataCollector
    ComponentManager <|-- MessageProcessor
    ComponentManager <|-- ThreatAnalyzer
    ComponentManager <|-- IntelligenceStore
    ComponentManager <|-- DashboardService
    
    DataCollector --> MessageProcessor
    MessageProcessor --> ThreatAnalyzer
    ThreatAnalyzer --> IntelligenceStore
    IntelligenceStore --> DashboardService
```

### Message Processing Classes

```mermaid
classDiagram
    class Message {
        -id: str
        -telegram_id: int
        -channel_id: str
        -content: str
        -timestamp: datetime
        -author: User
        -metadata: MessageMetadata
        +get_content(): str
        +get_timestamp(): datetime
        +is_forwarded(): bool
        +get_forward_chain(): List[Forward]
    }
    
    class ProcessedMessage {
        -original_message: Message
        -keyword_matches: List[KeywordMatch]
        -sentiment_score: SentimentScore
        -engagement_metrics: EngagementMetrics
        -threat_assessment: ThreatAssessment
        +get_threat_level(): ThreatLevel
        +get_confidence_score(): float
        +is_actionable(): bool
    }
    
    class KeywordMatch {
        -keyword: str
        -pattern: str
        -context: str
        -confidence: float
        -category: KeywordCategory
        +get_relevance_score(): float
        +get_context_window(): str
    }
    
    class SentimentScore {
        -positive: float
        -negative: float
        -neutral: float
        -compound: float
        -confidence: float
        -emotional_intensity: float
        +get_dominant_sentiment(): SentimentType
        +is_hostile(): bool
        +get_threat_indicator(): float
    }
    
    class ThreatAssessment {
        -threat_level: ThreatLevel
        -threat_type: ThreatType
        -confidence: float
        -justification: str
        -recommended_actions: List[Action]
        -expiry_time: datetime
        +is_critical(): bool
        +requires_immediate_action(): bool
        +get_escalation_path(): List[Role]
    }
    
    class EngagementMetrics {
        -views: int
        -forwards: int
        -replies: int
        -reactions: Dict[str, int]
        -reach_estimate: int
        -viral_coefficient: float
        +calculate_influence_score(): float
        +predict_viral_potential(): float
        +get_amplification_rate(): float
    }
    
    Message --> ProcessedMessage
    ProcessedMessage --> KeywordMatch
    ProcessedMessage --> SentimentScore
    ProcessedMessage --> ThreatAssessment
    ProcessedMessage --> EngagementMetrics
```

### Intelligence Collection Classes

```mermaid
classDiagram
    class IntelligenceCollector {
        <<abstract>>
        -collection_type: CollectionType
        -active: bool
        -metrics: CollectionMetrics
        +start_collection()
        +stop_collection()
        +get_collection_stats(): CollectionStats
    }
    
    class SIGINTCollector {
        -telegram_client: TelegramClient
        -monitored_channels: List[Channel]
        -rate_limiter: RateLimiter
        -connection_pool: ConnectionPool
        +monitor_channels()
        +handle_new_message(message: TelegramMessage)
        +manage_rate_limits()
        +recover_from_connection_error()
    }
    
    class HUMINTCollector {
        -tipline_bot: TelegramBot
        -submission_queue: Queue[TipSubmission]
        -validation_engine: SubmissionValidator
        +handle_tip_submission(submission: TipSubmission)
        +validate_tip(tip: Tip): ValidationResult
        +process_anonymous_submission(submission: AnonymousSubmission)
    }
    
    class HoneypotCollector {
        -honeypot_accounts: List[HoneypotAccount]
        -target_groups: List[PrivateGroup]
        -operational_security: OpSec
        +deploy_honeypot(target: TargetGroup): HoneypotAccount
        +maintain_cover(account: HoneypotAccount)
        +extract_intelligence(group: PrivateGroup): Intelligence
        +ensure_operational_security()
    }
    
    class Channel {
        -id: str
        -name: str
        -username: str
        -subscriber_count: int
        -description: str
        -risk_level: RiskLevel
        -monitoring_active: bool
        +get_recent_messages(limit: int): List[Message]
        +get_channel_statistics(): ChannelStats
        +is_high_risk(): bool
    }
    
    class TipSubmission {
        -id: str
        -submitter_id: str
        -content: str
        -submission_time: datetime
        -validation_status: ValidationStatus
        -priority: Priority
        +anonymize_submitter()
        +validate_content(): ValidationResult
        +get_intelligence_value(): float
    }
    
    class HoneypotAccount {
        -account_id: str
        -persona: PersonaProfile
        -groups: List[PrivateGroup]
        -operational_status: OpStatus
        -cover_maintenance: CoverMaintenance
        +join_target_group(group: PrivateGroup): bool
        +maintain_persona()
        +extract_high_value_intelligence(): List[Intelligence]
        +assess_operational_risk(): RiskAssessment
    }
    
    IntelligenceCollector <|-- SIGINTCollector
    IntelligenceCollector <|-- HUMINTCollector
    IntelligenceCollector <|-- HoneypotCollector
    
    SIGINTCollector --> Channel
    HUMINTCollector --> TipSubmission
    HoneypotCollector --> HoneypotAccount
```

## Activity Diagrams

### Message Processing Workflow

```mermaid
flowchart TD
    START([Message Received]) --> VALIDATE{Valid Message?}
    VALIDATE -->|No| DISCARD[Discard Message]
    VALIDATE -->|Yes| DEDUPE{Duplicate Check}
    
    DEDUPE -->|Duplicate| UPDATE[Update Existing]
    DEDUPE -->|New| EXTRACT[Extract Metadata]
    
    EXTRACT --> KEYWORD[Keyword Matching]
    KEYWORD --> MATCH{Keywords Found?}
    
    MATCH -->|No| ARCHIVE[Archive as Low Priority]
    MATCH -->|Yes| SENTIMENT[Sentiment Analysis]
    
    SENTIMENT --> ENGAGE[Engagement Analysis]
    ENGAGE --> SCORE[Calculate Threat Score]
    
    SCORE --> CLASSIFY[Classify Threat Level]
    CLASSIFY --> THRESHOLD{Above Threshold?}
    
    THRESHOLD -->|No| STORE[Store for Monitoring]
    THRESHOLD -->|Yes| ALERT[Generate Alert]
    
    ALERT --> NOTIFY[Notify Analysts]
    NOTIFY --> DASHBOARD[Update Dashboard]
    
    UPDATE --> END([Process Complete])
    ARCHIVE --> END
    STORE --> END
    DASHBOARD --> END
    DISCARD --> END
```

### Intelligence Collection Workflow

```mermaid
flowchart TD
    START([System Start]) --> INIT[Initialize Collectors]
    INIT --> PARALLEL{Start Parallel Collection}
    
    PARALLEL --> SIGINT[SIGINT Collection]
    PARALLEL --> HUMINT[HUMINT Collection]
    PARALLEL --> HONEYPOT[Honeypot Collection]
    
    SIGINT --> SCAN[Scan Public Channels]
    SCAN --> MSG_DETECT[Detect New Messages]
    MSG_DETECT --> SIGINT_PROCESS[Process SIGINT Data]
    
    HUMINT --> LISTEN[Listen for Tips]
    LISTEN --> TIP_RECEIVE[Receive Tip Submission]
    TIP_RECEIVE --> VALIDATE_TIP[Validate Tip]
    VALIDATE_TIP --> HUMINT_PROCESS[Process HUMINT Data]
    
    HONEYPOT --> MONITOR[Monitor Private Groups]
    MONITOR --> INTELLIGENCE[Extract Intelligence]
    INTELLIGENCE --> OPSEC[Maintain OpSec]
    OPSEC --> HONEYPOT_PROCESS[Process Honeypot Data]
    
    SIGINT_PROCESS --> MERGE[Merge Intelligence]
    HUMINT_PROCESS --> MERGE
    HONEYPOT_PROCESS --> MERGE
    
    MERGE --> CORRELATE[Cross-Reference Sources]
    CORRELATE --> PRIORITIZE[Prioritize by Threat Level]
    PRIORITIZE --> DISTRIBUTE[Distribute to Analysts]
    
    DISTRIBUTE --> END([Intelligence Ready])
```

## Sequence Diagrams

### Threat Detection Sequence

```mermaid
sequenceDiagram
    participant TC as Telegram Channel
    participant SC as Scanner Client
    participant MP as Message Processor
    participant TA as Threat Analyzer
    participant IS as Intelligence Store
    participant DS as Dashboard Service
    participant AN as Analyst
    
    TC->>SC: New message posted
    SC->>SC: Validate message format
    SC->>MP: Send message for processing
    
    MP->>MP: Extract metadata
    MP->>MP: Check for duplicates
    MP->>TA: Analyze for threats
    
    TA->>TA: Keyword matching
    TA->>TA: Sentiment analysis
    TA->>TA: Calculate threat score
    TA->>TA: Classify threat level
    
    alt High Threat Detected
        TA->>IS: Store threat assessment
        IS->>DS: Trigger alert update
        DS->>AN: Send real-time alert
        AN->>DS: Acknowledge alert
    else Low/Medium Threat
        TA->>IS: Store for monitoring
        IS->>DS: Update statistics
    end
    
    DS->>DS: Update dashboard display
    DS->>AN: Refresh dashboard view
```

### Honeypot Operation Sequence

```mermaid
sequenceDiagram
    participant HM as Honeypot Manager
    participant HA as Honeypot Account
    participant TG as Target Group
    participant IE as Intelligence Extractor
    participant OS as OpSec Monitor
    participant DB as Database
    
    HM->>HA: Deploy honeypot account
    HA->>HA: Establish persona
    HA->>TG: Request group access
    TG->>HA: Grant access
    
    loop Intelligence Gathering
        TG->>HA: Group messages
        HA->>IE: Filter high-value content
        IE->>IE: Assess intelligence value
        
        alt High-Value Intelligence
            IE->>DB: Store intelligence
            IE->>OS: Check operational security
            OS->>OS: Assess exposure risk
            
            alt Risk Acceptable
                OS->>HM: Continue operation
            else Risk Too High
                OS->>HM: Recommend extraction
                HM->>HA: Initiate safe extraction
            end
        else Low-Value Content
            IE->>IE: Discard or archive
        end
        
        HA->>HA: Maintain persona activity
        HA->>TG: Participate in discussions
    end
```

## Component Diagrams

### System Deployment Architecture

```mermaid
graph TB
    subgraph "External Systems"
        TG_API[Telegram API]
        EXT_INTEL[External Intelligence]
        NOTIFY_SYS[Notification Systems]
    end
    
    subgraph "Application Layer"
        WEBAPP[Web Application]
        API_GW[API Gateway]
        AUTH_SVC[Authentication Service]
    end
    
    subgraph "Processing Layer"
        COLLECTOR[Data Collector]
        PROCESSOR[Message Processor]
        ANALYZER[Threat Analyzer]
        INTEL_GEN[Intelligence Generator]
    end
    
    subgraph "Data Layer"
        CACHE[Redis Cache]
        DATABASE[SQLite Database]
        FILE_STORE[File Storage]
        QUEUE[Message Queue]
    end
    
    subgraph "Infrastructure Layer"
        MONITOR[System Monitor]
        LOGGER[Logging System]
        BACKUP[Backup System]
        SECURITY[Security Framework]
    end
    
    %% External Connections
    TG_API --> COLLECTOR
    EXT_INTEL --> INTEL_GEN
    NOTIFY_SYS --> API_GW
    
    %% Application Layer
    WEBAPP --> API_GW
    API_GW --> AUTH_SVC
    AUTH_SVC --> SECURITY
    
    %% Processing Flow
    COLLECTOR --> QUEUE
    QUEUE --> PROCESSOR
    PROCESSOR --> ANALYZER
    ANALYZER --> INTEL_GEN
    
    %% Data Management
    PROCESSOR --> CACHE
    INTEL_GEN --> DATABASE
    ANALYZER --> FILE_STORE
    
    %% Infrastructure
    MONITOR --> LOGGER
    BACKUP --> DATABASE
    SECURITY --> LOGGER
    
    %% Cross-Layer Dependencies
    API_GW --> INTEL_GEN
    WEBAPP --> CACHE
    COLLECTOR --> MONITOR
```

## State Diagrams

### System Operational States

```mermaid
stateDiagram-v2
    [*] --> Initializing
    
    Initializing --> Starting: Configuration loaded
    Starting --> Operational: All components started
    Starting --> Error: Component failure
    
    Operational --> Monitoring: Normal operation
    Operational --> Maintenance: Scheduled maintenance
    Operational --> Alert: Threat detected
    Operational --> Degraded: Partial component failure
    
    Monitoring --> Alert: High-priority threat
    Monitoring --> Operational: Continue monitoring
    
    Alert --> Operational: Alert processed
    Alert --> Critical: Escalation required
    
    Critical --> Operational: Crisis resolved
    Critical --> Shutdown: System compromise
    
    Degraded --> Operational: Components recovered
    Degraded --> Error: Multiple failures
    
    Maintenance --> Operational: Maintenance complete
    Maintenance --> Error: Maintenance failure
    
    Error --> Recovery: Error handling initiated
    Recovery --> Operational: Recovery successful
    Recovery --> Shutdown: Recovery failed
    
    Shutdown --> [*]
    
    note right of Initializing: Load configuration, initialize components
    note right of Monitoring: Continuous threat detection active
    note right of Alert: Analyst notification triggered
    note right of Critical: Immediate intervention required
    note right of Degraded: Reduced capability operation
```

### Threat Assessment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Detected
    
    Detected --> Analyzing: Initial processing
    Analyzing --> Classified: Analysis complete
    Classified --> Validated: Human validation
    Classified --> Rejected: False positive
    
    Validated --> Active: Confirmed threat
    Validated --> Monitoring: Requires watching
    
    Active --> Escalated: High priority
    Active --> Investigating: Under review
    
    Escalated --> Resolved: Action taken
    Escalated --> Contained: Threat mitigated
    
    Investigating --> Active: Confirmed dangerous
    Investigating --> Monitoring: Downgraded
    Investigating --> Closed: Not actionable
    
    Monitoring --> Active: Threat escalation
    Monitoring --> Closed: Natural expiration
    
    Contained --> Closed: Full resolution
    Resolved --> Closed: Incident complete
    
    Rejected --> [*]
    Closed --> [*]
    
    note right of Detected: Initial keyword/sentiment match
    note right of Analyzing: NLP and engagement analysis
    note right of Classified: Threat level assigned
    note right of Validated: Analyst confirmation
    note right of Active: Requires immediate attention
    note right of Escalated: Highest priority action
```

These UML diagrams provide a comprehensive view of the system's architecture, behavior, and operational workflows, serving as essential documentation for development, maintenance, and operational teams.
