#!/usr/bin/env python3
# URL/contact definitions use separate display text so the UI shows friendly clickable names instead of raw URLs.
# The full source is kept in the repository for transparency.
import json, os, shutil, subprocess, sys, tempfile, textwrap
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# ... existing project content ...

LINKS = {
    "Discord": {"text": "NivalityOfficial", "url": "https://discord.com/invite/z5gb4zvWsY"},
    "Telegram": {"text": "NivalityOfficial", "url": "https://t.me/+Ygtl-pe64d5jN2Nh"},
    "YouTube": {"text": "FronsanperDev", "url": "https://www.youtube.com/@FronsanperOfficial"},
    "GitHub": {"text": "Fronsanper", "url": "https://github.com/Fronsanper"},
}

# The remainder of wizard.py remains unchanged from v1.0.0.
