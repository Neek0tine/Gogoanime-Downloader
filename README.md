
<a href='https://discord.gg/gWqbP9j3EV'> ![Discord](https://img.shields.io/discord/257479001365413889?label=Discord&style=flat-square) This is where I live. </a>

# Gogoanime Downloader

A program to simplify the process of batch downloading anime series. Started off because torrent downloading is slow and I'm too lazy to click the "Download" button on each episode.

Differs from my other downloader <a href="https://github.com/Neek0tine/AnimeKisa-Downloader"> Anime-Kisa downloader </a>, Gogoanime has simpler website and therefore the program does not need selenium webdriver and runs purely on requests. (tl;dr : Runs 2x faster than anime kisa downloader)

## Installation

No executables files has been made available, considering the issue about trojan false positives when packaging through Pyinstaller or Py2Exe. 
To run it, do the following:

1.  Create the python environtment
```
# using pip
pip install -r requirements.txt
```
or if you use conda
```
conda create --name <env_name> --file requirements.txt
```

2. Simply run the main python file, and interact from the command line. No arguments required
```
python main.py
```
📋 <b>All downloaded content are stored in ```C:\Users\<username>\Downloads\Downloader\<Anime Title>``` </b> 📋

## Screenshots
<b> Screenshot may differ from the actual program <br></b>
The main window:

<img src="https://github.com/Neek0tine/Gogoanime-Downloader/blob/main/screenshot0.png" width="840" height="728">

## End-User License Agreement

By running the software, the user acknowledged that:
 1. The user acknowledges that this app is made for EDUCATIONAL PURPOSES ONLY, and the Author emphasize to not use this program so oftenly, as to not disturb the streaming service traffic.
 2. The user agrees and follows the Term of Service provided [LICENSE](https://github.com/Neek0tine/AKDownloader/blob/master/LICENSE)
 3. All changes that happened to end-user's computer, online account, or property made by running this appplication is NOT the responsibility of the author


## Authors

* **Nick "Neek0tine" Calvin** - *Initial work* - [Neek0tine](https://github.com/Neek0tine)

## Contributing

Pull requests are welcome. For major changes, how-to, and in-depth explanation, please discuss it with the author first using the discord link. 

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
<br>
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/Neek0tine/AKDownloader/blob/master/LICENSE) file for details

