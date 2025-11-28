import streamlit as st
import requests
import google.generativeai as genai
import datetime


api_keyy=st.secrets["Google_API_KEY"]
genai.configure(api_key=api_keyy)
model=genai.GenerativeModel("gemini-flash-lite-latest")

git_username=st.text_input("Enter github")
if git_username:
    url=f"https://api.github.com/users/{git_username}"
    r=requests.get(url)
    
    if r.status_code==200:
        git_user_data=r.json()
        repo_url=requests.get(git_user_data["repos_url"])
        repo_data=repo_url.json()
        totalrepos=len(repo_data)
        forkedrepo=0
        selfrepo=0
        for repo in repo_data:
            if repo["fork"]==True:
                forkedrepo+=1
            else:
                selfrepo+=1
    
        
        col1,col2,col3,col4=st.columns([0.2,0.3,0.2,0.3],border=True)
        col1.metric(label=" Followers",value=git_user_data["followers"])
        col2.metric(label="Started on",value=str(git_user_data['created_at'])[:10])
        col3.metric(label="Repositories",value=git_user_data["public_repos"])
        col4.metric(label="Updated at",value=str(git_user_data["updated_at"])[:10])

        tod=datetime.datetime.now()
        last_update=str(git_user_data["updated_at"][:10])
        date_format="%Y-%m-%d"
        last_date=datetime.datetime.strptime(last_update , date_format)
        time_difference=tod-last_date
        days_between=time_difference.days
        st.write(f"DAYS INACTIVE:{days_between}")
        # --- LOGIC: The "Kill Shot" Prompt ---
        roast_prompt = f"""
        You are "COOKED," a ruthless AI roaster who hates bad code. 
        Your job is to roast this GitHub user based on their real stats. Be mean, funny, and use Gen-Z slang (cooked, washed, npc, glaze).

        Here is the victim's data:
        - Bio: "{git_user_data['bio']}"
        - Followers: {git_user_data['followers']} (If low, roast them for having no clout)
        - Total Repos: {totalrepos}
        - Real Projects: {selfrepo}
        - Forked (Stolen) Repos: {forkedrepo}
        - Days Since Last Code Push: {days_between}

        SPECIFIC RULES:
        1. If "Days Since Last Code Push" is > 30, ask if they quit coding. If > 100, call them a "retired dev".
        2. If "Forked Repos" is higher than "Real Projects", call them out with a funny name for stealing it.
        3. If they have 0 Real Projects, ask them why they even have a GitHub account.
        4. Roast their Bio specifically if it's cringe.
        5. Keep it under 100 words. Brutal honesty only.
        6. If the data is insuffiecient roast em however u want but dont disrespect em , just roast em brutal that it burns in the ass.
        """

        # --- LOGIC: Pull the Trigger ---
        response = model.generate_content(roast_prompt)

        # --- LOGIC: Show the Damage ---
        st.divider() # Adds a nice line
        st.subheader("🔥 THE VERDICT")
        st.write(response.text)

        if totalrepos==0:
            st.write("CODING BHI KARLE BHAI LITERALLY ZERO REPOS")
        st.write("---------------------")
        st.subheader("BIO")
        a=(git_user_data["bio"])
        st.write(a)
        if a==None:
            st.write("NOTHING TO TELL BOUT URSELF ! NIGGA")

        
        
    elif r.status_code==404:
        st.write("Are u trying to search for a ghost brotha? Check for a valid username ")
    else :
        st.write(f"Things go wrong daily this time it's status is {r.status_code}")

     
    






