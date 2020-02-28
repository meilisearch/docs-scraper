class Hierarchy:
    def __init__(self):
        pass

    @staticmethod
    def get_hierarchy_radio(hierarchy, current_level, levels):
        """Returns the radio hierarchy for the record, where only one level is
        filled and the others are empty
        Ex: {
            lvl0: None,
            lvl1: None,
            lvl2: Baz,
            lvl3: None,
            lvl4: None,
            lvl5: None,
            lvl6: None
        }
        """

        hierarchy_radio = {}
        is_found = False
        for level in reversed(levels):
            if level == 'content':
                continue

            value = hierarchy[level]
            if is_found is False and value is not None and current_level != 'content':
                is_found = True
                hierarchy_radio[level] = value
                continue

            hierarchy_radio[level] = None

        return hierarchy_radio
