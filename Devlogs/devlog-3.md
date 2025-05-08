**CS4348 Project 3 Devlog - Day 3**

**Date:** May 6, 2025

**Focus:** Insert operation and B-tree split logic

**Tasks Completed:**

* Built helper for in-memory B-tree insert with disk I/O access limit (max 3 nodes)
* Implemented `insert_non_full` and `split_child` logic based on textbook B-tree approach
* Enabled recursive descent to find insert position while ensuring minimal in-memory usage
* Integrated insert command line handler: `insert <file> <key> <value>`
* Verified successful insertion for basic keys into root and children nodes

**Challenges Faced:**

* Balancing minimal memory usage with recursive insert complexity
* Managing accurate block ID assignments while appending new nodes

**Next Steps:**

* Add full in-order traversal to support `print` and `extract`
* Implement `search` with traversal based on key comparisons
