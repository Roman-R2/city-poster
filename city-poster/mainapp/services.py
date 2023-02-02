import locale
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pprint import pprint

import requests
from lxml.html import fromstring, tostring

if __name__ == "__main__":
    print(f"{__file__} must include as module.")
