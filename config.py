import json
import os
defaultConfig = {
    "vehicleNamesScreenRegion": [450, 337, 605, 800], # x1,y2, x2,y2
    #"tesseractExePath": r"D:\Programming\Tesseract-OCR\tesseract.exe"
    'tesseractExePath': r".\Tesseract-OCR\tesseract.exe",
    "googleApiKey": '',
    "googleCustomSearchEngineKey": "",
}
configFileName = 'config.json'

def getConfig():
    files = os.listdir()
    if configFileName not in files or os.stat(configFileName).st_size == 0:
        with open(configFileName, 'w') as f:
            json.dump(defaultConfig, f)
        return defaultConfig
    else:
        with open(configFileName, 'r') as f:
            config = json.load(f)
        return config

def setConfig(newConfig: dict):
    with open(configFileName, 'w') as f:
        json.dump(newConfig, f)

def setConfigVal(key, value):
    config = getConfig()
    config[key] = value
    print(config)
    setConfig(config)