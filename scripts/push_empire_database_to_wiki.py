#!/usr/bin/env python3

import argparse
from os import getenv
from os.path import join, dirname
from pprint import pprint
import re
import sys

from prompt_toolkit.shortcuts import confirm, prompt

import empire

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Push Empire database data to Empire wiki')
    parser.add_argument(
        'database_excel',
        metavar="DATABASE_EXCEL",
        help='Path to the Excel spreadsheet file with Empire database'
    )
    parser.add_argument(
        'wiki',
        metavar="WIKI",
        help='Domain or full URL of Empire wiki, e.g. https://empirewiki.example.org/'
    )
    parser.add_argument(
        'wiki_user',
        metavar="WIKI_USER",
        help='Username to use for login to Empire wiki'
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    wiki_url = args.wiki
    wiki_user = args.wiki_user

    # If the wiki argument does not contain scheme, we expect that it is just domain
    # using HTTPS.
    if not re.compile(r'(http://|https://)').search(wiki_url):
        wiki_url = f'https://{wiki_url}/'

    wiki_password = prompt(
        message=f'Password for user {wiki_user} at Empire wiki {wiki_url}: ',
        is_password=True
    )

    # Load data

    empire_data = empire.load_excel(args.database_excel)

    print(f"Loaded Empire database: {len(empire_data['legal_entities'])} legal entities, {len(empire_data['people'])} people, {len(empire_data['subsidies'])} subsidies")

    # Push to wiki

    wiki = empire.MediaWiki(wiki_url, wiki_user, wiki_password)
    
    print('Connected to Empire wiki')
    print('Preparing changes to be pushed...')

    changes = wiki.prepare_changes(empire_data)

    if not changes['pages']['create'] and not changes['pages']['update'] and not changes['pages']['delete']:
        print('Empire wiki is in sync with the Empire database Excel spreadsheet, no changes to be pushed were detected')
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

    wiki.commit_changes(changes, 'Project Empire script push_empire_database_to_wiki.py')
