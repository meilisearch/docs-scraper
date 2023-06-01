"""MeiliSearchHelper
Wrapper on top of the Meilisearch API client"""

import meilisearch
from builtins import range

from .config.version import qualified_version

def remove_bad_encoding(value):
    return value.replace('&#x27;', "'")

def clean_one_field(value):
    if isinstance(value, bool):
        return str(value)
    elif isinstance(value, str):
        return remove_bad_encoding(value)
    return value

def clean_dict(record):
    for key, value in record.items():
        if isinstance(value, dict):
            record[key] = clean_dict(value)
        else:
            record[key] = clean_one_field(value)
    return record

def parse_record(record):
    new_weight = {}
    for k, v in record['weight'].items():
        new_weight[k] = v
    new_hierarchy = {}
    for k, v in record['hierarchy'].items():
        new_hierarchy['hierarchy_' + k] = v
    new_hierarchy_radio = {}
    for k, v in record['hierarchy_radio'].items():
        key = 'hierarchy_radio_' + k
        new_hierarchy_radio = {**{key: v}, **new_hierarchy_radio}
    del record['weight']
    del record['hierarchy']
    del record['hierarchy_radio']
    del record['hierarchy_camel']
    del record['hierarchy_radio_camel']
    del record['content_camel']
    return {**record, **new_weight, **new_hierarchy, **new_hierarchy_radio}

class MeiliSearchHelper:
    """MeiliSearchHelper"""

    # Cf the end of this file to understand these settings
    SETTINGS = {
        'rankingRules': [
            'words',
            'typo',
            'attribute',
            'proximity',
            'exactness',
            'page_rank:desc',
            'level:desc',
            'position:asc'
        ],
        'distinctAttribute': 'url',
        'searchableAttributes': [
            'hierarchy_radio_lvl0',
            'hierarchy_radio_lvl1',
            'hierarchy_radio_lvl2',
            'hierarchy_radio_lvl3',
            'hierarchy_radio_lvl4',
            'hierarchy_radio_lvl5',
            'hierarchy_lvl0',
            'hierarchy_lvl1',
            'hierarchy_lvl2',
            'hierarchy_lvl3',
            'hierarchy_lvl4',
            'hierarchy_lvl5',
            'hierarchy_lvl6',
            'content',
            'objectID',
            'page_rank',
            'level',
            'position'
        ],
        'displayedAttributes': [
            'hierarchy_radio_lvl0',
            'hierarchy_radio_lvl1',
            'hierarchy_radio_lvl2',
            'hierarchy_radio_lvl3',
            'hierarchy_radio_lvl4',
            'hierarchy_radio_lvl5',
            'hierarchy_lvl0',
            'hierarchy_lvl1',
            'hierarchy_lvl2',
            'hierarchy_lvl3',
            'hierarchy_lvl4',
            'hierarchy_lvl5',
            'hierarchy_lvl6',
            'anchor',
            'url',
            'content',
            'objectID'
        ]
    }

    def __init__(self, host_url, api_key, index_uid, custom_settings):
        self.meilisearch_client = meilisearch.Client(host_url, api_key, client_agents=(qualified_version(),))
        self.meilisearch_index = self.meilisearch_client.index(index_uid)
        self.delete_index()
        self.add_settings(MeiliSearchHelper.SETTINGS, custom_settings)

    def add_settings(self, default_settings, custom_settings):
        settings = {**default_settings, **custom_settings}
        self.meilisearch_index.update_settings(settings)

    def delete_index(self):
        self.meilisearch_index.delete()

    def add_records(self, records, url, from_sitemap):
        """Add new records to the index"""

        record_count = len(records)
        for i in range(0, record_count, 50):
            parsed_records = list(map(parse_record, records[i:i + 50]))
            cleaned_records = list(map(clean_dict, parsed_records))
            self.meilisearch_index.add_documents(cleaned_records)

        color = "96" if from_sitemap else "94"

        print(
            f'\033[{color}m> Docs-Scraper: \033[0m{url}\033[93m {record_count} records\033[0m)')

# Algolia's settings:
    # {"minWordSizefor1Typo"=>3,
    # "minWordSizefor2Typos"=>7,
    # "hitsPerPage"=>20,
    # "maxValuesPerFacet"=>100,
    # "minProximity"=>1,
    # "version"=>2,
    # "attributesToIndex"=>
    # ["unordered(hierarchy_radio_camel.lvl0)",
    # "unordered(hierarchy_radio.lvl0)",
    # "unordered(hierarchy_radio_camel.lvl1)",
    # "unordered(hierarchy_radio.lvl1)",
    # "unordered(hierarchy_radio_camel.lvl2)",
    # "unordered(hierarchy_radio.lvl2)",
    # "unordered(hierarchy_radio_camel.lvl3)",
    # "unordered(hierarchy_radio.lvl3)",
    # "unordered(hierarchy_radio_camel.lvl4)",
    # "unordered(hierarchy_radio.lvl4)",
    # "unordered(hierarchy_radio_camel.lvl5)",
    # "unordered(hierarchy_radio.lvl5)",
    # "unordered(hierarchy_camel.lvl0)",
    # "unordered(hierarchy.lvl0)",
    # "unordered(hierarchy_camel.lvl1)",
    # "unordered(hierarchy.lvl1)",
    # "unordered(hierarchy_camel.lvl2)",
    # "unordered(hierarchy.lvl2)",
    # "unordered(hierarchy_camel.lvl3)",
    # "unordered(hierarchy.lvl3)",
    # "unordered(hierarchy_camel.lvl4)",
    # "unordered(hierarchy.lvl4)",
    # "unordered(hierarchy_camel.lvl5)",
    # "unordered(hierarchy.lvl5)",
    # "content"],
    # "numericAttributesToIndex"=>nil,
    # "attributesToRetrieve"=>["hierarchy", "content", "anchor", "url"],
    # "allowTyposOnNumericTokens"=>false,
    # "ignorePlurals"=>true,
    # "camelCaseAttributes"=>["hierarchy", "hierarchy_radio", "content"],
    # "advancedSyntax"=>true,
    # "attributeCriteriaComputedByMinProximity"=>true,
    # "distinct"=>true,
    # "unretrievableAttributes"=>nil,
    # "optionalWords"=>nil,
    # "userData"=>{"crawling_issue"=>false},
    # "attributesForFaceting"=>["lang"],
    # "attributesToSnippet"=>["content:10"],
    # "attributesToHighlight"=>["hierarchy", "hierarchy_camel", "content"],
    # "paginationLimitedTo"=>1000,
    # "attributeForDistinct"=>"url",
    # "exactOnSingleWordQuery"=>"attribute",
    # "ranking"=>
    # ["words", "filters", "typo", "attribute", "proximity", "exact", "custom"],
    # "customRanking"=>
    # ["desc(weight.page_rank)", "desc(weight.level)", "asc(weight.position)"],
    # "separatorsToIndex"=>"",
    # "removeWordsIfNoResults"=>"allOptional",
    # "queryType"=>"prefixLast",
    # "highlightPreTag"=>"<span class=\"algolia-docsearch-suggestion--highlight\">",
    # "highlightPostTag"=>"</span>",
    # "snippetEllipsisText"=>"",
    # "alternativesAsExact"=>["ignorePlurals", "singleWordSynonym"]}
