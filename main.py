import os
import winreg
import inquirer
from re import sub
from time import sleep
from textwrap import fill
from tabulate import tabulate
from bs4 import BeautifulSoup
from urllib3 import PoolManager, request
from urllib.parse import urlencode
from pyloader import Loader, DLable


def progress_callback(progress):
    print(f'\r[+] Downloading File: {progress.dlable.file_name}  Progress: ' + '{0:.2f}%'.format(
        progress.percent), end='')
    return False


loader = Loader.get_loader()
loader.configure(max_concurrent=3, update_interval=1, progress_cb=progress_callback, daemon=False)
loader.start()
html = PoolManager()


class downloader:
    def __init__(self):
        self.downloader()

    def search(self):

        _initial_requests = html.request('GET', 'https://gogoanime.pe//search.html?keyword=' + str(
            (urlencode({'q': f'{input("[+] Anime to search: ") or "sword art online"}'}).split('='))[-1]))

        if _initial_requests.status != 200:
            print(f'[!] Gogoanime error code {_initial_requests.status}! Please try again in several minutes!')
            quit()

        _search_result = BeautifulSoup(_initial_requests.data, features='html.parser')
        _search_result = _search_result.select('.last_episodes .items .name a')

        _title_list = []
        _href_list = []

        if len(_search_result) == 0:
            print('[!] Could not find anything. Please try again!')
            self.details()

        else:
            for _index, _item in enumerate(_search_result):
                _title_list.append(_item.text)
                _href_list.append(_item['href'])

            _title_list.append('Cancel')

            selection = [inquirer.List('Selected', message="Which one?", choices=_title_list)]
            title_name = (inquirer.prompt(selection))['Selected']

            if title_name == 'Cancel':
                self.search()

            _index_bridge = int(_title_list.index(f"{title_name}"))
            title_link = _href_list[_index_bridge]

            return title_name, title_link

    def details(self):
        _search_result = self.search()
        _title = ""
        try:
            _title = _search_result[0]
        except TypeError:
            self.downloader()

        _link = _search_result[1]
        _details_result = html.request('GET', 'https://gogoanime.pe/' + _link)
        _details_result = BeautifulSoup(_details_result.data, features='html.parser')

        infodes = [_details.text.replace('\n', '') for _details in _details_result.find_all('p', {'class': 'type'})]
        infodes = [_det if ':' not in _det else (_det.split(': ')[-1]) for _det in infodes]
        infodes.append(_details_result.find('a', {'class': 'active'}).text.split('-')[-1])

        print(tabulate([['Title', _title],
                        ['Alternative Title', infodes[5]],
                        ['Genre', infodes[2]],
                        ['Type', infodes[0]],
                        ['Status', infodes[4]],
                        ['Released', infodes[3]],
                        ['Episodes', infodes[6]]], tablefmt='orgtbl'), '\n\n' + fill(infodes[1], 80), '\n')

        return infodes[-1], _link, _title

    def downloader(self):
        _details_result = self.details()
        _episodes = int(_details_result[0])
        _link = _details_result[1]
        _filename = sub('[^A-Za-z0-9-,!() ]+', '', _details_result[2])
        _custom_episode = int()
        _queue = list()

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
            download_location = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

        download_confirmation = [
            inquirer.List('Selected', message="Proceed to download??", choices=['Cancel', 'All', 'Single'])]
        download_confirmation = (inquirer.prompt(download_confirmation))['Selected']

        if download_confirmation == 'Cancel':
            self.downloader()

        elif download_confirmation == 'Single':
            while _custom_episode == 0:
                try:
                    _custom_episode = int(input(f'[+] Which episode you wish to download? (1-{_episodes}): '))
                except ValueError:
                    print(f'[!] Please enter a valid episode (1 - {_episodes}')

        else:
            _file_list = os.scandir(download_location + '/Downloader')
            try:
                os.makedirs(f'{download_location}\\Downloader\\{_filename}')
                _queue = [ep for ep in list(range(1, _episodes + 1))]

            except FileExistsError:
                _queue = [ep for ep in list(range(1, _episodes + 1)) if
                          ep not in ([int(((str(entry)).split(' '))[-1].split('.')[0]) for entry in (os.scandir(
                              download_location + '/Downloader/' + _filename))])]

                if len(_queue) == 0:
                    print('[+] File already exists without missing an episode. Please look for a new series!')
                    self.downloader()

                print('[+] Found existing folder in the directory, checking for episodes ... ')
                print(f'[+] Downloading missing episodes: {", ".join(str(v) for v in _queue)}.')

        def get_files(url, episode):
            _download_page = BeautifulSoup((html.request('GET', url)).data, features='html.parser').select(
                '#wrapper_bg > section > section.content_left > div:nth-child(1) > div.anime_video_body > '
                'div.anime_video_body_cate > div.favorites_book > ul > li.dowloads > a')

            _download_link = (BeautifulSoup((html.request('GET', _download_page[0]['href'])).data,
                                            features='html.parser').select_one(
                '#main > div > div.content_c > div > div:nth-child(5) > div:nth-child(3) > a'))['href']

            target = DLable(url=_download_link, target_dir=f'{download_location}\\Downloader\\{_filename}',
                            file_name=f'{_filename} Episode {str(episode)}.mp4')
            loader.download(target)

            while loader.is_active():
                sleep(2)

        if _custom_episode != 0:
            link = ('https://gogoanime.pe/' + (str(_link).split('/'))[-1] + '-episode-' + str(_custom_episode))
            get_files(link, _custom_episode)
            print('[+] Download complete!\n')
            self.downloader()

        else:
            link = [('https://gogoanime.pe/' + (str(_link).split('/'))[-1] + '-episode-' + str(x)) for x in _queue]
            for index, item in enumerate(link):
                get_files(item, index + 1)
                print()
            print('[+] Download complete!\n')
            self.downloader()


if __name__ == '__main__':
    print(
        '=' * 55 + '\n _ _ _         _   \n| | | |___ ___| |_   Gogoanime Downloader by Neek0tine\n| | | | -_| -_| . '
                   '|  Version 0.1\n|_____|___|___|___|  https://github.com/neek0tine\n' + '=' * 55)

    d = downloader()
