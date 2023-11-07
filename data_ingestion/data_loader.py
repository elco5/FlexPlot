import os
import importlib
import parser
from utilities.logging import setup_logger


logger = setup_logger()
logger.info("Logging intitialized...")


####################################################################
# CLASS DEFINITION
####################################################################
class DataLoader:
    def __init__(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        self.file_info = {
            "full_path": None,
            "directory": None,
            "base_name": None,
            "type": None,
        }
        self.data = {
            "header_row": None,
            "data_frame": None,
        }
        self.metadata = {
            "equipment_type": None,
        }

        logger.info(f"DataLoader object from filename: {file_path}")

    ####################################################################
    # CLASS METHODS
    ####################################################################

    def auto_load(self, file_path) -> None:
        logger.info("Autoloader runining...")
        self.get_file_attributes(file_path)
        logger.info("Attempting to parse file metadata...")
        self.parse_metadata()
        self.get_header_row()

    def get_file_attributes(self, file_path) -> None:
        if os.path.isdir(file_path):
            logger.error(f"Provided path is a directory, not a file: {file_path}")
            raise ValueError("Provided path is a directory, not a file")

        self.file_info["full_path"] = file_path
        self.file_info["directory"], self.file_info["base_name"] = os.path.split(
            file_path
        )

        if not self.file_info["base_name"]:
            logger.error("File name is missing in the provided path")
            raise ValueError("File name is missing in the provided path")

        self.file_info["type"] = os.path.splitext(self.file_info["base_name"])[1]

        if not self.file_info["type"]:
            logger.warning(f"File extension is missing for the file: {file_path}")
        elif self.file_info["type"].lower() not in [".csv", ".xlsx"]:
            logger.warning(f"Unexpected file type: {self.file_info['type']}")

        logger.info(f"File attributes populated from: {self.file_info['base_name']}")

    def parse_metadata(self) -> None:
        lines_to_read = 5

        def read_first_n_lines(file_path, lines_to_read):
            lines = []
            with open(file_path, "r") as file:
                for _ in range(lines_to_read):
                    line = file.readline()
                    if not line:
                        break
                    lines.append(line)
            return "".join(lines)

        # Read the first 5 lines of the file
        first_n_lines = read_first_n_lines(self.file_info["full_path"], lines_to_read)
        logger.debug(f"First {lines_to_read} lines of the file: {first_n_lines}")

        # Iterate over each item in the metadata dictionary
        for device, attributes in parser.metadata_dictionary.items():
            if any(keyword in first_n_lines for keyword in attributes["keywords"]):
                self.equipment_type = device
                logger.info(f"Identified equipment type: {self.equipment_type}")

    def get_header_row(self) -> None:
        # use the equipment type to get the header by using the associated function
        if self.equipment_type == "WT3000":
            header_row = parser.fetch_wt3000_header(self.file_info["full_path"])
            self.data["header_row"] = header_row
            logger.info(f"Found header row:\n {header_row}")

        elif self.equipment_type == "smartdaq":
            header_row = parser.fetch_smartdaq_header(self.file_info["full_path"])
            self.data["header_row"] = header_row
            logger.info(f"Found header row: {header_row}")

        elif header_row is None:
            logger.error(f"No header fetching method found for {self.equipment_type}")
            raise ValueError(
                f"No header fetching method found for {self.equipment_type}"
            )

    def load_data(self):
        # Logic to load the data into a DataFrame
        pass


if __name__ == "__main__":
    file_path = r"../tests/sample_data/wt3000_file.csv"
    data = DataLoader(file_path=file_path)
    data.auto_load(file_path)
