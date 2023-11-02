import os

DEBUG = True

if DEBUG:
    # ### DEBUG IMPORT
    # When using AREPL name=='__main__'
    # Relative imports wont work.
    import sys
    sys.path.append('../')
    from utilities.logging import setup_logger

elif not DEBUG:
    # NON-DEBUG IMPORT
    # EXAMPLE: from ..package1 import module1
    # This is a relative import that goes up one level (..)
    # and then into the package1 directory.
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
            'full_path': None,
            'directory': None,
            'base_name': None,
            'type': None,
        }
        self.data = {
            'header': None,
            'dataframe': None,
        }
        self.metadata = {
            'measurement_device': None,
        }

        logger.info(
            f"DataLoader object succesfully created.") # with filename: {file_path}")

        

    ####################################################################
    # CLASS METHODS
    ####################################################################

    def auto_load(self, file_path) -> None:
        logger.info("Autoloader runining...")
        self.get_file_attributes(file_path)
        logger.info("Attempting to parse file metadata...")
        # self.parse_metadata()

    def get_file_attributes(self, file_path) -> None:
        if os.path.isdir(file_path):
            logger.error(
                f"Provided path is a directory, not a file: {file_path}")
            raise ValueError("Provided path is a directory, not a file")

        self.file_info['full_path'] = file_path
        self.file_info['directory'], self.file_info['base_name'] = os.path.split(
            file_path)

        if not self.file_info['base_name']:
            logger.error("File name is missing in the provided path")
            raise ValueError("File name is missing in the provided path")

        self.file_info['type'] = os.path.splitext(
            self.file_info['base_name'])[1]

        if not self.file_info['type']:
            logger.warning(
                f"File extension is missing for the file: {file_path}")
        elif self.file_info['type'].lower() not in ['.csv', '.xlsx']:
            logger.warning(f"Unexpected file type: {self.file_info['type']}")

        logger.info(f"File attributes successfully populated from: {self.file_info['base_name']}")

    # def get_file_attributes(self, file_path) -> None:

    #     self.file_info['full_path'] = file_path
    #     # Extract the directory and base filename with extension
    #     self.file_info['directory'], self.file_info['base_name'] = os.path.split(file_path)
    #     self.file_info['type'] = os.path.splitext(self.file_info['base_name'])[1]
    #     logger.info(f"File attributes succesfully populated")# with: {self.file_info}")

    def parse_metadata(self):

        lines_to_read = 5
        with open(self.file_info['full_path'], 'r', encoding='utf-8') as f:
            # N is the number of lines you want to read
            lines = [f.readline().strip() for _ in range(lines_to_read)]

            # for keyword, header_fetching_method in config.metadata_dictionary.items:
            #     # look for metadata keywords
            #     # and determine header_fetching_method

    def find_data_pattern(self, file_type):
        # Logic to scan for data patterns
        # Useful for double-checking or handling complex files
        pass

    def load_data(self, file_type, header_row):
        # Logic to load the data into a DataFrame
        # Handle different file types and apply transformations as needed
        pass

    # def auto_load(self):
    #     file_type = self.determine_file_type()
    #     header_row, metadata = self.parse_metadata(file_type)

    #     if header_row is None:
    #         header_row = self.find_data_pattern(file_type)

    #     df = self.load_data(file_type, header_row)
    #     return df, metadata

        # # Read the specific lines that contain parts of the header based on equipment type
        # if equipment_type == 'SmartDAQ':
        #     header_row = self.parse_smartdaq_header()

    # def parse_smartdaq_header(self):

    #     # Find the lines that contain the parts of the header
    #     tag_comment_line = [line for line in lines if "Tag Comment" in line][0]
    #     date_time_line = [
    #         line for line in lines if "Date" in line and "Time" in line][0]

    #     # Extract the relevant parts and construct the final header
    #     tag_comment_parts = tag_comment_line.split(
    #         "\t")[2:]  # Adjust based on the actual structure
    #     # Assuming "Date" and "Time" are the first two elements
    #     date_time_parts = date_time_line.split("\t")[:2]

    #     final_header = date_time_parts + tag_comment_parts
    #     return final_header


if DEBUG:
    file_path = r"C:\Users\ecountrywood\dev\tools\FlexPlot\tests\sample_data\sample_input_files\Overvoltage_264V_PM_0001.csv"
    data = DataLoader(file_path=file_path)
    data.auto_load(file_path)

else:
    if __name__ == '__main__':
        file_path = r"C:\Users\ecountrywood\dev\tools\FlexPlot\tests\sample_data\sample_input_files\Overvoltage_264V_PM_0001.csv"
        data = DataLoader(file_path=file_path)
        data.auto_load(file_path)
    