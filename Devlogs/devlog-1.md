**CS4348 Project 3 Devlog - Day 1**

**Date:** May 4, 2025

**Focus:** Project setup and understanding specification

**Tasks Completed:**

* Carefully read through the entire project specification PDF
* Identified major components required: file management, B-tree node structure, header block, and command interface
* Decided to implement the solution in Python for readability and rapid development
* Defined constants: block size, magic number, B-tree degree
* Drafted initial `Header` class and `BTreeNode` structure based on spec
* Set up byte serialization/deserialization methods for both classes

**Challenges Faced:**

* Needed to visualize the byte layout for a 512-byte block
* Clarified confusion between child pointer indexing and key placement in a B-tree node

**Next Steps:**

* Begin implementing file operations: `create`, `read_node`, `write_node`, `read_header`, and `write_header`
* Create a command-line entry point with argument parsing
