**CS4348 Project 3 Devlog - Day 4**

**Date:** May 7, 2025

**Focus:** Search, traversal, and print/extract commands

**Tasks Completed:**

* Implemented recursive search function traversing node keys and child blocks
* Added search CLI: `search <file> <key>` with printed results or not found error
* Wrote in-order traversal logic to collect key/value pairs for printing and extraction
* Finished `print` command to display sorted pairs to stdout
* Implemented `extract` command to write sorted results to a CSV file
* Added error handling for missing files and invalid formats

**Challenges Faced:**

* Ensuring recursion maintains correct disk reads while preserving memory limits
* Handling edge cases where child pointers are zero (leaf nodes)

**Next Steps:**

* Create `load` command to import bulk key/value pairs from CSV
* Validate large-scale insert performance
* Perform file corruption and recovery testing
