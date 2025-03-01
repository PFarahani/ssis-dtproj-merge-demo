"""
Cleans SSIS .dtproj files by removing references to non-existent packages
Usage: python cleanup-dtproj.py <path_to_project_folder>
"""

import sys
import os
from lxml import etree
from pathlib import Path

def main(project_path):
    # Find .dtproj file
    dtproj_files = list(Path(project_path).glob("*.dtproj"))
    if not dtproj_files:
        print(f"Error: No .dtproj file found in {project_path}")
        return 1
    
    dtproj_path = dtproj_files[0]
    
    # Create backup
    backup_path = dtproj_path.with_name(f"{dtproj_path.name}.bak")
    dtproj_path.rename(backup_path)
    print(f"Backup created at {backup_path}")

    # Parse XML with namespace handling
    ns = {"SSIS": "www.microsoft.com/SqlServer/SSIS"}
    tree = etree.parse(backup_path)
    root = tree.getroot()

    # Find all packages
    packages = root.findall(".//SSIS:Packages/SSIS:Package", ns)
    metadata = root.findall(".//SSIS:PackageMetaData", ns)

    # Map all children to their parents
    parent_map = {child: parent for parent in tree.iter() for child in parent}

    # Check package existence
    for elem in packages + metadata:
        package_name = elem.get('{www.microsoft.com/SqlServer/SSIS}Name')
        if not package_name:
            continue
            
        dtsx_path = Path(project_path) / package_name
        if not dtsx_path.exists():
            parent = parent_map.get(elem)
            if parent is not None:
                parent.remove(elem)

    # Save cleaned file
    tree.write(dtproj_path, pretty_print=False, encoding="utf-8", xml_declaration=True)
    print(f"Cleanup completed. Obsolete packages removed from {dtproj_path.name}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cleanup-dtproj.py <project_folder>")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))