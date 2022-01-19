from copy import deepcopy
from pprint import pprint
from urllib.parse import urlparse

import enlighten
import mwclient

from .legal_entities import prepare_legal_entities_changes
from .people import prepare_people_changes
from .summary import prepare_summary_changes


class MediaWiki:
    def __init__(self, wiki_url, wiki_username, wiki_password):
        url_parsed = urlparse(wiki_url)

        self.site = mwclient.Site(
            url_parsed.netloc, path='/', scheme=url_parsed.scheme)
        self.site.login(wiki_username, wiki_password)

        # Detect MediaWiki language
        siteinfo = self.site.raw_api(action='query', meta='siteinfo')
        self.lang = siteinfo['query']['general']['lang']

    def prepare_changes(self, empire_data):
        changes = {
            'pages': {
                'create': [],
                'update': [],
                'delete': []
            },
            'categories': {
                'create': [],
                'update': [],
                'delete': []
            }
        }

        changes = self._merge_changes(
            changes, prepare_legal_entities_changes(self, empire_data))
        changes = self._merge_changes(
            changes, prepare_people_changes(self, empire_data))
        changes = self._merge_changes(
            changes, prepare_summary_changes(self, empire_data))

        return changes

    def commit_changes(self, changes, change_message):
        total = 0
        if 'pages' in changes:
            if 'create' in changes['pages']:
                total += len(changes['pages']['create'])
            if 'update' in changes['pages']:
                total += len(changes['pages']['update'])
            if 'delete' in changes['pages']:
                total += len(changes['pages']['delete'])

        progress_bar = enlighten.Counter(
            total=total, desc='Pushing changes to Empire MediaWiki', unit='changes')

        if 'pages' in changes and 'create' in changes['pages']:
            for create_change in changes['pages']['create']:
                page = self.site.pages[create_change['name']]

                page.edit(create_change['content_change'], change_message)

                progress_bar.update()

        if 'pages' in changes and 'update' in changes['pages']:
            for update_change in changes['pages']['update']:
                page = self.site.pages[update_change['name']]

                page.edit(update_change['content_change'], change_message)

                progress_bar.update()

        if 'pages' in changes and 'delete' in changes['pages']:
            for delete_change in changes['pages']['delete']:
                page = self.site.pages[delete_change['name']]

                page.delete(change_message)

                progress_bar.update()

    def _merge_changes(self, changes_a, changes_b):
        result = deepcopy(changes_a)

        for entity_type, entity_type_changes in result.items():
            for change_type, changes in entity_type_changes.items():
                if entity_type in changes_b and change_type in changes_b[entity_type]:
                    result[entity_type][change_type] = result[entity_type][change_type] + \
                        changes_b[entity_type][change_type]

        return result
