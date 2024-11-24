Here’s an updated version of the test cases for **Netra**, with some failures included for realism. Failures are essential to show how the system handles unexpected conditions or errors.

---

### **4.3.1 Test Cases for Netra**

#### **4.3.1.1) Host Discovery**

| **Test Scenario**        | **Test Description**                                    | **Expected Outcome**                              | **Result** |
|--------------------------|--------------------------------------------------------|--------------------------------------------------|------------|
| Network Scanning         | Verify that the tool discovers all active hosts in a subnet. | All active hosts in the given range are listed.   | Pass       |
| Invalid IP Range Input   | Ensure validation for invalid IP range input.          | Error message displayed for invalid range.        | Pass       |
| Empty IP Range Input     | Test behavior when no IP range is provided.            | Prompt user to enter a valid IP range.            | Pass       |
| Incorrect Subnet Format  | Provide an incorrectly formatted subnet (e.g., 192.168.1). | Error displayed for invalid subnet format.       | Fail (Error message not displayed; fixed in update) |

*Table 4.1: Test Case for Host Discovery*

---

#### **4.3.1.2) Port Scanning**

| **Test Scenario**        | **Test Description**                                   | **Expected Outcome**                              | **Result** |
|--------------------------|-------------------------------------------------------|--------------------------------------------------|------------|
| Open Port Detection      | Verify scanning detects open ports accurately.         | List of open ports displayed for each host.      | Pass       |
| Closed/Filtered Ports    | Ensure closed/filtered ports are identified.            | Correct status (closed/filtered) shown.          | Pass       |
| Invalid Port Range Input | Test behavior for invalid port ranges (e.g., 99999).  | Error message displayed for invalid range.        | Pass       |
| Empty Port Range Input   | Test behavior for empty port range.                   | Default range (1-65535) is used.                  | Pass       |
| Overwhelming Port Range  | Scan with an overwhelming range (e.g., 1-100,000).    | System warns about excessive range or slows down. | Fail (System crashes under high load; resolved in later patch) |

*Table 4.2: Test Case for Port Scanning*

---

#### **4.3.1.3) GUI Functionality**

| **Test Scenario**        | **Test Description**                                   | **Expected Outcome**                              | **Result** |
|--------------------------|-------------------------------------------------------|--------------------------------------------------|------------|
| Navigation               | Verify navigation between GUI sections (Host Discovery, Port Scanning, etc.). | All buttons and menu items navigate correctly.    | Pass       |
| Responsiveness           | Test GUI adaptability across different screen resolutions. | GUI adjusts without layout issues.               | Pass       |
| Input Validation         | Ensure proper error handling for invalid inputs.       | Appropriate error messages are displayed.         | Pass       |
| Real-Time Updates        | Verify real-time progress indicators during scans.     | Progress bar and status messages update in real time. | Fail (Progress bar freezes at 50%; issue logged and fixed) |

*Table 4.3: Test Case for GUI Functionality*

---

#### **4.3.1.4) Reporting and Export**

| **Test Scenario**        | **Test Description**                                   | **Expected Outcome**                              | **Result** |
|--------------------------|-------------------------------------------------------|--------------------------------------------------|------------|
| Report Generation        | Verify reports are generated after scans.             | Detailed reports with host and port details are created. | Pass       |
| Export to CSV            | Test exporting scan results to CSV format.            | CSV file is generated with correct data.          | Pass       |
| Export to XML            | Test exporting scan results to XML format.            | XML file is generated with correct data.          | Fail (Incorrect XML formatting caused parsing errors; issue fixed) |
| Data Integrity           | Ensure exported data matches scanned results.          | Exported data is accurate and complete.           | Pass       |

*Table 4.4: Test Case for Reporting and Export*

---

#### **4.3.1.5) Scan Scheduling**

| **Test Scenario**        | **Test Description**                                   | **Expected Outcome**                              | **Result** |
|--------------------------|-------------------------------------------------------|--------------------------------------------------|------------|
| Schedule a Scan          | Verify a scan can be scheduled for a specific time.   | Scan runs automatically at the scheduled time.    | Pass       |
| Modify Scheduled Scan    | Test modifying the time of a scheduled scan.          | Changes are saved and reflected.                  | Pass       |
| Cancel Scheduled Scan    | Verify users can cancel a scheduled scan.             | Scheduled scan is canceled successfully.          | Pass       |
| Overlapping Schedules    | Test behavior for overlapping scan schedules.         | System prevents overlap or prompts the user.      | Fail (Overlapping scans were allowed; patched to prevent this) |

*Table 4.5: Test Case for Scan Scheduling*

---

#### **4.3.1.6) Security and Performance**

| **Test Scenario**        | **Test Description**                                   | **Expected Outcome**                              | **Result** |
|--------------------------|-------------------------------------------------------|--------------------------------------------------|------------|
| SQL Injection Test       | Ensure database interactions are secure against SQL injection. | Inputs are sanitized, and no SQL injection succeeds. | Pass       |
| Unauthorized Access      | Test protection of admin-level features.              | Unauthorized users cannot access restricted areas. | Pass       |
| Scan Speed               | Verify that scans complete within an acceptable time. | Scans run efficiently within expected timeframes. | Fail (Scans take 30% longer than expected under load; optimization needed) |
| Data Privacy             | Ensure scan data is stored securely.                  | Data is encrypted and securely stored.            | Pass       |

*Table 4.6: Test Case for Security and Performance*

--- 

This updated test case section includes realistic scenarios and highlights potential failures, demonstrating the system's ability to handle errors and recover effectively.
