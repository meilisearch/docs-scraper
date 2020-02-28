

class Anchor:
    def __init__(self):
        pass

    @staticmethod
    def _get_anchor_string_from_element(element):
        return element.get('name', element.get('id'))

    @staticmethod
    def get_anchor(element):
        """
        Return a possible anchor for that element.
        Looks for name and id, and if not found will look in children
        """
        if isinstance(element, str):
            return None

        # Check the name or id on the element
        anchor = Anchor._get_anchor_string_from_element(element)

        if anchor is not None and anchor != '':
            return anchor

        # Check on child
        children = element.cssselect('[name],[id]')
        if len(children) > 0:
            return Anchor._get_anchor_string_from_element(children[-1])

        el = element

        while el is not None:
            # go back
            while el.getprevious() is not None:
                el = el.getprevious()

                if el is not None:
                    anchor = Anchor._get_anchor_string_from_element(el)

                    if anchor is not None:
                        return anchor

            # check last previous
            if el is not None:
                anchor = Anchor._get_anchor_string_from_element(el)

                if anchor is not None:
                    return anchor

            # go up
            el = el.getparent()

            if el is not None:
                anchor = Anchor._get_anchor_string_from_element(el)

                # check parent
                if anchor is not None:
                    return anchor

        # No more parent, we have no anchor
        return None
