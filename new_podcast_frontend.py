import streamlit as st
import json
import os
import modal  # Import Modal library

def load_podcast(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_dict_from_json_files(.):
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


def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

def main():
    st.title("Your Podcast Pal - AI Generated Summaries To Save You Time")

    # Load available podcasts
    available_podcasts = create_dict_from_json_files('file_path')  # Update path as needed

    # Sidebar to select podcast RSS feed or enter custom URL
    st.sidebar.header("Select Podcast RSS Feed")
    podcast_option = st.sidebar.selectbox("Choose a podcast:", list(available_podcasts.keys()) + ["Custom URL"])
    
    # Sidebar to select podcast RSS feed or enter custom URL
    st.sidebar.header("Select Podcast RSS Feed")
    podcast_option = st.sidebar.selectbox("Choose a podcast:", ["Podcast 1", "Podcast 2", "Podcast 3", "Custom URL"])

    # Fun and special note for custom URL option
    st.sidebar.markdown(":tada: **Hey, Listener!** :tada:")
    st.sidebar.markdown("Feeling explorative? Choose 'Custom URL' from the dropdown above and enter your very own podcast URL! Then we'll process a summary of the latest episode for you! :sparkles:")

    # Input field for custom Podcast URL
    custom_url = ""
    if podcast_option == "Custom URL":
        custom_url = st.sidebar.text_input("Enter Podcast URL:")

    # Sidebar to select podcast RSS feed or enter custom URL
    st.sidebar.header("Select Podcast RSS Feed")
    podcast_option = st.sidebar.selectbox("Choose a podcast:", list(available_podcasts.keys()) + ["Custom URL"])

    # Load available podcasts
    available_podcasts = create_dict_from_json_files(file_path)  # Load JSON files from current directory
    
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
            file.write(f"Email Address: {email_address}\n")  # Save email address to file
            for name, summary in selected_podcasts.items():
                file.write(f"{name}: {summary}\n")
        st.sidebar.success("Subscribed! Summaries saved to selected_summaries.txt")

    # Email input field
    email_address = st.sidebar.text_input("Enter your email address:")

    # Load the selected podcast data from dropdown (only if "Custom URL" is not selected)
    if podcast_option in available_podcasts and podcast_option != "Custom URL":
        podcast_data = available_podcasts[podcast_option]
        cols = st.columns([1, 1])  # Create two columns
        # Column 1: Image, Podcast Title, Episode Title, Guest, and Summary
        cols[0].image(podcast_data["podcast_details"]["episode_image"], use_column_width=True)
        cols[0].header(podcast_data["podcast_details"]["podcast_title"])
        cols[0].subheader(podcast_data["podcast_details"]["episode_title"])
        cols[0].markdown("**Guest:** " + podcast_data["podcast_guest"])
        cols[0].markdown("**Summary:** " + podcast_data["podcast_summary"])
        # Column 2: Highlights
        cols[1].markdown("**Highlights:** " + podcast_data["podcast_highlights"])
    elif podcast_option == "Custom URL":
        st.write("Custom URL processing not yet implemented.")

if __name__ == "__main__":
    main()
