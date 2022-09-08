from abc import ABC


class ToDict(ABC):
    def to_dict(self) -> dict:
        output = {}

        for member in dir(self):
            if (member.startswith("_")):
                continue

            attribute = getattr(self, member)

            if (callable(attribute)):
                continue

            output[member] = attribute

        return output
