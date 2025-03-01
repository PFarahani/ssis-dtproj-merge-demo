# SSIS `dtproj` Merge Demo

This repository is dedicated to sharing insights and strategies for managing merge conflicts in SQL Server Integration Services (SSIS) projects, with a particular focus on the .dtproj file. Visit the full article on Medium.com <u>[here](https://medium.com/@peymanffarahani/the-challenges-of-collaborative-work-in-ssis-projects-3a7dd566b323)</u>.

### `cleanup-dtproj.py` Script
#### Purpose
This script takes the SSIS solution path and removes obsolete package references from .dtproj files.

#### Usage
Run the following code in your terminal:

```bash
python cleanup-dtproj.py path/to/ssis/project
```