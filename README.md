# CSC232 Grade Automation Program (GAP)

This project contains Python scripts for grading CSC232 assignments hosted on GitHub.

Assumptions:

* These scripts are executed in a Linux-like environment
* An SSH-key exists in your GitHub configuration to allow cloning via SSH.

## Scripts

### `grade_one.py`

```bash
$ ./grade_one.py assignment number username
```

where

```bash
assignment = {hw | lab}
number     = {1..12}
username   = GitHub username
```

Currently, this script also assumes that a `Hw` or `Lab` sub-directory exists in the working directory in which this script is executed. 
