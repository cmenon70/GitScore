import csv
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import markupsafe

def calculate_score(no_of_repos, no_of_languages, age_of_account, no_of_forks):
    if age_of_account==0:
        return 0
    else: 
        return ((0.2 * no_of_forks) + (0.35 * no_of_repos) + (0.35 * no_of_languages) + (0.1 * (no_of_repos/(age_of_account + 0.1))) )
    
def getuserdeetswithCSV(uploaded_file):
    # Upload a CSV file containing a list of GitHub URLs
    #uploaded_file = st.file_uploader("Choose a file", type=["csv"]).
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode('utf-8')
        csv_reader = csv.DictReader(content.splitlines(), delimiter=',')
        urls = [row['URL'] for row in csv_reader]
        age_in_years=0
        score=0

        # Set up the request headers
        headers = {'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'Bearer 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'}

        # Loop through each URL in the list and extract the desired information
        data_list = []
        for url in urls:
            username = url.split('/')[-1]
            api_url = f'https://api.github.com/users/{username}'

            # Make the request and parse the JSON response
            response = requests.get(api_url, headers=headers)
            data = response.json()

            # Extract the email, location, following, public repos, hireable status, bio, website, and language information from the JSON data
            email = data.get('email','')
            location = data.get('location','') 
            followers = data.get('followers','')
            following = data.get('following','')
            repos = data.get('public_repos','')
            hirable = data.get('hireable','') 
            bio = data.get('bio','')
            website = data.get('blog','')
            repos_url = data.get('repos_url','')
            created_at = data.get('created_at','')

            languages = {}

            # Make another request to get the user's repository information
            if repos_url:
                repos_response = requests.get(repos_url, headers=headers)
                repos_data = repos_response.json()

                languages = {}
                total_forks=0

                # Loop through each repository and extract the language information
                for repo in repos_data:
                    forks_count = repo['forks_count']
                    total_forks += forks_count
                    if repo['language']:
                        language = repo['language']
                        if language in languages:
                            languages[language] += 1
                        else:
                            languages[language] = 1

                # Compute the most used language and number of repos using it
                if not languages:
                    max_language = ''
                    repos_using_max_language = 0
                else:
                    max_language = max(languages, key=languages.get)
                    repos_using_max_language = languages[max_language]

                # Calculate the age of the account in years
                created_at = data.get('created_at','')
                if created_at:
                    created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                    age_in_years = (datetime.now() - created_date).days / 365.25
                else:
                    age_in_years = 0
                # Add the data to the list
                score=calculate_score(repos, len(languages),age_in_years,total_forks)
                data_list.append({'Username': username, 'Email': email, 'Location': location, 'Followers': followers, 'Following': following, 'Public Repos': repos, 'Hireable': hirable, 'Bio': bio, 'Website': website, 'Number of Languages': len(languages), 'Languages Used': ', '.join(languages.keys()), 'Most Used Language': max_language, 'Number of Repos Using Most Used Language': repos_using_max_language, 'Age of Account (Years)': age_in_years, 'Score': score,'Total forks':total_forks})
            else:
                created_at = data.get('created_at','')
                if created_at:
                    created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                    age_in_years = (datetime.now() - created_date).days / 365.25
                else:
                    age_in_years = 0
                # Add the data to the list, with default values for language-related fields
                # Add the data to the list, with default values for language-related fields
                score=calculate_score(repos, len(languages),age_in_years,total_forks)
                data_list.append({'Username': username, 'Email': email, 'Location': location, 'Followers': followers, 'Following': following, 'Public Repos': repos, 'Hireable': hirable, 'Bio': bio, 'Website': website, 'Number of Languages': 0, 'Languages Used': '', 'Most Used Language': '', 'Number of Repos Using Most Used Language': 0,'Age of Account (Years)': age_in_years, 'Score':score,'Total forks':total_forks})


        # Write the data to the CSV file
        with open('github_info_Sans_Contri.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Email', 'Location', 'Followers', 'Following', 'Public Repos', 'Hireable', 'Bio', 'Website', 'Number of Languages', 'Languages Used', 'Most Used Language', 'Number of Repos Using Most Used Language','Age of Account (Years)','Score','Total forks'])
            for data in data_list:
                writer.writerow(data.values())
        st.success('Data written to CSV file.')

        # Display the data in a table
        df = pd.DataFrame(data_list)
        df['Score'] = df['Score'].apply(lambda x: markupsafe.Markup(f"<span style='color:green'>{x}</span>") if x > 10 else x)
        table = df[['Username', 'Score']].to_html(escape=False)

        # Center align table headers and Set table width to 100%
        table = table.replace('<th>', '<th style="text-align: center;">')
        table = table.replace('<table', '<table style="width:100%"')

        # Display table
        st.write('### Data')
        st.markdown(table, unsafe_allow_html=True)

def getuserdeets(username):
        age_in_years=0
        score=0

        # Set up the request headers
        headers = {'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'Bearer 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'}

        # Loop through each URL in the list and extract the desired information
        data_list = []
        api_url = f'https://api.github.com/users/{username}'

        # Make the request and parse the JSON response
        response = requests.get(api_url, headers=headers)
        data = response.json()

        # Extract the email, location, following, public repos, hireable status, bio, website, and language information from the JSON data
        email = data.get('email','')
        location = data.get('location','') 
        followers = data.get('followers','')
        following = data.get('following','')
        repos = data.get('public_repos','')
        hirable = data.get('hireable','') 
        bio = data.get('bio','')
        website = data.get('blog','')
        repos_url = data.get('repos_url','')
        created_at = data.get('created_at','')

        languages = {}

        # Make another request to get the user's repository information
        if repos_url:
            repos_response = requests.get(repos_url, headers=headers)
            repos_data = repos_response.json()

            languages = {}
            total_forks=0

            # Loop through each repository and extract the language information
            for repo in repos_data:
                forks_count = repo['forks_count']
                total_forks += forks_count
                if repo['language']:
                    language = repo['language']
                    if language in languages:
                        languages[language] += 1
                    else:
                        languages[language] = 1

            # Compute the most used language and number of repos using it
            if not languages:
                max_language = ''
                repos_using_max_language = 0
            else:
                max_language = max(languages, key=languages.get)
                repos_using_max_language = languages[max_language]

            # Calculate the age of the account in years
            created_at = data.get('created_at','')
            if created_at:
                created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                age_in_years = (datetime.now() - created_date).days / 365.25
            else:
                age_in_years = 0
            # Add the data to the list
            score=calculate_score(repos, len(languages),age_in_years,total_forks)
            data_list.append({'Username': username, 'Email': email, 'Location': location, 'Followers': followers, 'Following': following, 'Public Repos': repos, 'Hireable': hirable, 'Bio': bio, 'Website': website, 'Number of Languages': len(languages), 'Languages Used': ', '.join(languages.keys()), 'Most Used Language': max_language, 'Number of Repos Using Most Used Language': repos_using_max_language, 'Age of Account (Years)': age_in_years, 'Score': score,'Total Forks': total_forks})
        else:
            created_at = data.get('created_at','')
            if created_at:
                created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                age_in_years = (datetime.now() - created_date).days / 365.25
            else:
                age_in_years = 0
            # Add the data to the list, with default values for language-related fields
            # Add the data to the list, with default values for language-related fields
            score=calculate_score(repos, len(languages),age_in_years,total_forks)
            data_list.append({'Username': username, 'Email': email, 'Location': location, 'Followers': followers, 'Following': following, 'Public Repos': repos, 'Hireable': hirable, 'Bio': bio, 'Website': website, 'Number of Languages': 0, 'Languages Used': '', 'Most Used Language': '', 'Number of Repos Using Most Used Language': 0,'Age of Account (Years)': age_in_years, 'Score':score, 'Total Forks': total_forks})


        # Write the data to the CSV file
        with open('github_info_Sans_Contri.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Email', 'Location', 'Followers', 'Following', 'Public Repos', 'Hireable', 'Bio', 'Website', 'Number of Languages', 'Languages Used', 'Most Used Language', 'Number of Repos Using Most Used Language','Age of Account (Years)','Score','Total Forks'])
            for data in data_list:
                writer.writerow(data.values())
        st.success('Data written to CSV file.')

        # Display the data in a table
        df= pd.DataFrame(data_list)
        st.write('### Data')
        df['Score'] = df['Score'].apply(lambda x: markupsafe.Markup(f"<span style='color:green'>{x}</span>") if x>10 else x)
        table=df[['Username','Score']].to_html(escape=False)
        st.markdown(table, unsafe_allow_html=True)
        