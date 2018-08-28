"""
存取dot ent檔設定
"""

from pathlib import Path

from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
