from json import JSONEncoder
import string
import time
import random
import logging
import itertools
import re
from typing import Callable
from urllib import request
from pathlib import Path

import unidecode
from bs4 import BeautifulSoup
from bs4.element import Tag

import utilities
from .scraper import Scraper
from models.planet import Planet


class PlanetDataScraper(Scraper):
    """
    Scrapes detailed planetary data from the specific page for that planet, and will yield a Planet object
    """

    def __init__(self,
        required_properties: list[str],
        vague_data_mappings: dict[str, any]
    ):
        self.logger = utilities.initialize_logging(logging.getLogger(__name__))

        self.required_properties = required_properties
        self.vague_data_mappings = vague_data_mappings
        self.non_float_regex = re.compile("[^\d\.-]")


    def _extract_planet_location(self, soup) -> tuple[str, str, str]:
        output = []

        location_start_element = soup.find(lambda tag: tag.name == "b" and tag.text.startswith("Location"))
        for element in itertools.islice(location_start_element.next_siblings, 1, 6, 2):
            output.append(element.text)

        return tuple(output)


    def _extract_text_below_header(self, header_text: str, soup) -> list[str]:
        header = soup.find(
            lambda tag: tag.parent.name.startswith("h") and tag.text.startswith(header_text)
        )

        if (header is None):
            return None

        content: list[str] = []
        element = header.parent
        stop = False
        while (not stop and element.next_sibling != None):
            element = element.next_sibling

            if (issubclass(type(element), str)):
                continue

            if (isinstance(element, Tag)):
                if (element.name in ["span", "p"]):
                    ## Convert the misc unicode characters into their approximate ascii flavor (it's usually just nbsp
                    ## and quote marks, so this is fine)
                    text = unidecode.unidecode(element.text.strip())

                    content.extend(text.splitlines())
                elif (element.name.startswith("h")):
                    stop = True

        return content


    def _convert_str_to_float(self, value: str) -> float:
        parsed = self.non_float_regex.sub("", value)

        return float(parsed)


    def _extract_planet_infobox_datum(self, infobox_key: str, soup) -> str:
        infobox = soup.select(".portable-infobox")
        if (len(infobox) == 0):
            return None

        datum_container = infobox[0].select(f"[data-source='{infobox_key}']")
        if (len(datum_container) == 0):
            return None

        value_container = datum_container[0].select(".pi-data-value")
        if (len(value_container) == 0):
            return None

        value = value_container[0].text.lower()

        if (value in self.vague_data_mappings):
            return str(self.vague_data_mappings.get(value))

        return value


    def _extract_planet_infobox_datum_float(self, infobox_key: str, soup) -> float:
        datum = self._extract_planet_infobox_datum(infobox_key, soup)

        if (datum is not None):
            return self._convert_str_to_float(datum)

        return None


    def _extract_planet_infobox_atmospheric_pressure(self, soup) -> float:
        atmospheric_pressure = self._extract_planet_infobox_datum("atmpressure", soup)
        if (atmospheric_pressure is None):
            return None

        return self._convert_str_to_float(atmospheric_pressure)


    def _extract_planet_infobox_satellites(self, soup) -> int:
        satellites = self._extract_planet_infobox_datum("satellites", soup)
        if (satellites is None):
            return None

        ## Ideally it can be converted to an int easily
        try:
            return int(satellites)
        except Exception:
            pass

        ## Or it's a list of explicitly named satellite(s) separated by commas
        if (len(satellites) > 0):
            return len(satellites.split(","))

        ## Fallback
        return 0


    def _is_valid_planet(self, planet: Planet) -> bool:
        if (any(getattr(planet, prop) is None for prop in self.required_properties)):
            return False

        return True


    def scrape(self, name: str, url: str) -> Planet:
        content = request.urlopen(url).read()
        ## Don't just hammer the server and get rate limited
        self.scrape_cooldown()
        soup = BeautifulSoup(content, "html.parser")

        location = self._extract_planet_location(soup)

        planet = Planet(
            name,
            location[0],
            location[1],
            location[2],
            self._extract_text_below_header("Description", soup),
            self._extract_text_below_header("Properties", soup),
            self._extract_text_below_header("Codex", soup),
            self._extract_text_below_header("Additional", soup),
            self._extract_text_below_header("Survey", soup),
            self._extract_planet_infobox_datum_float("orbitaldistance", soup),
            self._extract_planet_infobox_datum_float("orbitalperiod", soup),
            self._extract_planet_infobox_datum_float("kepler", soup),
            self._extract_planet_infobox_datum_float("radius", soup),
            self._extract_planet_infobox_datum_float("daylength", soup),
            self._extract_planet_infobox_atmospheric_pressure(soup),
            self._extract_planet_infobox_datum_float("surfacetemp", soup),
            self._extract_planet_infobox_datum_float("surfacegrav", soup),
            self._extract_planet_infobox_datum_float("mass", soup),
            self._extract_planet_infobox_satellites(soup)
        )

        if (self._is_valid_planet(planet)):
            return planet

        return None
