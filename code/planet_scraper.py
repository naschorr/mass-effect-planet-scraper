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
from scrapers.planet_category_scraper import PlanetCategoryScraper
from scrapers.planet_data_scraper import PlanetDataScraper
from models.planet import Planet

class PlanetScraper:
    def __init__(self):
        config = utilities.load_config()
        self.logger = utilities.initialize_logging(logging.getLogger(__name__))

        root_url: str = config.get("root_url")
        assert(root_url != None)

        planet_category_url_path: str = config.get("planet_category_url_path")
        assert(planet_category_url_path != None)

        url_query_param_format_string: str = config.get("url_query_param_format_string")
        assert(url_query_param_format_string != None)

        ## Essential start up of the class has completed, everything else is just setting the pieces into motion
        self.logger.info(f"Initialized {__name__}")

        planet_category_url = f"{root_url}{planet_category_url_path}"
        page_name_starts_with_blacklist: list = config.get("page_name_starts_with_blacklist", [])
        required_properties: list = config.get("required_properties", [])
        vague_data_mappings: dict[str, any] = config.get("vague_data_mappings", {})
        output_directory_path: Path = utilities.get_root_path() / Path(config.get("output_directory_path"))
        planet_index_json_name: str = config.get("planet_index_json_name", "planet_index")
        planet_index_json_path: Path = output_directory_path / f"{planet_index_json_name}.json"
        planet_data_json_name: str = config.get("planet_data_json_name", "planet_data")
        planet_data_json_path: Path = output_directory_path / f"{planet_data_json_name}.json"

        ## Init the scrapers
        self.planet_category_scraper = PlanetCategoryScraper(
            root_url,
            url_query_param_format_string,
            page_name_starts_with_blacklist
        )
        self.planet_data_scraper = PlanetDataScraper(required_properties, vague_data_mappings)

        ## Get a mapping of all planets to their wiki page urls
        self.planet_index: dict[str, str]
        try:
            self.planet_index = utilities.load_json(planet_index_json_path)
            self.logger.info(f"Loaded {len(self.planet_index.items())} planets from cache: {planet_index_json_path}")
        except FileNotFoundError:
            self.planet_index = self.planet_category_scraper.scrape(None, planet_category_url)
            self.logger.info(f"Loaded {len(self.planet_index.items())} planets from url: {planet_category_url}")

            utilities.store_json(self.planet_index, planet_index_json_path)
            self.logger.info(f"Stored {len(self.planet_index.items())} planets in cache: {planet_index_json_path}")

        ## Extract planetary info for each planet, and save it
        self.planets: list[Planet] = self._build_planets(self.planet_index)
        self.logger.info(f"Built {len(self.planets)} planets")

        ## Save planet data as a monolithic json file
        self._store_planets(self.planets, planet_data_json_path)
        self.logger.info(f"Stored {len(self.planets)} planets in store: {planet_data_json_path}")


    def _build_planets(self, planet_index: dict[str, str]) -> list[Planet]:
        planets: list[Planet] = []

        for name, url in planet_index.items():
            try:
                planet = self.planet_data_scraper.scrape(name, url)
            except Exception as e:
                self.logger.exception(e)
                continue

            planets.append(planet)
            self.logger.info(f"Built planet {planet.name}.")

        return planets


    def _store_planets(self, planets: list[Planet], path: Path):
        data = {planet.name: planet.to_dict() for planet in planets}

        utilities.store_json(data, path)


PlanetScraper()