import streamlit as st
import requests

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
    
        
        col1,col2,col3=st.columns([0.2,0.6,0.2],border=True)
        col1.metric(label=" Followers",value=git_user_data["followers"])
        col2.metric(label="Started on",value=str(git_user_data['created_at'])[:10])
        col3.metric(label="Repositories",value=git_user_data["public_repos"])
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

     
    






