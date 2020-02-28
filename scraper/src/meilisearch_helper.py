"""MeiliSearchHelper
Wrapper on top of the AlgoliaSearch API client"""

import time
import meilisearch
from builtins import range

def clean_one_field(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value)
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

    # Go to the end of this file to understand criteria order
    SETTINGS = {
        "rankingOrder": [
            "_number_of_words",
            "_sum_of_typos",
            "_sum_of_words_attribute",
            "_word_proximity",
            "_exact",
            "page_rank",
            "level",
            "position"
        ],
        "distinctField": "url",
        "rankingRules": {
            "page_rank": "dsc",
            "level": "dsc",
            "position": "asc"
        }
    }

    def __init__(self, app_id, api_key, index_uid):
        self.meilisearch_client = meilisearch.Client("https://" + app_id + ".getmeili.com" , api_key)
        self.index_uid = index_uid
        self.meilisearch_index = self.meilisearch_client.get_index(self.index_uid)
        self.meilisearch_index.add_settings(MeiliSearchHelper.SETTINGS)
        self.schema_added = False
        if len(self.meilisearch_index.get_documents({"limit": 10})) != 0:
            print('Schema already added')
            self.schema_added = True
        self.meilisearch_index.delete_all_documents()

    def add_records(self, records, url, from_sitemap):
        """Add new records to the temporary index"""

        record_count = len(records)
        for i in range(0, record_count, 50):
            parsed_records = list(map(parse_record, records[i:i + 50]))
            if self.schema_added == False:
                print('Updating schema...')
                self.update_schema_based_on(parsed_records[i])
                self.schema_added = True
            cleaned_records = list(map(clean_dict, parsed_records))
            self.meilisearch_index.add_documents(cleaned_records)

        color = "96" if from_sitemap else "94"

        print(
            '\033[{}m> DocSearch: \033[0m{}\033[93m {} records\033[0m)'.format(
                color, url, record_count))

    def update_schema_based_on(self, record):
        base_schema = {
            'anchor':    ['displayed'],
            'url':       ['displayed'],
            'content':   ['indexed', 'displayed'],
            'objectID':  ['identifier', 'indexed', 'displayed'],
            'page_rank': ['indexed', 'ranked'],
            'level':     ['indexed', 'ranked'],
            'position':  ['indexed', 'ranked']
        }
        hierarchy_radio_schema = {}
        hierarchy_schema = {}
        for k, v in record.items():
            if k.startswith('hierarchy_radio_'):
                hierarchy_radio_schema[k] = ['indexed']
            elif k.startswith('hierarchy_'):
                hierarchy_schema[k] = ['indexed', 'displayed']
        schema = {**hierarchy_radio_schema, **hierarchy_schema, **base_schema}
        self.meilisearch_index.update_schema(schema)

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
