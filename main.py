#main.py
"""
Action script to select a random quote/fun-fact and put it on given repository's README.
"""

import os
import re
import sys
import random
import base64
from typing import List
from github import Github, GithubException

STARTS_WITH = "<!--STARTS_HERE_QUOTE_README-->"
ENDS_WITH = "<!--ENDS_HERE_QUOTE_README-->"
REPL_PATTERN = f"{STARTS_WITH}[\\s\\S]+{ENDS_WITH}"

REPOSITORY = os.getenv("INPUT_REPOSITORY")
GH_TOKEN = os.getenv("INPUT_GH_TOKEN")
COMMIT_MSG = os.getenv("INPUT_COMMIT_MESSAGE")
OPTION = os.getenv("INPUT_OPTION")

QUOTES_PATH = "/quotes/quotes.txt"
FUNFACTS_PATH = "/funfacts/funfacts.txt"


def get_quotes() -> List[str]:
    """
    Get quotes from quotes/quotes.txt, return a list.
    """
    global QUOTES_PATH
    quotes = []
    with open(QUOTES_PATH, "r") as file:
        quotes.extend(file.readlines())
    random.shuffle(quotes)
    return quotes


def get_funfacts() -> List[str]:
    """
    Get funfacts from funfacts/funfacts.txt, return a list.
    """
    global FUNFACTS_PATH
    funfacts = []
    with open(FUNFACTS_PATH, "r") as file:
        funfacts.extend(file.readlines())
    random.shuffle(funfacts)
    return funfacts


def get_option_list(OPTION):
    """
    Utility to get text list for corresponding given option.
    """
    text_list = []
    if OPTION == 'quote':
        text_list.extend(get_quotes())
    elif OPTION == 'funfact':
        text_list.extend(get_funfacts())
    elif OPTION == 'both':
        text_list.extend(get_quotes())
        text_list.extend(get_funfacts())
        random.shuffle(text_list)
    return text_list


def get_quote_funfact(text_list: List[str]) -> str:
    """
    Utility to get random text from given list.
    """
    return random.choice(text_list)


def get_text_to_display() -> str:
    """
    Get text to display on readme, depending on option.
    """
    global OPTION
    text_list = get_option_list(OPTION)
    text_to_display = get_quote_funfact(text_list)
    text_to_display = re.sub('[\n]', '', text_to_display)
    text_to_display = re.sub('[\xa0]', ' ', text_to_display)
    text_to_display = f"<i>❝{text_to_display}❞</i>"
    return text_to_display


def decode_readme(data: str) -> str:
    """
    Decode the contents of old readme.
    """
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, 'utf-8')


def generate_new_readme(readme: str, i_tag: str) -> str:
    """
    Generate a new Readme.
    """
    update_readme_with = f"{STARTS_WITH}\n{i_tag}\n{ENDS_WITH}"
    return re.sub(REPL_PATTERN, update_readme_with, readme)


if __name__ == "__main__":
    g = Github(GH_TOKEN)
    try:
        readme_repo = g.get_repo(REPOSITORY)
    except GithubException:
        print("Authentication Error. Try saving a GitHub Token in your Repo Secrets or Use the GitHub Actions Token, which is automatically used by the action.")
        sys.exit(1)
    text_to_display = get_text_to_display()
    readme_obj = readme_repo.get_readme()
    readme_content = readme_obj.content
    readme_content_decoded = decode_readme(readme_content)
    new_readme = generate_new_readme(readme=readme_content_decoded, i_tag=text_to_display)
    if readme_content_decoded != new_readme:
        readme_repo.update_file(path=readme_obj.path, message=COMMIT_MSG,
                             content=new_readme, sha=readme_obj.sha)
        print("Success")
    else:
        print('No change')
