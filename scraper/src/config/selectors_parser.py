from ..helpers import css_to_xpath


class SelectorsParser:
    @staticmethod
    def _parse_selectors_set(config_selectors):
        selectors_set = {}
        for key in config_selectors:
            if key != 'text':
                selectors_set[key] = config_selectors[key]
            else:
                # Backward compatibility, rename text to content
                key = 'content'
                selectors_set[key] = config_selectors['text']

            # Backward compatibility, if it's a string then we put it in an object
            if isinstance(selectors_set[key], str):
                selectors_set[key] = {'selector': selectors_set[key]}

            # Global
            if 'global' in selectors_set[key]:
                selectors_set[key]['global'] = bool(
                    selectors_set[key]['global'])
            else:
                selectors_set[key]['global'] = False

            # Type
            if 'type' in selectors_set[key]:
                if selectors_set[key]['type'] not in ['xpath', 'css']:
                    raise Exception(
                        selectors_set[key][
                            'type'] + 'is not a good selector type, it should be `xpath` or `css`')
            else:
                selectors_set[key]['type'] = 'css'

            if selectors_set[key]['type'] == 'css':
                selectors_set[key]['selector'] = css_to_xpath(
                    selectors_set[key]['selector'])

            # We don't need it because everything is xpath now
            selectors_set[key].pop('type')

            # Default value
            selectors_set[key]['default_value'] = selectors_set[key][
                'default_value'] if 'default_value' in \
                                    selectors_set[
                                        key] else None

            # Strip chars
            selectors_set[key]['strip_chars'] = selectors_set[key][
                'strip_chars'] if 'strip_chars' in selectors_set[
                key] else None

            if 'attributes' in selectors_set[key]:
                selectors_set[key][
                    'attributes'] = SelectorsParser._parse_selectors_set(
                    selectors_set[key]['attributes'])

        return selectors_set

    def parse(self, config_selectors):
        selectors = {}

        if 'lvl0' in config_selectors:
            config_selectors = {'default': config_selectors}

        for selectors_key in config_selectors:
            selectors[selectors_key] = self._parse_selectors_set(
                config_selectors[selectors_key])

        return selectors

    @staticmethod
    def parse_min_indexed_level(min_indexed_level):
        min_indexed_level_object = min_indexed_level
        if isinstance(min_indexed_level, int):
            min_indexed_level_object = {
                'default': min_indexed_level_object
            }

        return min_indexed_level_object
