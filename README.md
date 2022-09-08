# Planet Scraper

Scrapes planetary data from the Mass Effect wiki for later usage

## The Data

The scraped data is available [here](https://github.com/naschorr/planet-scraper/blob/main/out/planet_data.json). It consists of a JSON file containing a mapping of planet names to planet objects. The planet object that each item is built from can be found [here](https://github.com/naschorr/planet-scraper/blob/main/code/models/planet.py).

## Running the Scraper

Running the scraper is pretty simple:

- Clone the repo to your system and `cd` into it
- Create a virtualenv: `python -m venv .`
- Install the requirements: `pip install -r requirements.txt`
- Double check the `config.jsonc`, and make sure everything looks good. Make sure to check the `required_properties` line if you want to enforce more or less correctness in the scraping, as well as the output options.
- Run it!
  - If you're using VS Code on Windows, feel free to use the provided launch option: "Python: Planet Scraper (Win)".
  - If not, from the activated virtualenv: `cd code; python planet_scraper.py`
