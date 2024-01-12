# Pizza Party Bot

Automated bot constructed to play [Pizza Party on MiniGames.com](https://www.minigames.com/games/pizza-party). 

Powered with `pyautogui` for image recognition and mouse control.

![](https://github.com/ravveni/pizza_party_bot/blob/main/preview.gif)
[Full playthrough](https://www.youtube.com/watch?v=wrMP2zDg1ds)
##
Contributing

## Contributing

## Usage
1. Run `main.py` (browser will open, do not resize)
2. Scroll to centre game and remove any banners/cookie agreements/popups
    - Ad size/banner location were too variable leading to inconsistent game screen placement which was out of scope for this bot
3. Press the "Go" button, stop touching mouse/trackpad, sit back, and watch the bot make loads of pizza

## Bot Capabilities
- Navigates through menus and description screens (will wait through any between-level ads)
- Plays through all 5 levels perfectly
- Closes browser and shuts itself down

## Min Requirements
- Firefox web browser
- Python 3.11
- 2.6GHz i7 processor
- 16GB RAM

## Setup
1. Clone the reponsitory
2. (Suggested) Create a virtual environment named 'PPBEnv': `python3 -m venv PPBEnv`
3. Install requirements: `pip3 install -r requirements.txt`
4. Get proper Geckodriver web driver for system:
    - [Download the latest driver here](https://github.com/mozilla/geckodriver/releases)
5. Move downloaded geckodriver executable into PATH: `/usr/local/bin/`

(MacOS only) You will have to grant permissions to your IDE when asked for selenium and the image recognition to work properly.

## Troubleshooting
The only known issue for newer versions of Python on a fresh install is this (workaroundable):
```
Traceback (most recent call last):
  File "/path/to/venv/lib/python3.11/site-packages/pyautogui/__init__.py", line 172, in wrapper
    return wrappedFunction(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/path/to/venv/lib/python3.11/site-packages/pyautogui/__init__.py", line 210, in locateOnScreen
    return pyscreeze.locateOnScreen(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/path/to/venv/lib/python3.11/site-packages/pyscreeze/__init__.py", line 375, in locateOnScreen
    screenshotIm = screenshot(
                   ^^^^^^^^^^^
  File "/path/to/venv/lib/python3.11/site-packages/pyscreeze/__init__.py", line 527, in _screenshot_osx
    if tuple(PIL__version__) < (6, 2, 1):

TypeError: '<' not supported between instances of 'str' and 'int'
```
So you need to click into the reported error file. Replace this code:
```python
if tuple(PIL__version__) < (6, 2, 1):
```
with this code:
```python
if tuple(map(int, PIL__version__.split("."))) < (6, 2, 1):
```
Now everything should work fine. [Source of fix](https://stackoverflow.com/questions/76361049/how-to-fix-typeerror-not-supported-between-instances-of-str-and-int-wh)

## Contributing
If you think of any efficiencies or improvements, don't hesitate to open an issue, PR, or start a discussion!
