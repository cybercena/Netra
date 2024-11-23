# Use Case Diagram for Tools like Nmap  

```mermaid
graph TB
    %% Actors
    User["Actor: User"] 
    NetworkAdmin["Actor: Network Admin"]

    %% Use Cases
    HostDiscovery["Use Case: Host Discovery"]
    PortScanning["Use Case: Port Scanning"]
    OSDetection["Use Case: OS Detection"]
    ServiceDetection["Use Case: Service Detection"]
    ReportExport["Use Case: Report Export"]
    Database["Database: Scanned Data Storage"]

    %% Relationships
    User -->|Uses| HostDiscovery
    User -->|Uses| PortScanning
    User -->|Uses| OSDetection
    User -->|Uses| ServiceDetection

    NetworkAdmin -->|Uses| HostDiscovery
    NetworkAdmin -->|Uses| PortScanning
    NetworkAdmin -->|Uses| ReportExport

    %% Database Relationships
    HostDiscovery -->|Stores Data| Database
    PortScanning -->|Stores Data| Database
    OSDetection -->|Stores Data| Database
    ServiceDetection -->|Stores Data| Database
    ReportExport -->|Reads Data| Database
