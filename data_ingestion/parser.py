


from utilities.logging import setup_logger

logger = setup_logger()


metadata_dictionary = {
    'WT3000': {
        'keywords': ['Function,Expression,Unit',
                     "F01:"],
        'header_fetching_method': 'parser.fetch_wt3000_header',
        'equipment_type': 'WT3000',
        # 'sample_rate': 0.050 
    },
    'smartdaq': {
        'keywords': ['SMARTDAC+ STANDARD', 'GM10'],
        'header_fetching_method': 'self.fetch_smartdaq_header',
    },

}

def fetch_wt3000_header(file_path):
    # use the line that starts with 'Store No.,' as the heaer row   
    header_row = None
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "Store No." in line:
                header_row = line
                break
    return header_row
        
def fetch_smartdaq_header(file_path):
    
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Find the lines that contain the parts of the header
    tag_comment_line = [line for line in lines if "Tag Comment" in line][0]
    date_time_line = [
        line for line in lines if "Date" in line and "Time" in line][0]

    # Extract the relevant parts and construct the final header
    tag_comment_parts = tag_comment_line.split(
        ",")[3:]  # Adjust based on the actual structure
    # Assuming "Date" and "Time" are the first two elements
    date_time_parts = date_time_line.split(",")[:3]

    final_header = date_time_parts + tag_comment_parts
    # print(final_header)
    return final_header

if __name__ == "__main__":
    file_path = r"../data/sample_data/smartdaq_sample.csv"
    fetch_smartdaq_header(file_path)
    logger.info("Done")