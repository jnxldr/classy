"""This module provides several functions to get informmation about WoW Classic addons from websites.

The library BeautifulSoup is used extensively to scrape the HTML for the desired information.

"""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import os.path
from os import walk
from os import listdir


def get_curse(url):
    """Returns information about WoW Classic addons from Curseforge.

    Two Try-Except blocks are used to account for formatting differences on addon pages,
    depending on whether an addon is Classic only or if it also has a Retail version.
    We're looking for instances of a string '1.13.2', the Classic build version,
    then navigating the HTML tree to find the information we want.

    Parameters:
        url (str): URL of the main addon page

    Returns:
        addon_name (str): Name of the addon without version numbers
        upload_date (str): Date of the latest addon update in YYYY-MM-DD format
        download_path (str): URL for direct download of the latest addon update

    """
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
    """Returns information about WoW Classic addons from WoW Interface.

    Parameters:
        url (str): URL of the main addon page

    Returns:
        addon_name (str): Name of the addon without version numbers
        upload_date (str): Date of the latest addon update in YYYY-MM-DD format
        download_path (str): URL for direct download of the latest addon update

    """
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
    """Returns information about WoW Classic addons from Github.

    We're looking for instances of a string 'Latest commit',
    then navigating the HTML tree to find the information we want.

    Parameters:
        url (str): URL of the main addon page

    Returns:
        addon_name (str): Name of the addon without version numbers
        upload_date (str): Date of the latest addon update in YYYY-MM-DD format
        download_path (str): URL for direct download of the latest addon update

    """
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


def check_local_version():
    """WORK IN PROGRESS
    Goes through the local addon folder and reads the TOC's to get the addon versions.
    Returns:
        local_addon_name (str): Name of the addon according to the local files
        local_addon_version (str): Version of the addon according to the local files

    """
    # base_path = 'F:/Battle.net/World of Warcraft/_classic_/Interface/AddOns/'
    base_path = 'D:/Documents/Coding/Python/4cram/Addons_Test/'
    if not os.path.exists(base_path):
        print('No local addon folder found.')
    else:
        local_addons = listdir(base_path)
        local_file_pair = []
        for directory_name in local_addons:
            directory_name = directory_name
            addon_path = base_path + directory_name + '/'

            for file in listdir(addon_path):
                if file.endswith('.toc'):
                    addon_toc = file
                    toc_path = base_path + directory_name + '/' + addon_toc
                    with open(toc_path, encoding='UTF-8') as fp:
                        read_lines = fp.read()
                        regex = r'## Title\: [a-zA-Z0-9 ]+'
                        pattern = re.compile(regex)
                        matches = pattern.findall(str(read_lines))
                        title_line = matches.replace('## Title: ', '')
                        print(matches)

                        local_file_pair.append([directory_name, matches])
                        #print(read_lines, end='')

        #print(local_file_pair)


        # local_file_pair.append([directory_name, file])
        # print(local_file_pair)

            # for root, directories, files in walk(base_path):
            #     for file in files:
            #         if file.endswith('.toc'):
            #             local_toc = file
            #             print(local_toc)

        # local_addon_names = listdir(base_path)

        # Use once in the directory
        # for file in listdir(base_path):
        #     if file.endswith('.toc'):
        #         print(os.path.join(base_path, file))

        return True
