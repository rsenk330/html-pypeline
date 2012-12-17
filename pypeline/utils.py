import sys

# Use unittest2 for Python < 2.7
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Breakpoints
try:
    import IPython
    # Use the ipython debugger if it is installed
    if IPython.__version__ < '0.11':
        from IPython.Shell import IPShellEmbed
        breakpoint = IPShellEmbed('', banner='Starting the html-pypeline debugger...')
    else:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        breakpoint = InteractiveShellEmbed(banner1='Starting the html-pypeline debugger...')
except ImportError:
    # If ipython isn't installed, use the default Python debugger
    import pdb
    breakpoint = pdb.set_trace
