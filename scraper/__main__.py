"""Main module

Permits:

"""
import os
from scraper.src.index import run_config
import argparse

def main(sys_args=None):
    """ Supports calling gui directly with command line arguments """

    parser = argparse.ArgumentParser(
        description='Scrape documentation.'
    )
    parser.add_argument(
        'config_file', type=str, help='The path to the configuration file.'
    )

    parser.add_argument(
        '--meilisearch-host-url', type=str,
        required=False,
        help='The URL to the meilisearch host',
    )

    parser.add_argument(
        '--meilisearch-api-key', type=str,
        required=False,
        help='The URL to the meilisearch host',
    )

    parser.add_argument(
        '--cname', type=str,
        required=False,
        help='The CNAME of the webpage',
    )

    parser.add_argument(
        '--port', type=str,
        required=False,
        help='The port where local HTML files are served.',
    )

    args = parser.parse_args()

    if args.meilisearch_host_url is not None:
        os.environ['MEILISEARCH_HOST_URL'] = args.meilisearch_host_url
    if args.meilisearch_api_key is not None:
        os.environ['MEILISEARCH_API_KEY'] = args.meilisearch_api_key
    if args.cname is not None:
        os.environ['DOCUMENTATION_CNAME'] = args.cname
    if args.port is not None:
        os.environ['DOCUMENTATION_PORT'] = args.port

    if 'MEILISEARCH_HOST_URL' not in os.environ:
        raise RuntimeError(
            '\n\nMEILISEARCH_HOST_URL is required either the command line argument:'
            '\n\n    --meilisearch-host-url <URL>\n\n'
            'or as the environment variable "MEILISEARCH_HOST_URL"'
        )

    if 'MEILISEARCH_API_KEY' not in os.environ:
        raise RuntimeError(
            '\n\nMEILISEARCH_API_KEY is required either the command line argument:'
            '\n\n    --meilisearch-api-key <URL>\n\n'
            'or as the environment variable "MEILISEARCH_API_KEY"'
        )

    run_config(args.config_file)


if __name__ == '__main__':
    main()
