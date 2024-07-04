"""
This file just contains the blocklist of the JTW tokens. 
It will be imported by the app and the logout resource so that 
tokens can be added to the blocklist when the user logs out.
"""
from typing import Any
BLOCKLIST: Any = set()