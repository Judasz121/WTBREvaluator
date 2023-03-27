import asyncio
from dataFetcher import DataFetcher
from config import getConfig, setConfig, setConfigVal
import pyautogui


class UserCommands:





    @staticmethod
    def printCommandsDocumentation():
        print('the syntax for 3 parameter command is:[command] [arg1] [arg2] [arg3]')
        print('for example:')
        print('setconfigval tesseractExePath C:/path/to/tesseract/exe')
        print('"/" in a command name means that the command has an abbreviation.')
        print('commands:')

        for key in UserCommands.commandsList:
            UserCommands.commandsList[key]['print']()
        pass   


    @staticmethod
    async def checkbr():
        fetcher = DataFetcher(getConfig())
        screenshot = pyautogui.screenshot('testscreenshot.png')
        br = await fetcher.runOcrBrEvaluation(screenshot)
        print('BR: ', br)
        return br
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
        pass
    @staticmethod
    def __setconfigval_print():
        print()
        print("===setconfigvalb===")
        print('Updates the config \nargs:\n1.config item key\n2.Config item value')
        pass

    @staticmethod
    def testscreenshot():
        DataFetcher.performScreenshotTestForUser()
        pass
    @staticmethod
    def __testscreenshot_print():
        print()
        print('===testscreenshot===')
        print('Takes a screenshot of an area on the screen based on config and saves it into the same folder as this .exe.')
        pass

    commandsList = {
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
            'exec': testscreenshot.__func__
        }
    }


