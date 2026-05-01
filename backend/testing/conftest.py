import sys
from unittest.mock import MagicMock

# Mock the db module before anything imports it
sys.modules['db'] = MagicMock()
sys.modules['models'] = MagicMock()