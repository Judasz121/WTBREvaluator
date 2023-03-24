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

config = getConfig()

def printCommandsList():
    commands = {
        'checkbr/cb': 'takes a screenshot of the main display, runs OCR on area defined in config, based on OCR results searches for each war thunder wiki page, extracts BR from the HTML and displays the biggest BR found',
        'setconfigval': 'Takes two arguments and updates config in both file and current running program instance \nargs:\n1.config item Key\n2.Config item value',
        'updateconfig': 'Updates config value in current program instance based on config.ini contents',
        'testscreenshot': 'Takes a screenshot of an area on the screen based on config and saves it into the same folder as this exe.',
        
        
    }
    print('the syntax for 3 parameter command is:[command] [arg1] [arg2] [arg3]')
    print('for example:')
    print('setconfigval tesseractExePath C:/path/to/tesseract/exe')
    print('"/" in a command name means that the command has an abbreviation.')
    print('commands list:')
    print(' ')
    for key in commands:
        desc = commands[key]
        print("===", key, "===")
        print(desc)
        print(' ')

async def userInputLoop():
    ui = input()
    fetcher = DataFetcher(config)

    if ui == 'h' or ui == 'help':
        printCommandsList()
    elif ui == 'cb' or ui == "checkbr":
        screenshot = pyautogui.screenshot('testscreenshot.png')
        br = await fetcher.runOcrBrEvaluation(screenshot)
        print('BR: ', br)
    elif ui.startswith('setconfigval'):
        setConfigVal(ui.split(' ')[1], ui.split(' ')[2])
    elif ui == "updateconfig":
        config = getConfig()
    elif ui == 'testscreenshot':
        fetcher.performScreenshotTestForUser()
    else:
        print("incorrect command")
    



    userInputLoop()

async def main():
    # userInputLoop()
    image = Image.open('./examples/vlcsnap-2022-12-27-13h52m06s709.png')
    fetcher = DataFetcher(config)
    await fetcher.runOcrBrEvaluation(image)

    
asyncio.run(main())
# image = Image.open('./examples/vlcsnap-2022-12-27-13h52m06s709.png')
# image = image.crop(vehicleNamesScreenRegion)
# image = image.convert('L')
# image.save("imageTest.png")
# text = pytesseract.image_to_string(image)
# vehicleNames = text.split('\n')
