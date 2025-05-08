**CS4348 Project 3 Devlog - Day 2**

**Date:** May 5, 2025

**Focus:** File operations and basic commands

**Tasks Completed:**

* Implemented the `create` command to initialize a new index file with header block
* Added helper functions to read/write 512-byte blocks from/to file
* Created logic for serializing and deserializing `Header` and `BTreeNode` classes
* Added checks for file existence and format verification using magic number
* Implemented `read_header`, `write_header`, `read_node`, `write_node`
* Started basic command-line interface using `sys.argv`

**Challenges Faced:**

* Managing big-endian byte order conversions accurately
* Ensuring padding to 512 bytes while avoiding structural misalignment

**Next Steps:**

* Add stub implementations for `insert`, `search`, `load`, `print`, and `extract`
* Begin building out the recursive B-tree insert logic with node splitting
