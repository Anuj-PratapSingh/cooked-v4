import streamlit as st
import requests
import google.generativeai as genai

apikeyy=st.secrets["Google_API_KEY_chess"]
genai.configure(api_key=apikeyy)
model=genai.GenerativeModel("gemini-flash-lite-latest")

chess_name=st.text_input("Enter your username")
if chess_name:
    url=f"https://api.chess.com/pub/player/{chess_name}/stats"
    header={"User-Agent":"Mozilla/5.0","username":f"{chess_name}"}
    response=requests.get(url,headers=header)


    if response.status_code==200:
        UserData=response.json()
        st.header("The Data")
        st.write("----")
        #box wali design ka code
        d1,d2,d3=st.columns(spec=3,border=True)
        r1,r2,r3=st.columns(3,border=True)
        blt1,blt2,blt3=st.columns(3,border=True)
        bltz1,bltz2,bltz3=st.columns(3,border=True)


        #daily mode stats chess ke records , rating , win , loss , draws
        dailyrating=UserData.get("chess_daily",{}).get("last",{}).get("rating",0)
        dailywins=UserData.get("chess_daily",{}).get("record",{}).get("win",0)
        dailyloss=UserData.get("chess_daily",{}).get("record",{}).get("loss",0)
        dailydraw=UserData.get("chess_daily",{}).get("record",{}).get("draw",0)
        totalmatchesdaily=int(dailyloss+dailywins+dailydraw)
        if totalmatchesdaily>0:
            wlratiodaily=f"{(dailywins+(0.5*dailydraw))/totalmatchesdaily:.2f}"
        else:
            wlratiodaily="NO DATA"
        #rapid mode ke stats with rating win loss draws
        rapidrating=UserData.get("chess_rapid",{}).get("last",{}).get("rating",0)
        rapidwins=UserData.get("chess_rapid",{}).get("record",{}).get("win",0)
        rapidloss=UserData.get("chess_rapid",{}).get("record",{}).get("loss",0)
        rapiddraw=UserData.get("chess_rapid",{}).get("record",{}).get("draw",0)
        totalrapidmatches=int(rapidwins+rapidloss+rapiddraw)
        if totalrapidmatches>0:
            wlratiorapid=f"{(rapidwins+(0.5*rapiddraw))/totalrapidmatches:.2f}"
        else:
            wlratiorapid="NO DATA"
        #bullet mode ke stats with rating win loss draws
        bulletrating=UserData.get("chess_bullet",{}).get("last",{}).get("rating",0)
        bulletwins=UserData.get("chess_bullet",{}).get("record",{}).get("win",0)
        bulletlost=UserData.get("chess_bullet",{}).get("record",{}).get("loss",0)
        bulletdraw=UserData.get("chess_bullet",{}).get("record",{}).get("draw",0)
        totalbulletmatches=int(bulletwins+bulletlost+bulletdraw)
        if totalbulletmatches>0:
            wlratiobullet=f"{(bulletwins+(0.5*bulletdraw))/totalbulletmatches:.2f}"
        else:
            wlratiobullet="NO DATA"  
        #blitz mode ke stats with rating win loss draws
        blitzrating=UserData.get("chess_blitz",{}).get("last",{}).get("rating",0)
        blitzwins=UserData.get("chess_blitz",{}).get("record",{}).get("win",0)
        blitzloss=UserData.get("chess_blitz",{}).get("record",{}).get("loss",0)
        blitzdraw=UserData.get("chess_blitz",{}).get("record",{}).get("draw",0)
        totalblitzmatches=int(blitzwins+blitzloss+blitzdraw)
        if totalblitzmatches>0:
            wlratioblitz=f"{(blitzwins+(0.5*blitzdraw))/totalblitzmatches:.2f}"
        else:
            wlratioblitz="NO DATA"
     
        
        #daily data dabbe
        d1.metric(label="Daily Rating",value=dailyrating,border=True)
        d2.metric(label="Win Rate", value=wlratiodaily,border=True)
        d3.metric(label="Total",value=totalmatchesdaily,border=True)

        #rapid data dabbe
        r1.metric(label="Rapid Rating",value=rapidrating,border=True)
        r2.metric(label="Win Rate",value=wlratiorapid,border=True)
        r3.metric(label="Total games played",value=totalrapidmatches,border=True)

        #bullet data ke dabbe lol
        blt1.metric(label="Bullet Wins",value=bulletrating,border=True)
        blt2.metric(label="Win Rate",value=wlratiobullet,border=True)
        blt3.metric(label="Total games played",value=totalbulletmatches,border=True)

        #blitz data ke dabbe lol
        bltz1.metric(label="Blitz Rating",value=blitzrating,border=True)
        bltz2.metric(label="Win Rate",value=wlratioblitz,border=True)
        bltz3.metric(label="Total games played",value=totalblitzmatches,border=True)

        roast_prompt=f'''U r a retired pro chess grandmaster genius and nowadays u roast people's profiles
        The roast instructions are as follows:
       -- Roast them while using genz slang and popular chess memes
        --Use their data that has daily rating: {dailyrating}, win rate:{wlratiodaily},draws:{totalmatchesdaily}
        For bullet mode; rating:{bulletrating},win rate:{wlratiobullet},totalmatches:{totalbulletmatches}
        for blitz mode: rating:{blitzrating},win rate:{wlratioblitz},totalmatches:{totalblitzmatches}
        for rapid mode : rating:{rapidrating},win rate:{wlratiorapid},totalmatches:{totalrapidmatches}
       -- call them out if they have too low win rate i.e. less than 0.50 
       -- call them out if they play too much bullet than anything , make a funny name for it in genz slag
       --roast em if one of their mode is played tooo much and call them a funny name for that too
       --call them names and roast their profile , if the stats are rookie , tell them to touch grass or similar as chess is not for them or similar
       keep it all under 200 words'''
        

        r=model.generate_content(roast_prompt)
        st.divider()
        st.subheader("THE VERDICT 🔥🔥🔥🔥")
        st.write(r.text)


       


        



        

    elif response.status_code==404:
        st.write("U Searching for ur crush.... Maybe she lied bout her username tho.")
    else :
        st.write(f"Mistakes happens and so do connection errors. Come later we might fix it by then.ERROR CODE IS {response.status_code}")













