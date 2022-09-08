class Body:
    def __init__(self,
            name: str,
            ## Location
            galaxy: str,
            cluster: str,
            system: str,
            ## Properties
            description: list[str],
            properties: list[str],
            codex: list[str],
            additional_info: list[str],
            survey_text: list[str]
    ):
        self.name = name
        self.galaxy = galaxy
        self.cluster = cluster
        self.system = system
        self.description = description
        self.properties = properties
        self.codex = codex
        self.additional_info = additional_info
        self.survey_text = survey_text

    ## Properties

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value


    @property
    def galaxy(self) -> str:
        return self._galaxy

    @galaxy.setter
    def galaxy(self, value: str):
        self._galaxy = value


    @property
    def cluster(self) -> str:
        return self._cluster

    @cluster.setter
    def cluster(self, value: str):
        self._cluster = value


    @property
    def system(self) -> str:
        return self._system

    @system.setter
    def system(self, value: str):
        self._system = value


    @property
    def description(self) -> list[str]:
        return self._description

    @description.setter
    def description(self, value: list[str]):
        self._description = value


    @property
    def properties(self) -> list[str]:
        return self._properties

    @properties.setter
    def properties(self, value: list[str]):
        self._properties = value


    @property
    def codex(self) -> list[str]:
        return self._codex

    @codex.setter
    def codex(self, value: list[str]):
        self._codex = value


    @property
    def additional_info(self) -> list[str]:
        return self._additional_info

    @additional_info.setter
    def additional_info(self, value: list[str]):
        self._additional_info = value


    @property
    def survey_text(self) -> list[str]:
        return self._survey_text

    @survey_text.setter
    def survey_text(self, value: list[str]):
        self._survey_text = value