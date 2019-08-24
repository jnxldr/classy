import tldextract

from azeroth import get_curse, get_wowi, get_github
from google_api_call import google_read


def main():
    """Gets all addons from the spreadsheet and compares upload dates against live dates.
    """
    spreadsheet_id = '1FF2AMBdi8GQSKecYbeGA_tQEB3XhH-QXG0xTegqvxks'
    spreadsheet_source = 'Tested!A2:E'

    addon_list = google_read(spreadsheet_id, spreadsheet_source)

    if not addon_list:
        print('No data found.')
    else:
        print('Checking for addons with different upload dates than those you stored...', '\n')

        for stored_addon_info in addon_list:
            url = stored_addon_info[2]
            last_update = stored_addon_info[4]
            domain_extract = tldextract.extract(url).domain

            if domain_extract in 'curseforge':
                live_addon_info = get_curse(url)
                if live_addon_info[2] != last_update:
                    print('Name: ', live_addon_info[0])
                    print('Current Version: ', live_addon_info[1])
                    print('Current Upload Date: ', live_addon_info[2])
                    print('Stored Upload Date: ', last_update)
                    print('Download: ', live_addon_info[3], '\n')

            elif domain_extract in 'wowinterface':
                live_addon_info = get_wowi(url)
                if live_addon_info[2] != last_update:
                    print('Name: ', live_addon_info[0])
                    print('Current Version: ', live_addon_info[1])
                    print('Current Upload Date: ', live_addon_info[2])
                    print('Stored Upload Date: ', last_update)
                    print('Download: ', live_addon_info[3], '\n')

            elif domain_extract in 'github':
                live_addon_info = get_github(url)
                if live_addon_info[1] != last_update:
                    print('Name: ', live_addon_info[0])  # Different index  for github as I don't return the version
                    print('Current Upload Date: ', live_addon_info[1])
                    print('Stored Upload Date: ', last_update)
                    print('Download: ', live_addon_info[2], '\n')
                pass
            else:
                pass

    print('Done checking the spreadsheet.')

if __name__ == '__main__':
    main()

    '''
    url = 'https://www.curseforge.com/wow/addons/buffwatch-classic/files'
    print(get_curse(url))

    url = 'https://www.wowinterface.com/downloads/info24919-VuhDoClassic.html'
    print(get_wowi(url))

    github_addon_list = ('https://github.com/AeroScripts/QuestieDev',
                         'https://github.com/cannonpalms/FasterLooting',
                         'https://github.com/kesava-wow/kuinameplates2/tree/classic',
                         'https://github.com/shirsig/Cleanup',
                         'https://github.com/shirsig/SortBags/tree/retail',
                         'https://github.com/smp4903/FiveSecondRule/')

    url = 'https://github.com/cannonpalms/FasterLooting'
    for url in github_addon_list:
        print(get_github(url), '\n')
    '''
