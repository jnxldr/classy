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
            last_upload = stored_addon_info[4]
            domain_extract = tldextract.extract(url).domain

            if domain_extract in 'curseforge':
                live_addon_info = get_curse(url)
                if live_addon_info[1] != last_upload:
                    print('Name: ', live_addon_info[0])
                    # print('Current Version: ', live_addon_info[1]) # Omitted until storing version in Sheets
                    print('Current Upload Date: ', live_addon_info[1])
                    print('Stored Upload Date: ', last_upload)
                    print('Addon Page: ', url)
                    print('Direct Download: ', live_addon_info[2], '\n')

            elif domain_extract in 'wowinterface':
                live_addon_info = get_wowi(url)
                if live_addon_info[1] != last_upload:
                    print('Name: ', live_addon_info[0])
                    # print('Current Version: ', live_addon_info[1]) # Omitted until storing version in Sheets
                    print('Current Upload Date: ', live_addon_info[1])
                    print('Stored Upload Date: ', last_upload)
                    print('Addon Page: ', url)
                    print('Direct Download: ', live_addon_info[2], '\n')

            elif domain_extract in 'github':
                live_addon_info = get_github(url)
                if live_addon_info[1] != last_upload:
                    print('Name: ', live_addon_info[0])  # Different index  for github as I don't return the version
                    print('Current Upload Date: ', live_addon_info[1])
                    print('Stored Upload Date: ', last_upload)
                    print('Addon Page: ', url)
                    print('Direct Download: ', live_addon_info[2], '\n')
                pass
            else:
                pass

    print('Done checking the spreadsheet.')


if __name__ == '__main__':
    main()
