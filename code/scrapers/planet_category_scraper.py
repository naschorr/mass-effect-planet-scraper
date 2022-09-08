import logging
import string
from typing import Callable
from urllib import request

import utilities
from bs4 import BeautifulSoup

from .scraper import Scraper


class PlanetCategoryScraper(Scraper):
    """
    Handles scraping the planet category page for the name and URL of all potential planets
    """

    def __init__(self,
            root_url: str,
            url_query_param_format_string: str,
            page_name_starts_with_blacklist: list[str]
    ):
        self.logger = utilities.initialize_logging(logging.getLogger(__name__))

        self.root_url = root_url
        self.url_query_param_format_string = url_query_param_format_string
        self.page_name_starts_with_blacklist = page_name_starts_with_blacklist


    def _generate_section_urls(self, base_url: str) -> tuple[str, str]:
        def build_section_url(value: any) -> str:
            query_param = self.url_query_param_format_string.format(value)
            return f"{base_url}{query_param}"

        yield from [(str(value), build_section_url(value)) for value in range(10)]
        yield from [(value, build_section_url(value)) for value in string.ascii_lowercase]


    def _find_index_conditional(self, sequence: list, condition: Callable) -> int:
        """
        Finds the index of an element in a provided list based on the evaluation of a provided condition
        """

        for index, element in enumerate(sequence):
            if (condition(element)):
                return index

        return -1


    def _is_valid_page_name(self, page_name: str) -> bool:
        """
        Validate that the provided page name refers to a page that should be scraped
        """

        ## Does the page name start with any blacklisted strings?
        any_failed_conditions = any(page_name.startswith(value) for value in self.page_name_starts_with_blacklist)

        ## Chain additional conditions here if necessary

        return not any_failed_conditions


    def _extract_planets_from_category_section(self, section) -> dict[str, str]:
        planets_in_section_mapping = {}

        link_elements = section.parent.select("a.category-page__member-link")
        ## With the relevant section found, iterate over its children with this class. These elements have the name
        ## and href data that we need
        for element in link_elements:
            ## Some children are of the wrong type (ex. a link to a planet image)
            page_name = element.text
            if (not self._is_valid_page_name(page_name)):
                continue

            ## Ensure that the child isn't malformed, and has a link
            href = element.attrs.get('href')
            if (href is None):
                continue

            planets_in_section_mapping[page_name] = f"{self.root_url}{href}"

            self.logger.debug(f"Found: {page_name}, {planets_in_section_mapping[page_name]}")

        return planets_in_section_mapping


    def _scrape_planets_from_category_url(self, name: str, url: str) -> dict[str, str]:
        content = request.urlopen(url).read()
        soup = BeautifulSoup(content, "html.parser")

        ## Each page can have multuple sections, so we need to find the specific one for our current section_name
        sections = soup.select("div.category-page__first-char")
        ## This is the (index of the) section that's relevant to the current url, as the wiki will (sometimes) return multiple sections starting with the one requested
        section_index = self._find_index_conditional(sections, lambda candidate: candidate.text.strip().lower() == name.lower())
        if (section_index < 0):
            return {}

        section = sections[section_index]

        return self._extract_planets_from_category_section(section)


    def scrape(self, name: str, url: str) -> dict[str, str]:
        planet_url_mapping = {}

        ## Look over all provided planet category urls for potential planets and their urls
        for section_name, planet_url in self._generate_section_urls(url):
            ## And save those planet -> url mappings in memory for now
            planet_url_mapping.update(self._scrape_planets_from_category_url(section_name, planet_url))

            ## Don't just hammer their servers and get rate limited
            self.scrape_cooldown()

        return planet_url_mapping
