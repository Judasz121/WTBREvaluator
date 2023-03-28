
import requests
import asyncio
from lxml import html
from lxml.cssselect import CSSSelector
from PIL import Image, ImageFilter
from pytesseract import pytesseract
import pyautogui
import subprocess
import webbrowser
import googleapiclient.discovery
import os
import sys



# async def websearchVehicleWikiPage(name) -> str:  # google api version
#     service = googleapiclient.discovery.build("customsearch", "v1", developerKey=googleApiKey)
#     response = service.cse().list(q=name, cx=googleCustomSearchEngineKey).execute()

#     # for result in response['items']:
#     #     print(result['title'])
#     #     print(result['link'])
#     #     print(' ')
    
#     nigger = response['items'][0]
#     niggerFaggot = nigger['link']
#     wikiHtml = requests.get(response['items'][0]['link']).text
#     return (name, html.fromstring(wikiHtml))

class DataFetcher:
    # vehicleNamesScreenRegion = (450, 337, 605, 800)
    def __init__(self, config):
        self.tesseractExePath = config['tesseractExePath']
        pytesseract.tesseract_cmd = self.tesseractExePath
        self.vehicleNamesScreenRegion = config['vehicleNamesScreenRegion']
        self.googleApiKey = config['googleApiKey']
        self.googleCustomSearchEngineKey = config['googleCustomSearchEngineKey']


    async def googleApiSearchVehicleWikiPage(self, name) -> str:  # google api version
        print(name + " api search started")
        service = googleapiclient.discovery.build("customsearch", "v1", developerKey=self.googleApiKey)
        response = service.cse().list(q=name, cx=self.googleCustomSearchEngineKey).execute()
        
        wikiHtml = requests.get(response['items'][0]['link']).text
        print('found wiki by google: ' + response['items'][0]['link'])
        return (name, html.fromstring(wikiHtml))

    async def googleScrapeSearchVehicleWikiPage(self, name: str) -> str:
        print(name + " scrape search started")
        #response = requests.get("https://www.google.com/search?q=" + name + '+war+thunder+wiki')
        response = requests.get("https://www.google.com/search?q=" + name + '+site%3Awiki.warthunder.com')
        links = CSSSelector('a[href^="/url?q=https://wiki.warthunder.com/"]')(html.fromstring(response.text))
        
        if len(links) == 0: # accept cookies page showed up
            acceptCoockiesHtml = html.fromstring(response.text)
            form = acceptCoockiesHtml.xpath("//form")[1]
            formInputs = form.xpath('input')
            formData = {}
            for input in formInputs:
                if not input.name == None:
                    formData[input.name] = input.value
            response = requests.post(form.action, formData)
            links = CSSSelector('a[href^="/url?q=https://wiki.warthunder.com/"]')(html.fromstring(response.text))

        
        wikiUrl = links[0].attrib['href']
        wikiUrl = wikiUrl.split('/url?q=')[1].split('&')[0]
        print("found wiki: " , wikiUrl)
        return (name, html.fromstring(requests.get(wikiUrl).text))

    async def runOcrBrEvaluation(self, image: Image, cropped = False):
        if not cropped:
            image = image.crop(self.vehicleNamesScreenRegion)
        image = image.convert('L')
        text = pytesseract.image_to_string(image)
        vehicleNames = text.split('\n')
        webSearchTasks = []
        for name in vehicleNames:
            if name == '':
                continue
            webSearchTasks.append(asyncio.create_task(self.googleApiSearchVehicleWikiPage(name)))

        wikiHtmls = await asyncio.gather(*webSearchTasks)
        def extractBr(wikiHtml):
            try:
                trEls = CSSSelector('.general_info_br tr')(wikiHtml[1])
                br = CSSSelector('td')(trEls[1])[1].text
                return float(br)
            except IndexError:      
                print("wiki page for ", wikiHtml[0], " is incorrect (didn't find the node with BR)")
                return 1
    
        vehicleBrs = list(map(extractBr, wikiHtmls))
        return vehicleBrs

    def performScreenshotTestForUser(self, openImage: bool):
        screenShotFileName = 'testScreenshot.png'
        pyautogui.screenshot(screenShotFileName)
        with Image.open(screenShotFileName) as image:
            image = image.crop(self.vehicleNamesScreenRegion)
            image.save(screenShotFileName)
        absolutePath = os.path.dirname(os.path.realpath(__file__)) + '\\' + screenShotFileName

        if(openImage):
            imageViewerFromCommandLine = {'linux':'xdg-open',
                                    'win32':'explorer',
                                    'darwin':'open'}[sys.platform]
            subprocess.run([imageViewerFromCommandLine, absolutePath])
            # webbrowser.open(path)
        pass



