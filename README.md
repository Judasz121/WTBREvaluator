# WTBREvaluator
War Thunder Battle Rating Evaluator  
Made for War Thunder Realistic Battles  

### How it works
1. Takes a screenshot of a leaderboard.
2. With the help of Tesseract-OCR reads team's vehicle names.
3. Using google search api or web scraping, searches for war thunder wiki page for each vehicle.
4. Web scrapes the BR for RB.
5. Displays the highest BR

### Dependencies  
Aside from dependencies listed in requirements.txt, this project requires you to install Tesseract OCR and provide a path to its .exe in config.json
