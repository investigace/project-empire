#!/usr/bin/env python3

import argparse
from os import getenv
from os.path import join, dirname
from pprint import pprint

from dotenv import load_dotenv
from prompt_toolkit.shortcuts import confirm

import empire

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Push Empire spreadsheet data to Empire MediaWiki')
    parser.add_argument('--excel', help='Path to the Excel spreadsheet file with Empire database')
    args = parser.parse_args()

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Load data

    empire_data = empire.load_excel(args.excel)

    # Push to wiki

    wiki_url = getenv('WIKI_URL')
    wiki_username = getenv('WIKI_USERNAME')
    wiki_password = getenv('WIKI_PASSWORD')

    if wiki_url is None or wiki_username is None or wiki_password is None:
        print('Missing .env file with WIKI_URL, WIKI_USERNAME and WIKI_PASSWORD variables to use for connecting to MediaWiki. Please create .env file with mentioned variables.')
        exit(1)

    wiki = empire.MediaWiki(wiki_url, wiki_username, wiki_password)

    print('Preparing changes to be pushed...')

    changes = wiki.prepare_changes(empire_data)

    if not changes['pages']['create'] and not changes['pages']['update'] and not changes['pages']['delete']:
        print('Empire MediaWiki is in sync with the Empire spreadsheet, no changes to push were detected')
        exit(0)

    print('')
    print('Prepared following changes:')

    if changes['pages']['create']:
        print('')
        print('Pages to be created:')
        for page_create_change in changes['pages']['create']:
            print(f"  {page_create_change['name']}")

    if changes['pages']['update']:
        print('')
        print('Pages to be updated:')
        for page_update_change in changes['pages']['update']:
            print(f"  {page_update_change['name']}")

    if changes['pages']['delete']:
        print('')
        print('Pages to be deleted:')
        for page_delete_change in changes['pages']['delete']:
            print(f"  {page_delete_change['name']}")

    print('')
    answer = confirm("Are you sure you want to push these to Empire MediaWiki?")
    if answer != True:
        print('Ok, not pushing anything')
        exit(0)

    wiki.commit_changes(changes, 'Project Empire script push_spreadsheet_data_to_wiki.py')
