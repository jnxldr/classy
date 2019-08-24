import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_curse(url):
    classic_version_files = url + '/all?filter-game-version=2020709689%3A7350'  # All 1.13.2 files only
    source = requests.get(classic_version_files).content
    soup = BeautifulSoup(source, 'html.parser')

    # Addon Name
    addon_name = soup.find('meta', property='og:title')['content']

    try:
        # Addon Info Table
        target_game_version = soup.find_all(string=re.compile('1.13.2'))[1]
        addon_table = target_game_version.find_parent("tr")

        # Addon Version
        addon_version = addon_table.a.text

        # Last Updated Date
        update_epoch = addon_table.abbr['data-epoch']
        update_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        # Download Path
        href_path = 'https://www.curseforge.com' + addon_table.a['href']
        download_path = href_path.replace('files', 'download')

        return addon_name, addon_version, update_date, download_path

    except (AttributeError, IndexError):
        pass

    try:
        # Addon Info Table
        target_game_version = soup.find_all(string=re.compile('1.13.2'))[2]
        addon_table = target_game_version.find_parent("tr")

        # Addon Version
        addon_version = addon_table.a.text

        # Last Updated Date
        update_epoch = addon_table.abbr['data-epoch']
        update_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        # Download Path
        href_path = 'https://www.curseforge.com' + addon_table.a['href']
        download_path = href_path.replace('files', 'download')

        return addon_name, addon_version, update_date, download_path

    except (AttributeError, IndexError):
        pass


'''
    # This block isn't currently required.
    # These were workarounds that were useful in the situations described.
    # Now that the variable 'classic_version_files' is used, we always get all the 1.13.2 addon only
    
    try:
        # If the first instance of a 1.13.2 file is also the latest version of the addon
        # but isn't exclusively for Classic
        # I.e., the 'Main File' on the page of a Retail addon ported to Classic

        # Addon Info Table
        target_game_version = soup.find_all(string=re.compile('1.13.2'))[1]
        addon_table = target_game_version.find_parent("article")

        # Addon Version
        addon_version = addon_table.h3.text

        # # Download Path
        # file_path = 'https://www.curseforge.com' + addon_table.a['href']
        # download_path = file_path.replace('files', 'download')

        # Last Updated Date
        update_epoch = addon_table.abbr['data-epoch']
        update_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        return addon_name, addon_version, update_date

    except (AttributeError, IndexError):
        pass

    try:
        # If the first instance of a 1.13.2 file is also the latest version of a Classic exclusive addon
        # I.e., the 'Main File' on the page

        # Addon Info Table
        target_game_version = soup.find_all(string=re.compile('1.13.2'))[1]
        addon_table = target_game_version.find_parent("article")

        # Addon Version
        addon_version = addon_table.h3.text

        # # Download Path
        # file_path = 'https://www.curseforge.com' + addon_table.a['href']
        # download_path = file_path.replace('files', 'download')

        # Last Updated Date
        update_epoch = addon_table.abbr['data-epoch']
        update_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        return addon_name, addon_version, update_date

    except (AttributeError, IndexError):
        pass
'''


def get_wowi(url):
    source = requests.get(url).content
    soup = BeautifulSoup(source, 'html.parser')

    # Addon Name
    addon_name = soup.find('meta', property='og:title')['content']

    # Addon Version
    addon_version = soup.find('div', id='version').text.replace('Version: ', '')

    # Last Updated Date
    date_modified = str(soup.find('div', id='safe').text.replace('Updated: ', '')[:-9])
    update_date = datetime.strptime(date_modified, '%m-%d-%y').date().strftime('%Y-%m-%d')

    # Download Path
    replace_path = url.replace('info', 'download')
    download_path = replace_path.replace('.html', '')

    return addon_name, addon_version, update_date, download_path


def get_github(url):
    source = requests.get(url).content
    soup = BeautifulSoup(source, 'html.parser')

    # Addon Name
    raw_addon_name = soup.find('meta', property='og:title')['content']
    addon_name = raw_addon_name.rsplit('/', 1)[1]

    # Addon Version
    # addon_version = soup.find('div', id='version').text.replace('Version: ', '')

    # Last Updated Date
    date_modified = soup.find('span', itemprop='dateModified').text.replace(',', '')
    update_date = datetime.strptime(date_modified, '%b %d %Y').date().strftime('%Y-%m-%d')

    # Download Path
    get_path = soup.find(string=re.compile('Download ZIP'))
    path_table = get_path.find_parent("a")
    download_path = 'https://github.com' + path_table.get('href')

    return addon_name, update_date, download_path

