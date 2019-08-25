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
        # Omitted until storing version in Sheets, so we can do comparisons
        # addon_version = addon_table.a.text

        # Last Upload Date
        update_epoch = addon_table.abbr['data-epoch']
        upload_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        # Download Path
        href_path = 'https://www.curseforge.com' + addon_table.a['href']
        download_path = href_path.replace('files', 'download')

        return addon_name, upload_date, download_path

    except (AttributeError, IndexError):
        pass

    try:
        # Addon Info Table
        target_game_version = soup.find_all(string=re.compile('1.13.2'))[2]
        addon_table = target_game_version.find_parent("tr")

        # Addon Version
        # Omitted until storing version in Sheets, so we can do comparisons
        # addon_version = addon_table.a.text

        # Last Upload Date
        update_epoch = addon_table.abbr['data-epoch']
        upload_date = datetime.fromtimestamp(int(update_epoch)).strftime('%Y-%m-%d')

        # Download Path
        href_path = 'https://www.curseforge.com' + addon_table.a['href']
        download_path = href_path.replace('files', 'download')

        return addon_name, upload_date, download_path

    except (AttributeError, IndexError):
        pass


def get_wowi(url):
    source = requests.get(url).content
    soup = BeautifulSoup(source, 'html.parser')

    # Addon Name
    addon_name = soup.find('meta', property='og:title')['content']

    # Addon Version
    # Omitted until storing version in Sheets, so we can do comparisons
    # addon_version = soup.find('div', id='version').text.replace('Version: ', '')

    # Last Upload Date
    date_modified = str(soup.find('div', id='safe').text.replace('Updated: ', '')[:-9])
    upload_date = datetime.strptime(date_modified, '%m-%d-%y').date().strftime('%Y-%m-%d')

    # Download Path
    replace_path = url.replace('info', 'download')
    download_path = replace_path.replace('.html', '')

    return addon_name, upload_date, download_path


def get_github(url):
    source = requests.get(url).content
    soup = BeautifulSoup(source, 'html.parser')

    # Addon Name
    raw_addon_name = soup.find('meta', property='og:title')['content']
    addon_name = raw_addon_name.rsplit('/', 1)[1]

    # Addon Info Table
    target_version = soup.find(string=re.compile('Latest commit'))
    addon_table = target_version.find_parent("div")

    # Last Upload Date
    age_data = addon_table.find({'relative-time': 'datetime'})
    raw_time = age_data['datetime']
    upload_date = raw_time[:10]

    # Download Path
    get_path = soup.find(string=re.compile('Download ZIP'))
    path_table = get_path.find_parent("a")
    download_path = 'https://github.com' + path_table.get('href')

    return addon_name, upload_date, download_path
