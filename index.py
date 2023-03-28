# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import sys
import math
import re
import asyncio
import pyautogui
import keyboard
from dataFetcher import DataFetcher
from config import getConfig, setConfig, setConfigVal
from PIL import Image
from commands import UserCommands


async def main():
        
    UserCommands.exec("stest opencc")
    UserCommands.exec("setconfigval googleApiKey yourmomma")
    pass

    
asyncio.run(main())
