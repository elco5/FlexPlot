import logging
logger = logging.getLogger('my_logger')


metadata_dictionary = {
    "WT3000": {
        "keywords": ["Function,Expression,Unit", "F01:"],
        "header_fetching_method": "parser.fetch_wt3000_header",
        "equipment_type": "WT3000",
        # 'sample_rate': 0.050
    },
    "smartdaq": {
        "keywords": ["SMARTDAC+ STANDARD", "GM10"],
        "header_fetching_method": "self.fetch_smartdaq_header",
    },
}


def fetch_wt3000_header(file_path: str) -> tuple[str, int]:
    # use the line that starts with 'Store No.,' as the heaer row
    _header_string = None
    _data_row = 1
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            _data_row += 1
            if "Store No." in line:
                _header_string = line
                break
        if _header_string is not None:
            # create a list of header items and strip the whitespace
            _header_list = _header_string.split(",")
            _header_list = [item.strip() for item in _header_list]
            
        elif _header_string is None:
            raise ValueError("No header row found")
    
    return _header_list, _data_row


def fetch_smartdaq_header(file_path) -> tuple[str, int]:
    logger.info(f"Fetching smartdaq header from {file_path}")
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Find the lines that contain the parts of the header
    tag_comment_line = [line for line in lines if "Tag Comment" in line][0]
    date_time_line = [line for line in lines if "Date" in line and "Time" in line][0]
    logger.info(f"found the compnents of the smartdaq header")
    # extract the parts to be used in the final header
    date_time_parts = date_time_line.split(",")[:3]
    tag_comment_parts = tag_comment_line.split(",")[3:]
    
    # Construct the final header and strip the whitespace
    _header_list = date_time_parts + tag_comment_parts
    _header_list = [item.strip() for item in _header_list]
    
    # Find the index of the first data row
    _data_row = lines.index(date_time_line) + 1
    logger.info(f"First data row is at index {_data_row}")
    
    return _header_list, _data_row


if __name__ == "__main__":
    file_path = r"../tests/sample_data/smartdaq_sample.csv"
    fetch_smartdaq_header(file_path)
    logger.info("Done")
