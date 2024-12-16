+-----------------+      +----------------------------+
|                 |      |                            |
|   Library User  |      |    Library Management      |
|    (External    | <--> |         System             |
|    Entity)      |      |    (Process 0)             |
|                 |      |                            |
+-----------------+      +----------------------------+
                           |         ^         |
                           |         |         |
                           v         |         v
                     +------------+    +----------------+
                     | Librarian  |    | Admin           |
                     | (External  |    | (External       |
                     |  Entity)   |    |  Entity)        |
                     +------------+    +----------------+
                             ^
                             |
                             v
                      +-------------------+
                      |    External       |
                      |    Database       |
                      +-------------------+
