from . import algolia_helper, fetchers


def _is_automatically_updated(config, attribute):
    for start_url in config['start_urls']:
        if not isinstance(start_url, str):
            if 'variables' in start_url:
                for variable in start_url['variables']:
                    if (variable == attribute):
                        if not isinstance(start_url['variables'][variable],
                                          list):
                            return True
    return False


def get_email_for_config(config, analytics_statuses=None):
    base_template = """Hi there,

Congratulations, your search is now ready!
I've successfully configured the underlying crawler and it will now run every 24h.

You're now a few steps away from having it working on your website:

- Copy the following CSS/JS snippets and add them to your page

<!-- at the end of the HEAD -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsearch.js@2/dist/cdn/docsearch.min.css" />

<!-- at the end of the BODY -->
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/docsearch.js@2/dist/cdn/docsearch.min.js"></script>
<script type="text/javascript"> docsearch({
  apiKey: '{{API_KEY}}',
  indexName: '{{INDEX_NAME}}',
  inputSelector: '### REPLACE ME ####'{{ALGOLIA_OPTIONS}},
  debug: false // Set debug to true if you want to inspect the dropdown
});
</script>

- Add a search input in your page if you don't have any yet. Then update the inputSelector value in JS snippet
  to a CSS selector that targets your search input field.{{FACETS}}
- Optionally customize the look and feel by following the DocSearch documentation
  (See https://community.algolia.com/docsearch/styling.html)
- You can also check your configuration in our GitHub repository
  (See https://github.com/algolia/docsearch-configs/blob/master/configs/{{INDEX_NAME}}.json).
{{ANALYTICS}}
Please open a pull request if want to leverage your configuration!

Feel free to get back to us if you have any issues or questions regarding the integration.

We'd also be happy to get your feedback and thoughts about DocSearch - so we can continue to improve it.

Have a nice day :)"""

    base_facet_template = """\n- Replace ${{CAPITALISE_NAME}} with the {{NAME}} you want to search on.
   The list of possible {{NAME}} {{UPDATED}}.
   So as of today you have: {{VALUES}}\n"""

    base_example_template = """
  For example if you want to refine the search to {{EXAMPLE_PHRASE}} just specify: 'facetFilters': [{{EXAMPLE_CODE}}]
"""

    # Let the user know how they can access their Analytics
    analytics_details = ''
    if isinstance(analytics_statuses, dict):
        for email, analytics_status in list(analytics_statuses.items()):
            analytics_details += '- ' + email
            if isinstance(analytics_status, str):
                analytics_details += '''\
 can get access to the full Algolia analytics for your DocSearch index by creating an account,\
 following this link: ''' + analytics_status + '\n'
            else:
                analytics_details += '''\
 has already an Algolia account. Analytics available from the Algolia dashboard by selecting\
 the application DOCSEARCH (access granted)'''

    facets = algolia_helper.get_facets(config)

    facet_template = ""
    algolia_options = ""

    if facets is not None:
        facet_template = "\n"
        configs = fetchers.get_configs_from_repos()

        example_phrase = []
        example_code = []
        example_options = []

        for name, values in list(facets.items()):
            if name == "no_variables":
                continue
            keys = list(values.keys())
            keys.sort()

            if len(keys) > 0:
                updated = "is automatically fetched from your website" if _is_automatically_updated(
                    configs[config],
                    name) else "is hardcoded in the config"
                facet_template += base_facet_template.replace('{{NAME}}', name) \
                    .replace('{{CAPITALISE_NAME}}', name.upper()) \
                    .replace("{{UPDATED}}", updated) \
                    .replace("{{VALUES}}", ', '.join(keys))

                example_phrase.append('the ' + name + ' "' + keys[0] + '"')
                example_code.append("\"" + name + ":" + keys[0] + "\"")
                example_options.append(
                    "\"" + name + ":$" + name.upper() + "\"")

        if len(example_options) > 0:
            algolia_options += ",\n  algoliaOptions: { 'facetFilters': [" + (
                ', '.join(example_options)) + "] }"
            facet_template += base_example_template.replace(
                '{{EXAMPLE_PHRASE}}', ' and '.join(example_phrase)) \
                .replace('{{EXAMPLE_CODE}}', ', '.join(example_code))

        if facet_template == "\n":
            facet_template = ""

    api_key = algolia_helper.get_docsearch_key(config)
    api_key = "### REPLACE ME ####" if api_key == 'Not found' else api_key

    template = base_template.replace('{{API_KEY}}', api_key) \
        .replace('{{INDEX_NAME}}', config) \
        .replace('{{FACETS}}', facet_template) \
        .replace('{{ALGOLIA_OPTIONS}}', algolia_options) \
        .replace('{{ANALYTICS}}', analytics_details)

    return template
