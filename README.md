# MCPRemapper
Remaps minecraft mod class names from one version to another. 

## Usage:
`py remapper.py apply <target> <mappings>`
	where `target` is the file or directory you want to remap, and `mappings` is the mapping csv you want to use.

This outputs to an /output directory your code but with all references to the old classes changed to the new ones.

**Merging Mappings**:

You can merge mappings between two version by using `merge` as the first argument:  
`py remapper.py merge 1.12-to-1.13.1.csv 1.13.1-to-1.14.3.csv > 1.12-to-1.14.3.csv`
