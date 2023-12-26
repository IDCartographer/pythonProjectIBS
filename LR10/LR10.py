from abc import ABC, abstractmethod
from io import StringIO
import json
import csv
import yaml

class BaseWriter(ABC):
    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        pass

class JSONWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        json_data = json.dumps(data, indent=2)
        return StringIO(json_data)

class CSVWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerows(data)
        return csv_data

class YAMLWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        yaml_data = yaml.dump(data, default_flow_style=False)
        return StringIO(yaml_data)

class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data

    def generate(self) -> None:
        data = [
            [1, "дед", 2.5],
            [2, "менеджер", 1.8],
            [3, "1231", 3.2],
            [4, "чтото", 2.0]
        ]
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        if self.data is None:
            raise Exception("Data has not been generated")

        file_content = writer.write(self.data)

        with open(path, "w") as file:
            file.write(file_content.getvalue())


generator = DataGenerator()
generator.generate()

json_writer = JSONWriter()
generator.to_file("data.json", json_writer)

csv_writer = CSVWriter()
generator.to_file("data.csv", csv_writer)

yaml_writer = YAMLWriter()
generator.to_file("data.yaml", yaml_writer)
