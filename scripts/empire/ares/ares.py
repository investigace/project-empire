from .fetch_relationships import fetch_relationships
from .link_fetched_relationships import link_fetched_relationships


class Ares:
    def __init__(self):
        pass

    def fetch_relationships(self, legal_entities, cache_ares_xmls=False):
        return fetch_relationships(legal_entities, cache_ares_xmls)

    def link_fetched_relationships(self, current_empire_data, fetched_empire_data):
        return link_fetched_relationships(current_empire_data, fetched_empire_data)
