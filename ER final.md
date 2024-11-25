erDiagram
    USER {
        int UserID PK
        string Name
        string Email
        string Password
        string Role
        datetime CreatedAt
        datetime LastLogin
    }
    
    SCAN {
        int ScanID PK
        int UserID FK
        string ScanType
        string TargetIP
        datetime StartTime
        datetime EndTime
        string Status
        int ReportID FK
        string Parameters
    }
    
    TARGET {
        int TargetID PK
        string IPAddress
        string Hostname
        string OS
        string MACAddress
        int ScanID FK
        string Location
        string Notes
    }
    
    PORT {
        int PortID PK
        int PortNumber
        string Protocol
        string State
        string Service
        int TargetID FK
        string Banner
    }
    
    REPORT {
        int ReportID PK
        int ScanID FK
        string FileName
        string Format
        datetime GeneratedTime
        string Summary
    }

    AUTHENTICATION {
        int AuthID PK
        int UserID FK
        string AuthMethod
        datetime AuthTimestamp
    }

    USER ||--o{ SCAN : initiates
    SCAN ||--o{ TARGET : includes
    TARGET ||--o{ PORT : has
    SCAN ||--o| REPORT : generates
    USER ||--o{ AUTHENTICATION : uses
