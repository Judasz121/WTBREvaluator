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
    # userInputLoop()
    # image = Image.open('./examples/vlcsnap-2022-12-27-13h52m06s709.png')
    # fetcher = DataFetcher(config)
    # await fetcher.runOcrBrEvaluation(image)
    UserCommands.printCommandsDocumentation()
    # UserCommands.instanceMethod(UserCommands())
    pass

    
asyncio.run(main())
