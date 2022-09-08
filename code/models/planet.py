from .body import Body
from extensions.to_dict import ToDict

class Planet(Body, ToDict):
    def __init__(self,
        name: str,
        ## Location
        galaxy: str,
        cluster: str,
        system: str,
        ## Text Properties
        description: list[str],
        properties: list[str],
        codex: list[str],
        additional_info: list[str],
        survey_text: list[str],
        ## Planetary Properties
        orbital_distance_au: float,
        orbital_period_years: float,
        keplerian_ratio: float,
        radius_km: float,
        day_length_earth_hours: float,
        atmospheric_pressure: float,
        surface_temperature_celcius: float,
        surface_gravity_g: float,
        mass_earth_masses: float,
        satellite_count: int
    ):
        super().__init__(name, galaxy, cluster, system, description, properties, codex, additional_info, survey_text)

        self.orbital_distance_au = orbital_distance_au
        self.orbital_period_years = orbital_period_years
        self.keplerian_ratio = keplerian_ratio
        self.radius_km = radius_km
        self.day_length_earth_hours = day_length_earth_hours
        self.atmospheric_pressure = atmospheric_pressure
        self.surface_temperature_celcius = surface_temperature_celcius
        self.surface_gravity_g = surface_gravity_g
        self.mass_earth_masses = mass_earth_masses
        self.satellite_count = satellite_count

    ## Properties

    @property
    def orbital_distance_au(self) -> float:
        return self._orbital_distance_au

    @orbital_distance_au.setter
    def orbital_distance_au(self, value: float):
        self._orbital_distance_au = value


    @property
    def orbital_period_years(self) -> float:
        return self._orbital_period_years

    @orbital_period_years.setter
    def orbital_period_years(self, value: float):
        self._orbital_period_years = value


    @property
    def keplerian_ratio(self) -> float:
        return self._keplerian_ratio

    @keplerian_ratio.setter
    def keplerian_ratio(self, value: float):
        self._keplerian_ratio = value


    @property
    def radius_km(self) -> float:
        return self._radius_km

    @radius_km.setter
    def radius_km(self, value: float):
        self._radius_km = value


    @property
    def day_length_earth_hours(self) -> float:
        return self._day_length_earth_hours

    @day_length_earth_hours.setter
    def day_length_earth_hours(self, value: float):
        self._day_length_earth_hours = value


    @property
    def atmospheric_pressure(self) -> float:
        return self._atmospheric_pressure

    @atmospheric_pressure.setter
    def atmospheric_pressure(self, value: float):
        self._atmospheric_pressure = value


    @property
    def surface_temperature_celcius(self) -> float:
        return self._surface_temperature_celcius

    @surface_temperature_celcius.setter
    def surface_temperature_celcius(self, value: float):
        self._surface_temperature_celcius = value


    @property
    def surface_gravity_g(self) -> float:
        return self._surface_gravity_g

    @surface_gravity_g.setter
    def surface_gravity_g(self, value: float):
        self._surface_gravity_g = value


    @property
    def mass_earth_masses(self) -> float:
        return self._mass_earth_masses

    @mass_earth_masses.setter
    def mass_earth_masses(self, value: float):
        self._mass_earth_masses = value


    @property
    def satellite_count(self) -> int:
        return self._satellite_count

    @satellite_count.setter
    def satellite_count(self, value: int):
        self._satellite_count = value