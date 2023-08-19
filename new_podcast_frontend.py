import streamlit as st
import json

def load_podcast(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
    
(file_path)_1 = 'path/to/podcast-1.json'
(file_path)_2 = 'path/to/podcast-2.json'
(file_path)_3 = 'path/to/podcast-3.json'

def load_podcast_titles():
    json_files = [file_path_1, file_path_2, file_path_3]
    titles = [json.load(open(file_path))['podcast_details']['podcast_title'] for file_path in json_files]
    return titles

def build_sidebar():
    st.sidebar.header("Select an RSS feed")
    podcast_titles = load_podcast_titles()
    selected_podcast = st.sidebar.selectbox("Choose a podcast:", podcast_titles)

    st.sidebar.header("Enter your own RSS feed to process")
    rss_feed = st.sidebar.text_input("RSS Feed URL:")
    if st.sidebar.button("Submit"):
        # Placeholder for calling the "process_podcast" function with the entered RSS feed
        pass

    st.sidebar.header("Enter your email address for a newsletter")
    email_address = st.sidebar.text_input("Email Address:")

    return selected_podcast, rss_feed, email_address

def load_podcast_details(selected_podcast):
    json_files = [file_path_1, file_path_2, file_path_3]
    for file_path in json_files:
        details = json.load(open(file_path))['podcast_details']
        if details['podcast_title'] == selected_podcast:
            return details

def build_main_page(selected_podcast):
    podcast_details = load_podcast_details(selected_podcast)

    # First column to show podcast image, title, and guest
    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(podcast_details['episode_image'])
        st.markdown(f"**Podcast Title:** {podcast_details['podcast_title']}")
        st.markdown(f"**Podcast Guest:** {podcast_details.get('podcast_guest', 'N/A')}")

    # Second column to show Key insights, Critical questions, and Hot topics/controversial opinions
    with col2:
        st.markdown("**Key Insights:**") # Placeholder
        st.markdown("**Critical Questions:**") # Placeholder
        st.markdown("**Hot Topics/Controversial Opinions:**") # Placeholder

def main():
    selected_podcast, rss_feed, email_address = build_sidebar()
    build_main_page(selected_podcast)

main()
