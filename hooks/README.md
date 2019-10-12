# Git hooks
When you clone this repo, copy the `post-commit` script to `.git/hooks`. This hook tags the commit with a version number if the version string in `__init__.py` was changed.
