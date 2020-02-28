import os
import re
import html

from helpscout.client import HelpScout


def get_helpscout_app_id():
    hs_api_id = os.environ.get('HELPSCOUT_APP_ID')

    if not hs_api_id:
        raise ValueError("None HELPSCOUT_APP_ID from environment variables")

    return hs_api_id


def get_helpscout_app_secret():
    hs_api_secret = os.environ.get('HELPSCOUT_APP_SECRET')

    if not hs_api_secret:
        raise ValueError(
            "None HELPSCOUT_APP_SECRET from environment variables")

    return hs_api_secret


def is_helpdesk_url(u):
    return 'secure.helpscout.net/conversation' in u


def get_conversation_ID_from_url(hs_url):
    capture_conversation_uid = re.compile(r'.+/conversation/(\d+)/.*')

    conversation_uid_match = capture_conversation_uid.match(hs_url)

    # Handle URL that are build without the tailing /
    if conversation_uid_match is None:
        capture_conversation_uid = re.compile(r'.+/conversation/(\d+)')
        conversation_uid_match = capture_conversation_uid.match(hs_url)
        cuid = conversation_uid_match.group(1)

    else:
        cuid = conversation_uid_match.group(1)

    if not len(cuid) > 0 or cuid is None:
        raise ValueError(
            'Wrong help scout url {}, must have a conversation sub part with ID'.format(
                hs_url))

    if not RepresentsInt(cuid):
        raise ValueError(
            'Conversation ID : {} must be an integer'.format(cuid))

    return cuid


def get_conversation(cuid, params=None):
    app_id = get_helpscout_app_id()
    app_secret = get_helpscout_app_secret()
    hs = HelpScout(app_id, app_secret)
    conversation = hs.conversations.get(params=params, resource_id=cuid)

    if not conversation:
        raise ValueError(
            "Wrong json returned from help scout, must have an item attribute")

    return conversation


def get_conversation_with_threads(cuid):
    return get_conversation(cuid, params='embed=threads')


def get_start_url_from_conversation(conversation_with_threads):
    embedded_conversation = conversation_with_threads._embedded
    if not embedded_conversation or not embedded_conversation["threads"][-1]:
        raise ValueError(
            "Wrong input conversation, must be not evaluate at None and have at least one thread")

    # The message to extract is the first from the thread and it was sent by a customer
    first_thread = embedded_conversation["threads"][-1]
    was_sent_by_customer = first_thread['createdBy']['type'] == 'customer'
    url_from_conversation = first_thread['body']

    if not len(url_from_conversation):
        raise ValueError("First thread from the conversation thread is empty")

    if not was_sent_by_customer:
        raise ValueError(
            "First thread from the conversation thread wasn't sent by customer")

    print(
        'URL fetched is \033[1;36m{}\033[0m sent by \033[1;33m{}\033[0m'.format(
            url_from_conversation, first_thread["customer"]["email"]))

    return url_from_conversation


def get_emails_from_conversation(conversation_with_threads):
    emails = []

    embedded_conversation = conversation_with_threads._embedded
    if not conversation_with_threads or not embedded_conversation["threads"][-1]:
        raise ValueError(
            "Wrong input conversation, must be not evaluate at None and have at least one thread")

    # Extract customer
    first_thread = embedded_conversation["threads"][-1]
    customer = first_thread['customer']
    customers_mail = customer['email']
    was_sent_by_customer = first_thread['createdBy']['type'] == 'customer'

    if not was_sent_by_customer:
        raise ValueError(
            "First thread from the conversation thread wasn't sent by customer")

    emails.append(customers_mail)

    cc = first_thread['cc']
    if cc:
        emails = emails + cc

    bcc = first_thread['bcc']
    if bcc:
        emails = emails + bcc

    if len(emails) > 1:
        print(
            "Conversation sent by \033[1;33m" + customers_mail + "\033[0m" + (
                " with " + " ".join(emails[1:])))

    return emails


def add_note(cuid, body):
    app_id = get_helpscout_app_id()
    app_secret = get_helpscout_app_secret()
    hs = HelpScout(app_id, app_secret)

    # Inserting HTML code into HTML mail, snippet need to be HTML escaped
    body = html.escape(body)

    data = {"text": body}
    hs.conversations[cuid].notes.post(data=data)

    return True


def get_conversation_url_from_cuid(cuid):
    if not cuid:
        raise ValueError("Wrong input conversation ID")

    return 'https://secure.helpscout.net/conversation/{}'.format(cuid)


def check_if_is_tag(tag, ref_tag):
    '''
        Check if a tag is a ref_tag
    '''
    return tag["tag"] == ref_tag


def check_if_has_tag(conversation, ref_tags):
    '''
            Check if the conversation has one tag from ref_tags
    '''
    for ref_tag in ref_tags:
        if any(check_if_is_tag(tag, ref_tag) for tag in conversation.tags):
            return True


def is_docusaurus_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["docusaurus", "ds_docusaurus",
                             "gen-docusaurus"])


def is_docusaurus_v2_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["docusaurus_v2", "ds_docusaurus_v2",
                             "gen-docusaurus_v2"])


def is_gitbook_conversation(conversation):
    return check_if_has_tag(conversation, ["gitbook"])


def is_pkgdown_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["pkgdown", "ds_pkgdown", "gen-pkgdown"])


def is_vuepress_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["vuepress", "ds_vuepress", "gen-vuepress"])


def is_larecipe_conversation(conversation):
    return check_if_has_tag(conversation, ["larecipe"])


def is_publii_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["publii", "ds_publii", "gen-publii"])


def is_jsdoc_conversation(conversation):
    return check_if_has_tag(conversation,
                            ["jsdoc", "ds_jsdoc", "gen-jsdoc"])


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
