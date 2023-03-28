import asyncio
from dataFetcher import DataFetcher
from config import getConfig, setConfig, setConfigVal
import pyautogui
from collections import deque
from inspect import signature, iscoroutinefunction

class UserCommands:





    @staticmethod
    def printCommandsDocumentation():
        print('the syntax for 3 parameter command is:[command] [arg1] [arg2] [arg3]')
        print('for example:')
        print('setconfigval tesseractExePath C:/path/to/tesseract/exe')
        print('"/" in a command name means that the command has an abbreviation.')
        print('commands:')

        for key in UserCommands.commandsDict:
            UserCommands.commandsDict[key]['print']()
        pass   


    @staticmethod
    async def checkbr():
        fetcher = DataFetcher(getConfig())
        screenshot = pyautogui.screenshot()
        brs = await fetcher.runOcrBrEvaluation(screenshot)
        print(brs)
        print('max BR: ', max(brs))
        pass   
    @staticmethod
    def __checkbr_print():
        print()
        print("===checkbr/br===")
        print('Takes a screenshot of the main display, runs OCR on area defined in config, based on OCR results searches for each war thunder wiki page, extracts BR from the HTML and displays the biggest BR found')
        pass     

    @staticmethod
    async def setconfigval(key, value):
        setConfigVal(key, value)
        print("config updated")
        print(getConfig())
        pass
    @staticmethod
    def __setconfigval_print():
        print()
        print("===setconfigvalb===")
        print('Updates the config \nargs:\n1.config item key\n2.Config item value')
        pass

    @staticmethod
    def testscreenshot(open = ""):
        if open.lower() in ['o', 'open']:
            open = True
        else: open = False
        DataFetcher(getConfig()).performScreenshotTestForUser(open)
        pass
    @staticmethod
    def __testscreenshot_print():
        print()
        print('===testscreenshot===')
        print('Takes a screenshot of an area on the screen based on config and saves it into the same folder as this .exe.')
        print('args:\n1.opens file with default photo viewer if "o" or "open" is provided')
        pass

    commandsDict = {
        'checkbr': {
            'print': __checkbr_print.__func__,
            'abbreviations': 'cb',
            'exec': checkbr.__func__,
        },
        'setconfigval': {
            'print': __setconfigval_print.__func__,
            'exec': setconfigval.__func__  
        },
        'testscreenshot': {
            'print': __testscreenshot_print.__func__,
            'abbreviations': 'stest',
            'exec': testscreenshot.__func__
        }
    }

    @staticmethod
    async def exec(inputCmd):
        inputCmd = inputCmd.strip()
        args = deque(inputCmd.split(' '))
        inputCmd = args.popleft()
        if inputCmd.lower() in ['help', 'h']:
            UserCommands.printCommandsDocumentation()
            return
        
        def checkCommandNameMatch(dictCmd):
            if(dictCmd.lower() == inputCmd.lower()):
                return True
            if not 'abbreviations' in UserCommands.commandsDict[dictCmd]:
                return False
            abbr = UserCommands.commandsDict[dictCmd]['abbreviations']
            if(isinstance(abbr, list) and inputCmd in abbr):
                return True
            elif isinstance(abbr, str) and abbr.lower() == inputCmd.lower():
                return True
            return False                
            pass
        foundCmd = list(filter(checkCommandNameMatch, UserCommands.commandsDict))
        if(len(foundCmd) > 0):
            func = UserCommands.commandsDict[foundCmd[0]]['exec']
            funcArgsNum = len(signature(func).parameters)
            if(funcArgsNum < len(args)):
                print(f"This command accepts a maximum of {funcArgsNum} parameters, while you provided {len(args)}. Behave yourself!")
                return False
            elif iscoroutinefunction(func):
                await func(*args)
            else:
                func(*args)
            return True
        else:
            print("Command not recognized.")
            print('Use "h" or "help" for a list of commands.')        
            return False
        pass


