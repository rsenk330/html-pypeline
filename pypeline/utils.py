import sys

# Use unittest2 for Python < 2.7
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
