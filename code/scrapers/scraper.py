import random
import time
from abc import ABC, abstractmethod

class Scraper(ABC):
    @abstractmethod
    def scrape(self, name: str, url: str) -> object:
        pass


    ## Implicitly virtual
    def scrape_cooldown(self, min_seconds: int = 0, max_seconds: int = 5):
        cooldown = random.uniform(min_seconds, max_seconds)
        self.logger.info(f"Sleeping for {cooldown:.1f} seconds")
        time.sleep(cooldown)
