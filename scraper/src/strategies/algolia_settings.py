class AlgoliaSettings:
    def __init__(self):
        pass

    @staticmethod
    def get(config, levels):
        attributes_to_index = []

        # We first look for matches in the exact titles
        for level in levels:
            for selectors_key in config.selectors:
                attr_to_index = 'unordered(hierarchy_radio.' + level + ')'
                if level in config.selectors[
                    selectors_key] and attr_to_index not in attributes_to_index:
                    attributes_to_index.append(
                        'unordered(hierarchy_radio_camel.' + level + ')')
                    attributes_to_index.append(attr_to_index)

        # Then in the whole title hierarchy
        for level in levels:
            for selectors_key in config.selectors:
                attr_to_index = 'unordered(hierarchy.' + level + ')'
                if level in config.selectors[
                    selectors_key] and attr_to_index not in attributes_to_index:
                    attributes_to_index.append(
                        'unordered(hierarchy_camel.' + level + ')')
                    attributes_to_index.append(attr_to_index)

        for selectors_key in config.selectors:
            if 'content' in config.selectors[
                selectors_key] and 'content' not in attributes_to_index:
                attributes_to_index.append('content')

        settings = {
            'attributesToIndex': attributes_to_index,
            'attributesToRetrieve': [
                'hierarchy',
                'content',
                'anchor',
                'url'
            ],
            'attributesToHighlight': [
                'hierarchy',
                'hierarchy_camel',
                'content'
            ],
            'attributesToSnippet': [
                'content:10'
            ],
            'camelCaseAttributes': [
                'hierarchy',
                'hierarchy_radio',
                'content'
            ],
            'attributesForFaceting': ['tags', 'no_variables',
                                      'extra_attributes'] + config.get_extra_facets(),
            'distinct': True,
            'attributeForDistinct': 'url',
            'customRanking': [
                'desc(weight.page_rank)',
                'desc(weight.level)',
                'asc(weight.position)'
            ],
            # Default ranking is: typo, geo, words, proximity, attribute, exact, custom
            # - We removed geo as this is irrelevant
            # - We moved words before typo, because in case of a documentation
            #   search you have no idea where your matching words will be (not
            #   necessarily at the start)
            # - For the same reason, we put proximity lower and gave more weight
            #   to attribute
            'ranking': [
                'words',
                'filters',
                'typo',
                'attribute',
                'proximity',
                'exact',
                'custom'
            ],
            'highlightPreTag': '<span class="algolia-docsearch-suggestion--highlight">',
            'highlightPostTag': '</span>',
            'minWordSizefor1Typo': 3,
            'minWordSizefor2Typos': 7,
            'allowTyposOnNumericTokens': False,
            'minProximity': 1,
            'ignorePlurals': True,
            'advancedSyntax': True,
            'attributeCriteriaComputedByMinProximity': True,
            'removeWordsIfNoResults': 'allOptional',
            'userData': {
                'crawling_issue': False
            }
        }
        # apply custom updates
        if config.custom_settings is not None:
            settings.update(config.custom_settings)

        return settings
