**CS4348 Project 3 Devlog - Day 5**

**Date:** May 8, 2025

**Focus:** CSV bulk loader and final testing

**Tasks Completed:**

* Built `load` command to ingest key-value pairs from a user-specified CSV file
* Verified sequential insert of CSV lines with error checking and key/value parsing
* Stress-tested insertions on large datasets (hundreds of keys) to verify tree balancing
* Conducted full end-to-end testing: `create`, `insert`, `search`, `load`, `print`, `extract`
* Added usage messages and help prompts for invalid command-line formats

**Challenges Faced:**

* Detecting malformed CSV lines and reporting errors without crashing
* Ensuring insert doesn’t violate memory cap (3 node max in memory)

**Next Steps:**

* Final code cleanup and edge case validation
* Submit the final version after double-checking file outputs and block structure
