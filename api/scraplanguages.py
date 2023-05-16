import requests
from bs4 import BeautifulSoup


MAIN_URL = 'https://en.wikipedia.org/wiki/List_of_programming_languages'


def get_languages(URL: str = MAIN_URL) -> list[str]:
    """
    Get all programming languages from Wikipedia

    Args:
        URL: The URL to get content from

    Returns:
        list[str]: List of programming languages found on the wikipedia page

    """
    page_content = _get_page_content(URL)
    main_div, content_div = _find_divs(page_content)
    languages = _get_languages_values(content_div)

    return languages


def _get_page_content(URL: str) -> BeautifulSoup:
    """
    Get page content from a given URL

    Args:
        URL: The URL to get content from

    Returns:
        BeautifulSoup: Parsed HTML content of the Wikipedia page

    Raises:
        HTTPError: If the request to the URL fails

    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        raise
    else:
        return BeautifulSoup(response.text, 'html.parser')


def _find_divs(page_content: BeautifulSoup) -> tuple[BeautifulSoup, BeautifulSoup]:
    """
    Find the main div and the content div in the page content

    Args:
        page_content: The parsed HTML content of the Wikipedia page

    Returns:
        tuple[BeautifulSoup, BeautifulSoup]: The main div and the content div

    Raises:
        ValueError: If the main div or the content div cannot be found
    """
    main_div = page_content.find("div", id='mw-content-text')
    if main_div is None:
        raise ValueError("Could not find the main div")

    content_div = main_div.find("div", class_='mw-parser-output')
    if content_div is None:
        raise ValueError("Could not find the content div")

    return main_div, content_div


def _get_languages_values(content_div: BeautifulSoup) -> list[str]:
    """
    Get the values of the languages from the div containing the languages

    Args:
        content_div: The content of the div containing the languages

    Returns:
        list[str]: List of programming languages
    """
    languages = []
    languages_elements = content_div.select('div.div-col li a')
    for element in languages_elements:
        languages.append(element.text)

    return languages


if __name__ == '__main__':
    languages = get_languages()
    print(len(languages))
