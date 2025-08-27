# Sequence Diagrams

## Comprehensive System Interaction Flows

This section provides detailed sequence diagrams illustrating the temporal interactions between system components, external services, and users throughout various operational scenarios.

## Core System Operations

### System Initialization Sequence

```mermaid
sequenceDiagram
    participant ADMIN as System Administrator
    participant SM as System Manager
    participant CM as Component Manager
    participant DB as Database
    participant REDIS as Redis Cache
    participant TG as Telegram API
    participant LOG as Logging Service
    
    ADMIN->>SM: Initialize System
    SM->>LOG: Start logging service
    LOG-->>SM: Logging active
    
    SM->>DB: Initialize database connection
    DB-->>SM: Connection established
    
    SM->>REDIS: Initialize cache connection  
    REDIS-->>SM: Cache ready
    
    SM->>CM: Initialize all components
    activate CM
    
    loop For each component
        CM->>CM: Load component configuration
        CM->>CM: Validate dependencies
        CM->>CM: Start component
    end
    
    CM-->>SM: All components initialized
    deactivate CM
    
    SM->>TG: Test Telegram API connection
    TG-->>SM: Connection verified
    
    SM->>SM: Start monitoring threads
    SM->>LOG: System initialization complete
    SM-->>ADMIN: System ready for operation
```

### Message Collection and Processing Pipeline

```mermaid
sequenceDiagram
    participant TC as Telegram Channel
    participant SC as Scanner Client
    participant QUEUE as Message Queue
    participant WORKER as Processing Worker
    participant NLP as NLP Engine
    participant TS as Threat Scorer
    participant DB as Database
    participant CACHE as Cache
    participant DASH as Dashboard
    
    TC->>SC: New message event
    SC->>SC: Validate message structure
    SC->>SC: Extract message metadata
    SC->>SC: Check rate limits
    
    alt Rate limit OK
        SC->>QUEUE: Enqueue message for processing
        QUEUE->>WORKER: Assign message to worker
        
        activate WORKER
        WORKER->>WORKER: Deserialize message data
        WORKER->>DB: Check for duplicate message
        
        alt New message
            WORKER->>NLP: Process text content
            activate NLP
            NLP->>NLP: Keyword matching
            NLP->>NLP: Sentiment analysis
            NLP->>NLP: Language detection
            NLP-->>WORKER: Analysis results
            deactivate NLP
            
            WORKER->>TS: Calculate threat score
            activate TS
            TS->>TS: Apply scoring algorithm
            TS->>TS: Classify threat level
            TS-->>WORKER: Threat assessment
            deactivate TS
            
            WORKER->>DB: Store processed message
            WORKER->>CACHE: Update real-time metrics
            
            alt High threat level
                WORKER->>DASH: Trigger alert notification
                DASH->>DASH: Generate alert
            end
            
        else Duplicate message
            WORKER->>WORKER: Log duplicate detection
        end
        
        deactivate WORKER
        
    else Rate limited
        SC->>SC: Implement backoff strategy
        SC->>SC: Schedule retry
    end
```

## Intelligence Collection Workflows

### SIGINT Collection Sequence

```mermaid
sequenceDiagram
    participant SCHED as Task Scheduler
    participant SIGINT as SIGINT Collector
    participant TG_CLIENT as Telegram Client
    participant CHANNELS as Channel List
    participant PROCESSOR as Message Processor
    participant VALIDATOR as Data Validator
    participant STORE as Intelligence Store
    
    SCHED->>SIGINT: Trigger scheduled collection
    SIGINT->>CHANNELS: Get active monitored channels
    CHANNELS-->>SIGINT: Channel list with metadata
    
    loop For each channel
        SIGINT->>TG_CLIENT: Connect to channel
        TG_CLIENT->>TG_CLIENT: Authenticate session
        
        alt Connection successful
            TG_CLIENT->>TG_CLIENT: Get latest messages
            TG_CLIENT->>TG_CLIENT: Check for new content
            
            loop For each new message
                TG_CLIENT->>VALIDATOR: Validate message format
                VALIDATOR->>VALIDATOR: Check data integrity
                VALIDATOR->>VALIDATOR: Verify timestamp
                
                alt Valid message
                    VALIDATOR->>PROCESSOR: Send for processing
                    PROCESSOR->>PROCESSOR: Apply initial filters
                    PROCESSOR->>STORE: Queue for storage
                else Invalid message
                    VALIDATOR->>VALIDATOR: Log validation error
                end
            end
            
            TG_CLIENT->>SIGINT: Update last collection timestamp
            
        else Connection failed
            SIGINT->>SIGINT: Log connection error
            SIGINT->>SIGINT: Implement retry logic
        end
    end
    
    SIGINT->>SCHED: Collection cycle complete
```

### HUMINT Tipline Operation

```mermaid
sequenceDiagram
    participant USER as Tip Submitter
    participant BOT as Tipline Bot
    participant VALIDATOR as Submission Validator
    participant QUEUE as Processing Queue
    participant ANALYST as Human Analyst
    participant DB as Database
    participant NOTIF as Notification Service
    
    USER->>BOT: Submit tip via message
    BOT->>BOT: Parse submission format
    BOT->>BOT: Generate unique tip ID
    
    BOT->>VALIDATOR: Validate tip content
    activate VALIDATOR
    VALIDATOR->>VALIDATOR: Check for spam/malicious content
    VALIDATOR->>VALIDATOR: Assess information quality
    VALIDATOR->>VALIDATOR: Categorize tip type
    VALIDATOR-->>BOT: Validation results
    deactivate VALIDATOR
    
    alt Valid tip
        BOT->>USER: Send confirmation with tip ID
        BOT->>QUEUE: Queue tip for analysis
        
        QUEUE->>ANALYST: Notify of new tip
        ANALYST->>DB: Review tip details
        ANALYST->>ANALYST: Assess intelligence value
        
        alt High-value intelligence
            ANALYST->>DB: Flag as priority
            ANALYST->>NOTIF: Trigger urgent notification
            NOTIF->>NOTIF: Alert security teams
        else Standard intelligence
            ANALYST->>DB: File for routine processing
        end
        
        ANALYST->>BOT: Update tip status
        BOT->>USER: Send status update (if requested)
        
    else Invalid tip
        BOT->>USER: Request clarification/rejection
        BOT->>DB: Log invalid submission
    end
```

### Honeypot Intelligence Extraction

```mermaid
sequenceDiagram
    participant HM as Honeypot Manager
    participant HA as Honeypot Account
    participant PG as Private Group
    participant IE as Intelligence Extractor
    participant OPSEC as OpSec Monitor
    participant SECURE_DB as Secure Database
    participant ALERT as Alert System
    
    HM->>HA: Activate honeypot account
    HA->>HA: Load persona profile
    HA->>PG: Monitor group activity
    
    loop Continuous monitoring
        PG->>HA: New message in group
        HA->>IE: Analyze message content
        
        IE->>IE: Extract potential intelligence
        IE->>IE: Assess intelligence value
        
        alt High-value intelligence detected
            IE->>OPSEC: Check extraction risk
            OPSEC->>OPSEC: Assess operational security
            
            alt Risk acceptable
                IE->>SECURE_DB: Store intelligence securely
                IE->>ALERT: Generate intelligence alert
                ALERT->>ALERT: Notify intelligence analysts
            else Risk too high
                OPSEC->>HM: Recommend operation pause
                HM->>HA: Reduce activity level
            end
            
        else Low-value content
            IE->>IE: Discard or log for patterns
        end
        
        HA->>OPSEC: Report activity status
        OPSEC->>OPSEC: Monitor for compromise indicators
        
        alt Compromise suspected
            OPSEC->>HM: Initiate emergency extraction
            HM->>HA: Execute safe shutdown
            HA->>PG: Gradually reduce activity
            HA->>HA: Delete sensitive data
        end
        
        HA->>HA: Maintain persona credibility
        HA->>PG: Post appropriate responses
    end
```

## Analysis and Threat Assessment

### NLP Analysis Pipeline

```mermaid
sequenceDiagram
    participant INPUT as Message Input
    participant PREPROC as Preprocessor
    participant TOKENIZER as Tokenizer
    participant KEYWORD as Keyword Matcher
    participant SENTIMENT as Sentiment Analyzer
    participant NER as Named Entity Recognition
    participant CLASSIFIER as Threat Classifier
    participant OUTPUT as Analysis Output
    
    INPUT->>PREPROC: Raw message text
    PREPROC->>PREPROC: Clean and normalize text
    PREPROC->>PREPROC: Remove noise and formatting
    PREPROC->>PREPROC: Detect language
    
    PREPROC->>TOKENIZER: Preprocessed text
    TOKENIZER->>TOKENIZER: Split into tokens
    TOKENIZER->>TOKENIZER: Remove stop words
    TOKENIZER->>TOKENIZER: Lemmatize tokens
    
    TOKENIZER->>KEYWORD: Token list
    KEYWORD->>KEYWORD: Match against threat keywords
    KEYWORD->>KEYWORD: Apply contextual rules
    KEYWORD->>KEYWORD: Calculate keyword scores
    
    TOKENIZER->>SENTIMENT: Token list  
    SENTIMENT->>SENTIMENT: Analyze emotional tone
    SENTIMENT->>SENTIMENT: Calculate sentiment scores
    SENTIMENT->>SENTIMENT: Detect emotional intensity
    
    TOKENIZER->>NER: Token list
    NER->>NER: Identify entities (person, location, org)
    NER->>NER: Extract relationships
    NER->>NER: Build entity context
    
    par Parallel Classification
        KEYWORD->>CLASSIFIER: Keyword analysis results
        SENTIMENT->>CLASSIFIER: Sentiment analysis results  
        NER->>CLASSIFIER: Entity analysis results
    end
    
    CLASSIFIER->>CLASSIFIER: Combine analysis results
    CLASSIFIER->>CLASSIFIER: Apply classification model
    CLASSIFIER->>CLASSIFIER: Generate confidence scores
    
    CLASSIFIER->>OUTPUT: Complete analysis package
```

### Threat Scoring and Classification

```mermaid
sequenceDiagram
    participant ANALYSIS as Analysis Results
    participant SCORER as Threat Scorer
    participant WEIGHTS as Weight Manager
    participant RULES as Business Rules
    participant HISTORY as Historical Data
    participant CLASSIFIER as Threat Classifier
    participant ALERTS as Alert Manager
    
    ANALYSIS->>SCORER: Analysis data package
    SCORER->>WEIGHTS: Get current scoring weights
    WEIGHTS-->>SCORER: Weight configuration
    
    SCORER->>RULES: Apply business rules
    RULES->>RULES: Check threshold conditions
    RULES->>RULES: Apply contextual modifiers
    RULES-->>SCORER: Rule application results
    
    SCORER->>HISTORY: Get historical context
    HISTORY->>HISTORY: Lookup similar patterns
    HISTORY->>HISTORY: Calculate trend factors
    HISTORY-->>SCORER: Historical context data
    
    SCORER->>SCORER: Calculate base threat score
    SCORER->>SCORER: Apply contextual adjustments
    SCORER->>SCORER: Normalize final score
    
    SCORER->>CLASSIFIER: Threat score and metadata
    CLASSIFIER->>CLASSIFIER: Determine threat category
    CLASSIFIER->>CLASSIFIER: Assign threat level
    CLASSIFIER->>CLASSIFIER: Generate justification
    
    alt Critical threat level
        CLASSIFIER->>ALERTS: Trigger immediate alert
        ALERTS->>ALERTS: Notify on-duty analysts
        ALERTS->>ALERTS: Escalate to supervisors
    else High/Medium threat
        CLASSIFIER->>ALERTS: Queue for review
        ALERTS->>ALERTS: Add to analyst workload
    else Low threat
        CLASSIFIER->>CLASSIFIER: Archive for monitoring
    end
    
    CLASSIFIER->>HISTORY: Update threat patterns
    HISTORY->>HISTORY: Store classification results
```

## User Interface and Reporting

### Dashboard Real-time Updates

```mermaid
sequenceDiagram
    participant ANALYST as Analyst User
    participant DASH as Dashboard Frontend
    participant API as API Gateway
    participant AUTH as Auth Service
    participant CACHE as Cache Layer
    participant DB as Database
    participant WS as WebSocket Service
    
    ANALYST->>DASH: Load dashboard page
    DASH->>AUTH: Authenticate user session
    AUTH->>AUTH: Validate credentials
    AUTH-->>DASH: Authentication successful
    
    DASH->>API: Request dashboard data
    API->>CACHE: Check for cached data
    
    alt Cache hit
        CACHE-->>API: Return cached data
    else Cache miss
        API->>DB: Query latest threat data
        DB-->>API: Return query results
        API->>CACHE: Update cache
    end
    
    API-->>DASH: Dashboard data
    DASH->>DASH: Render initial dashboard
    
    DASH->>WS: Establish WebSocket connection
    WS->>WS: Register client for updates
    
    loop Real-time updates
        DB->>WS: New threat detected
        WS->>WS: Format update message
        WS->>DASH: Send real-time update
        DASH->>DASH: Update dashboard display
        
        alt Critical alert
            DASH->>DASH: Highlight critical threat
            DASH->>ANALYST: Show alert notification
        end
    end
    
    ANALYST->>DASH: Interact with threat data
    DASH->>API: Request detailed analysis
    API->>DB: Fetch threat details
    DB-->>API: Return detailed data
    API-->>DASH: Threat analysis details
    DASH->>DASH: Display detailed view
```

### Report Generation Workflow

```mermaid
sequenceDiagram
    participant ANALYST as Security Analyst
    participant UI as Report Interface
    participant API as API Service
    participant REPORT_GEN as Report Generator
    participant DB as Database
    participant TEMPLATE as Template Engine
    participant EXPORT as Export Service
    participant EMAIL as Email Service
    
    ANALYST->>UI: Request custom report
    UI->>UI: Show report configuration form
    ANALYST->>UI: Specify report parameters
    
    UI->>API: Submit report request
    API->>API: Validate request parameters
    API->>REPORT_GEN: Initialize report generation
    
    REPORT_GEN->>DB: Query threat data
    DB-->>REPORT_GEN: Return filtered results
    
    REPORT_GEN->>REPORT_GEN: Aggregate data
    REPORT_GEN->>REPORT_GEN: Calculate statistics
    REPORT_GEN->>REPORT_GEN: Generate insights
    
    REPORT_GEN->>TEMPLATE: Apply report template
    TEMPLATE->>TEMPLATE: Format data presentation
    TEMPLATE->>TEMPLATE: Generate visualizations
    TEMPLATE-->>REPORT_GEN: Formatted report
    
    REPORT_GEN->>EXPORT: Convert to requested format
    
    alt PDF Export
        EXPORT->>EXPORT: Generate PDF document
    else Excel Export  
        EXPORT->>EXPORT: Create Excel workbook
    else PowerPoint Export
        EXPORT->>EXPORT: Build presentation slides
    end
    
    EXPORT-->>REPORT_GEN: Export complete
    REPORT_GEN->>API: Report generation complete
    API-->>UI: Report ready notification
    
    UI->>ANALYST: Show download link
    
    opt Email delivery requested
        ANALYST->>UI: Request email delivery
        UI->>EMAIL: Send report via email
        EMAIL->>EMAIL: Deliver to recipients
        EMAIL-->>UI: Delivery confirmation
    end
```

## Error Handling and Recovery

### System Error Recovery Sequence

```mermaid
sequenceDiagram
    participant COMP as System Component
    participant ERROR as Error Handler
    participant MONITOR as System Monitor
    participant LOG as Logging Service
    participant ADMIN as Administrator
    participant RECOVERY as Recovery Service
    
    COMP->>COMP: Operation failure occurs
    COMP->>ERROR: Throw exception
    ERROR->>ERROR: Analyze error type
    ERROR->>LOG: Log error details
    
    ERROR->>MONITOR: Report component failure
    MONITOR->>MONITOR: Assess system impact
    
    alt Critical system component failure
        MONITOR->>ADMIN: Send urgent notification
        MONITOR->>RECOVERY: Initiate emergency procedures
        
        RECOVERY->>RECOVERY: Attempt automatic recovery
        
        alt Recovery successful
            RECOVERY->>COMP: Restart component
            COMP->>MONITOR: Report healthy status
            MONITOR->>LOG: Log recovery success
        else Recovery failed
            RECOVERY->>ADMIN: Escalate to manual intervention
            ADMIN->>ADMIN: Perform manual diagnostics
            ADMIN->>RECOVERY: Apply manual fix
        end
        
    else Non-critical failure
        MONITOR->>RECOVERY: Queue for standard recovery
        RECOVERY->>RECOVERY: Apply standard recovery procedure
        RECOVERY->>COMP: Restart with safe configuration
    end
    
    COMP->>MONITOR: Resume normal operation
    MONITOR->>LOG: System recovery complete
```

These sequence diagrams provide detailed insights into the temporal behavior of the system, showing how components interact during various operational scenarios. They serve as essential documentation for understanding system behavior, debugging issues, and ensuring proper implementation of complex workflows.
