from typing import Dict, Any, List, Callable, Tuple
import os
import pandas as pd

from . import flex_parser as fp 
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
        
        self.file_info: Dict[str,str] = {
            "full_path": None,
            "directory": None,
            "base_name": None,
            "type": None,
        }
        self.data: Dict[str, Any] = {
            "first_data_row": 0,
            "header_string": "",
            "data_frame": pd.DataFrame(),
            "columns": []
        }
        self.metadata: Dict[str] = {
            "equipment_type": None,
        }

        logger.info(f"DataLoader object created. Referenceing filename: {file_path}")

    ####################################################################
    # CLASS METHODS
    ####################################################################

    def auto_load(self, file_path: str) -> None:
        logger.info("Autoloader runining...")
        self.get_file_attributes(file_path)
        logger.info("Attempting to parse file metadata...")
        self.parse_metadata()
        self.get_header()
        self.load_data()

    def get_file_attributes(self, file_path: str) -> None:
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
        for device, attributes in fp.metadata_dictionary.items():
            if any(keyword in first_n_lines for keyword in attributes["keywords"]):
                self.equipment_type = device
                logger.info(f"Identified equipment type: {self.equipment_type}")

    def get_header(self) -> None:
        # Define the type alias for the header fetching function signature
        HeaderFetchFunction = Callable[[str], Tuple[str, int]]
        # Dictionary mapping equipment types to their header fetching functions
        header_fetch_methods: Dict[str, HeaderFetchFunction] = {
            "WT3000": fp.fetch_wt3000_header,
            "smartdaq": fp.fetch_smartdaq_header,
        }

        # Get the appropriate header fetching function based on the equipment type
        fetch_header = header_fetch_methods.get(self.equipment_type)
        logger.info(f"Fetching header for {self.equipment_type}...")

        if fetch_header:
            _columns, _first_data_row = fetch_header(self.file_info["full_path"])
            self.data["columns"] = _columns
            self.data["first_data_row"] = _first_data_row
            logger.info(f"Able to fetch header for {self.equipment_type}")
        else:
            logger.error(f"No header fetching method found for {self.equipment_type}")
            raise ValueError(f"No header fetching method found for {self.equipment_type}")
    
    def clean_header(self):
        # Split the header_string string into a list of column names
        columns = self.data["header_string"].strip().split(',')
        # Clean the column names
        columns = [col.strip() for col in columns]
        self.data["columns"] = columns
        
    
    def load_data(self):
        # Logic to load the data into a DataFrame using  
        # self.data["header"] as the header, 
        # and self.data["first_data_row"] as the first row of data
        # self.clean_header()
        # Now, read the rest of the data into a DataFrame, skipping rows up to the header
        # and setting the column names to the ones you've extracted
        df = pd.read_csv(self.file_info['full_path'], skiprows=self.data["first_data_row"], header=None)
        df.columns = self.data["columns"]
        self.data["data_frame"] = df
        logger.info(f"Loaded data into DataFrame:\n {df.head(3)}")


if __name__ == "__main__":
    file_path = r"C:\Users\count\dev\FlexPlot\tests\sample_data\wt3000_file.csv"
    # file_path = r"C:\Users\count\dev\FlexPlot\tests\sample_data\smartdaq_sample.csv"
    data = DataLoader(file_path=file_path)
    data.auto_load(file_path)
    # print(data.data["data_frame"].head(),5)
