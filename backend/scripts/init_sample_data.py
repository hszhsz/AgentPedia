#!/usr/bin/env python3
"""
初始化示例数据脚本
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import asyncio
from agentpedia.scripts.sample_data import main

if __name__ == "__main__":
    asyncio.run(main())