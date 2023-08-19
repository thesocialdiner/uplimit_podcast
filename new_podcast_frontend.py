def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"JSON files found in {folder_path}: {json_files}")  # Debugging print statement
    data_dict = {}
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        print(f"Loading JSON file from {file_path}")  # Debugging print statement
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info
    return data_dict
