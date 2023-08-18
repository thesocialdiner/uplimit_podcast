import streamlit as st
import json
import os
import modal  # Import Modal library

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info

    return data_dict


def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

def main():
    st.title("Your Podcast Pal - AI Generated Summaries To Save You Time")

    # Sidebar to select podcast RSS feed or enter custom URL
    st.sidebar.header("Select Podcast RSS Feed")
    podcast_option = st.sidebar.selectbox("Choose a podcast:", ["Podcast 1", "Podcast 2", "Podcast 3", "Custom URL"])

    # Fun and special note for custom URL option
    st.sidebar.markdown(":tada: **Hey, adventurer!** :tada:")
    st.sidebar.markdown("Feeling explorative? Choose 'Custom URL' from the dropdown above and enter your very own podcast URL! Then we'll process a summary of the latest episode for you! :sparkles:")

    # Input field for custom Podcast URL
    custom_url = ""
    if podcast_option == "Custom URL":
        custom_url = st.sidebar.text_input("Enter Podcast URL:")

    # Load available podcasts
    available_podcasts = create_dict_from_json_files('.')  # Load JSON files from current directory

    # Heading above checkboxes
    if podcast_option != "Custom URL":
        st.header("Select podcasts to be summarized in a weekly newsletter!")

    # Display available podcasts with checkboxes (only if "Custom URL" is not selected)
    selected_podcasts = {}
    if podcast_option != "Custom URL":
        for name in available_podcasts.keys():
            selected = st.checkbox(name, key=name)
            if selected:
                selected_podcasts[name] = available_podcasts[name]["podcast_summary"]

    # Sidebar: Display selected podcasts and Subscribe button
    st.sidebar.header("Selected Podcasts for Newsletter")
    for name in selected_podcasts.keys():
        st.sidebar.write(name)
    if st.sidebar.button("Subscribe"):
        # Create text file with selected summaries
        with open("selected_summaries.txt", "w") as file:
            for name, summary in selected_podcasts.items():
                file.write(f"{name}: {summary}\n")
        st.sidebar.success("Subscribed! Summaries saved to selected_summaries.txt")

    # Load the selected podcast data from dropdown (only if "Custom URL" is not selected)
    if podcast_option in available_podcasts and podcast_option != "Custom URL":
        podcast_data = available_podcasts[podcast_option]
        # ... Rest of the code for displaying podcast details ...

    elif podcast_option == "Custom URL" and custom_url:
        podcast_data = process_podcast_info(custom_url)
        # ... Rest of the code for displaying podcast details ...

    else:
        st.write("Custom URL processing not yet implemented.")

if __name__ == "__main__":
    main()
