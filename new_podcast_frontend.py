import streamlit as st
import json
import os
import modal  # Import Modal library


# Paths to the JSON files (relative to the location of this Python file)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path_1 = os.path.join(current_directory, 'podcast-1.json')
file_path_2 = os.path.join(current_directory, 'podcast-2.json')
file_path_3 = os.path.join(current_directory, 'podcast-3.json')

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

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
    if st.sidebar.button("Submit RSS"):
        pass

    st.sidebar.header("Enter your email address for a newsletter")
    email_address = st.sidebar.text_input("Email Address:")
    if st.sidebar.button("Subscribe"):
        with open(os.path.join(current_directory, 'subscribed_emails.txt'), 'a') as file:
            file.write(email_address + '\n')
        st.sidebar.success("Subscribed successfully!")

    return selected_podcast, email_address

def load_podcast_details(selected_podcast):
    json_files = [file_path_1, file_path_2, file_path_3]
    for file_path in json_files:
        details = json.load(open(file_path))
        if details['podcast_details']['podcast_title'] == selected_podcast:
            return details

def get_podcast_filename(selected_podcast):
    json_files = [file_path_1, file_path_2, file_path_3]
    for file_path in json_files:
        details = json.load(open(file_path))
        if details['podcast_details']['podcast_title'] == selected_podcast:
            return os.path.basename(file_path)

def extract_highlights(highlights_content):
    try:
        sections = highlights_content.split('\n\n')
        summary = sections[0].replace('Summary: ', '')
        key_insights = sections[1].replace('Key insights:\n', '') if len(sections) > 1 else "Not available"
        return summary, key_insights
    except Exception as e:
        st.error(f"An error occurred while extracting highlights: {str(e)}")
        return "Not available", "Not available"

def build_main_page(selected_podcast, email_address):
    try:
        podcast_details = load_podcast_details(selected_podcast)
        podcast_filename = get_podcast_filename(selected_podcast)
        podcast_highlights = podcast_details.get('podcast_highlights', '')
        summary, key_insights = extract_highlights(podcast_highlights)
        st.title("Your Podcast Pal - AI Generated Summaries To Save You Time")
        col1, col2 = st.columns(2)
        with col1:
            st.image(podcast_details['podcast_details']['episode_image'])
            add_to_newsletter = st.checkbox("Add this Podcast Summary to my Newsletter Subscription")
            if add_to_newsletter:
                with open(os.path.join(current_directory, 'newsletter_subscriptions.txt'), 'a') as file:
                    file.write(f"{email_address},{podcast_filename}\n")
            st.markdown(f"**Podcast Title:** {podcast_details['podcast_details']['podcast_title']}")
            st.markdown(f"**Podcast Guest:** {podcast_details['podcast_guest']}")
            st.markdown(f"**Summary:** {summary}")

        with col2:
            st.markdown("**Key Insights:**")
            st.markdown(key_insights)
            critical_questions = podcast_highlights.split('Critical questions:\n')[1].split('Hot topics/controversial opinions:')[0] if 'Critical questions:' in podcast_highlights else "Not available"
            hot_topics = podcast_highlights.split('Hot topics/controversial opinions:\n')[1] if 'Hot topics/controversial opinions:' in podcast_highlights else "Not available"
            st.markdown("**Critical Questions:**")
            st.markdown(critical_questions)
            st.markdown("**Hot Topics/Controversial Opinions:**")
            st.markdown(hot_topics)
    except Exception as e:
        st.error(f"An error occurred while building the main page: {str(e)}")

def main():
    selected_podcast, email_address = build_sidebar()
    build_main_page(selected_podcast, email_address)

main()
