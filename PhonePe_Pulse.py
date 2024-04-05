import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly_express as px
import os
import pymysql
import json
from PIL import Image


myconnection = pymysql.connect(host = 'localhost',user='root',passwd='Muthu!123*456',database = "phone", port = 3306)

cursor = myconnection.cursor()

#agg_trans:

cursor.execute('SELECT * FROM aggr_trans')
myconnection.commit()
table1 = cursor.fetchall()

Aggr_Trans1 = pd.DataFrame(table1, columns = ("State", "Year","Quater", "Transaction_type", "Transaction_count", "Transaction_amount" ))

#agg_users:

cursor.execute("select * from aggr_users")
myconnection.commit()
table2 = cursor.fetchall()

Aggr_Users1 = pd.DataFrame(table2, columns = ("State", "Year","Quater", "Brand", "Transaction_count", "Percentage" ))

#map_Trans:

cursor.execute("select * from map_tr")
myconnection.commit()
table3 = cursor.fetchall()

Map_Trans1 = pd.DataFrame(table3, columns = ("State", "Year","Quater", "District_Name", "Transaction_count", "Transaction_amount" ))

#map_Users:

cursor.execute("select * from map_us")
myconnection.commit()
table4 = cursor.fetchall()

Map_Users1 = pd.DataFrame(table4, columns = ("State", "Year","Quater", "District_Name", "Registered_Users", "App_opens" ))


#Top_Trans:

cursor.execute("select * from top_tr")
myconnection.commit()
table5 = cursor.fetchall()

Top_Trans1 = pd.DataFrame(table5, columns = ("State", "Year","Quater", "Pincodes", "Transaction_count", "Transaction_amount" ))


#Top_USers:

cursor.execute("select * from top_us")
myconnection.commit()
table6 = cursor.fetchall()

Top_Users1 = pd.DataFrame(table6, columns = ("State", "Year","Quater", "District_Name", "Transaction_count"))



def Transaction_Trans_User(df, year):

    ta1 =df[df['Year']== year]
    ta1.reset_index(drop=True, inplace=True)

    ta2 = ta1.groupby("State")[["Transaction_amount","Transaction_count"]].sum()
    ta2.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:


        fig_amount = px.bar(ta2, x = "State", y= "Transaction_amount", title=f"{year} Transaction_Amount", color_discrete_sequence=px.colors.sequential.BuGn_r)
        st.plotly_chart(fig_amount)

    with col2:


        fig_count = px.bar(ta2, x = "State", y= "Transaction_count", title=f"{year} Transaction_Count",color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    return ta1


def Transaction_Trans_geo(df,year):

    tab1 =df[df['Year']== year]
    tab1.reset_index(drop=True, inplace=True)

    tab2 = tab1.groupby("State")[["Transaction_amount","Transaction_count"]].sum()
    tab2.reset_index(inplace=True)



    fig = px.choropleth(df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey = "properties.ST_NM",
                            locations = "State",
                            color = 'Transaction_amount',
                            color_continuous_scale= "Reds",
                            hover_name="State",
                            fitbounds = "locations",
                            title= f"{year}Transaction_Amount")

    fig.update_geos(visible = False)
    st.plotly_chart(fig)

def Transaction_Count_geo(df,year):

    tab1 =df[df['Year']== year]
    tab1.reset_index(drop=True, inplace=True)

    tab2 = tab1.groupby("State")[["Transaction_amount","Transaction_count"]].sum()
    tab2.reset_index(inplace=True)


    fig = px.choropleth(df,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey = "properties.ST_NM",
                        locations = "State",
                        color = 'Transaction_count',
                        color_continuous_scale= "greens",
                        hover_name="State",
                        fitbounds = "locations",
                        title= f"{year}Transaction_Count")

    fig.update_geos(visible = False)
    st.plotly_chart(fig)



def Transaction_Trans_Aggr(df, Year, Quater):

    tab1 =df[(df['Year']== Year)  & (df["Quater"]== Quater)]
    tab1.reset_index(drop=True, inplace=True)

    tab2 = tab1.groupby("State")[["Transaction_amount","Transaction_count"]].sum()
    tab2.reset_index(inplace=True)

    fig_amount = px.bar(tab2, x = "State", y= "Transaction_amount", title=f"{Year} AND {Quater}Transaction_Amount", color_discrete_sequence=px.colors.sequential.BuGn_r)
    st.plotly_chart(fig_amount)


    fig_count = px.bar(tab2, x = "State", y= "Transaction_count", title=f"{Year} AND {Quater}Transaction_Count",color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_count)


def Transaction_User_Aggr(df, Year, Quater):

    tab1 =df[(df['Year']== Year)  & (df["Quater"]== Quater)]
    tab1.reset_index(drop=True, inplace=True)

    tab2 = tab1.groupby("Brand")[["Percentage","Transaction_count"]].sum()
    tab2.reset_index(inplace=True)

    fig_count = px.pie(df, names= "Brand",  title=" Brand Names & count", values="Transaction_count", width=600, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_count)

    fig_per = px.pie(df, names= "Brand",  title=" Brand Names & Percentage", values="Percentage", width=600, color_discrete_sequence=px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig_per)


def Transaction_User_Map(df, Year, Quater):

    tab1 =df[(df['Year']== Year)  & (df["Quater"]== Quater)]
    tab1.reset_index(drop=True, inplace=True)

    tab2 = tab1.groupby("State")[["Registered_Users","App_opens"]].sum()
    tab2.reset_index(inplace=True)

    fig_regist_user = px.pie(df, names= "State",  title=" State Wise Registered Users", values="Registered_Users", width=800,height=800, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_regist_user)


    fig_App_opens = px.pie(df, names= "State",  title=" State Wise App_Opens", values="App_opens", width=800,height=800, color_discrete_sequence=px.colors.sequential.Darkmint)
    st.plotly_chart(fig_App_opens)



def states_names(df,State):

    df33 = df[df["State"] == State]
    df33.reset_index(drop = True, inplace =True)

    df34 = df33.groupby("Transaction_type")[["Transaction_amount","Transaction_count"]].sum()
    df34.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:

        fig_pie_1 = px.pie(data_frame = df34, names="Transaction_type", values="Transaction_amount", width = 600, color_discrete_sequence=px.colors.sequential.Aggrnyl,
                    title=f"{"State".upper()} TRANSACTION AMOUNT", hole = 0.5)

        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2 = px.pie(data_frame = df34, names="Transaction_type", values="Transaction_count", width = 600, color_discrete_sequence=px.colors.sequential.Blugrn,
                    title=f"{"State".upper()} TRANSACTION COUNT", hole = 0.5)
        st.plotly_chart(fig_pie_2)


#Top 10 Brands:
    
def Top_10_Brands_users(Table):

    cursor.execute(f'''select Brand, AVG(Transaction_count) from {Table}
                group by Brand
                    order by Brand desc limit 10
                        ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df_12 = pd.DataFrame(table5, columns= ("Brand", "Transaction count"))

    fig_count = px.pie(df_12, names= "Brand",  title=" Top 10 Brands", values="Transaction count", width=600, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_count)

#Top 10 Pincodes:

def Top_10_State_pincode(Table):

    cursor.execute(f'''select Pincodes, AVG(Transaction_Amount) from {Table}
                group by Pincodes
                    order by Pincodes desc limit 10
                        ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df_12 = pd.DataFrame(table5, columns= ("Pincodes", "Transaction amount"))

    fig_pin = px.pie(df_12, names= "Pincodes",  title=" Top 10 Pincodes", values="Transaction amount", width=600, color_discrete_sequence=px.colors.sequential.RdPu_r)
    st.plotly_chart(fig_pin)

#Top 10 States Transaction amount:

def Top_10_state_trans(Table):

    cursor.execute(f'''select State, AVG(Transaction_Amount) from {Table}
                group by State
                    order by State desc limit 10
                        ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df_12 = pd.DataFrame(table5, columns= ("State", "Transaction amount"))

    fig_state = px.pie(df_12, names= "State",  title=" Top 10 State", values="Transaction amount", width=600, color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_state)


#Top payments type:

def Top_10_Payment_Type(Table):

    cursor.execute(f'''Select Transaction_type, SUM(Transaction_amount) AS transaction_amount from {Table}
                        GROUP BY  Transaction_type
                        ORDER BY Transaction_amount desc
                        limit 10;
                        ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df123 = pd.DataFrame(table5, columns=("Transaction_Type", "Transaction_Amount"))

    fig_pay_type = px.pie(df123, names= "Transaction_Type",  title=" Top Transaction type", values="Transaction_Amount", width=600, color_discrete_sequence=px.colors.sequential.Agsunset_r)
    st.plotly_chart(fig_pay_type)





#question 1 :

#aggr top 10 Trans:


def Top_10_Trans_counts(Table):

    cursor.execute(f'''Select State, SUM(Transaction_amount) AS transaction_amount from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_amount desc
                    limit 10''')

    myconnection.commit()
    table2 = cursor.fetchall()

    df_1 = pd.DataFrame(table2, columns = ("State", "Transaction_amount" ))
    
    col1, col2 = st.columns(2)

    with col1:

        fig_amount = px.histogram(df_1, x = "State", y= "Transaction_amount", title=" Transaction_Amount", width=500, color_discrete_sequence=px.colors.sequential.haline)
        st.plotly_chart(fig_amount)

    #aggr top10 counts:

    cursor.execute(f'''Select State, SUM(Transaction_count) AS transaction_count from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_count desc
                    limit 10''')

    myconnection.commit()
    table1 = cursor.fetchall()

    df_11 = pd.DataFrame(table1, columns = ("State", "Transaction_count" ))
    
    with col2:

        fig_count = px.histogram(df_11, x = "State", y= "Transaction_count", title=" Transaction_count", width=500, color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_count)


#question 2:


#aggr least 10 Trans:

def Least_10_Trans_Counts(Table):

    cursor.execute(f'''Select State, SUM(Transaction_amount) AS transaction_amount from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_amount
                    limit 10''')

    myconnection.commit()
    table2 = cursor.fetchall()

    df_1 = pd.DataFrame(table2, columns = ("State", "Transaction_amount" ))

    col1, col2 = st.columns(2)

    with col1:

        fig_amount = px.histogram(df_1, x = "State", y= "Transaction_amount", title=" Transaction_Amount", width=500, color_discrete_sequence=px.colors.sequential.GnBu)
        st.plotly_chart(fig_amount)



    cursor.execute(f'''Select State, SUM(Transaction_count) AS transaction_count from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_count 
                    limit 10''')

    myconnection.commit()
    table1 = cursor.fetchall()

    df_11 = pd.DataFrame(table1, columns = ("State", "Transaction_count" ))

    with col2:

        fig_count = px.histogram(df_11, x = "State", y= "Transaction_count", title=" Transaction_count", width=500, color_discrete_sequence=px.colors.sequential.Oryel_r)
        st.plotly_chart(fig_count)


#Question 3

#36states trans :

def State_36_Trans(Table):

    cursor.execute(f'''Select State, SUM(Transaction_amount) AS transaction_amount from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_amount
                    ''')

    myconnection.commit()
    table2 = cursor.fetchall()

    df_1 = pd.DataFrame(table2, columns = ("State", "Transaction_amount" ))

    fig_amount = px.histogram(df_1, x = "State", y= "Transaction_amount", title=" Transaction_Amount", color_discrete_sequence=px.colors.sequential.Inferno_r)
    st.plotly_chart(fig_amount)

#Qustion 4

#aggr counts for 36 states:

def State_36_Counts(Table):

    cursor.execute(f'''Select State, SUM(Transaction_count) AS transaction_count from {Table}
                    GROUP BY  State
                    ORDER BY Transaction_count desc
                    ''')

    myconnection.commit()
    table1 = cursor.fetchall()

    df_11 = pd.DataFrame(table1, columns = ("State", "Transaction_count" ))

    fig_count = px.bar(df_11, x = "State", y= "Transaction_count", title=" Transaction_count",  color_discrete_sequence=px.colors.sequential.PuBuGn_r)
    st.plotly_chart(fig_count)


#Question 5


#Top 10 Registered users:

def Top_registered_users(Table, state):

    cursor.execute(f'''select District_Name, SUM(Registered_Users) as registeredusers from {Table}
                    where State = '{state}'
                    group by District_Name
                    ORDER BY registeredusers desc
                LIMIT 10 ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df124 = pd.DataFrame(table5, columns=("District Name", "registered Users"))

    fig_reg = px.bar(df124, x = "District Name", y= "registered Users", title="Top 10 Registered Users", color_discrete_sequence=px.colors.sequential.turbid)
    st.plotly_chart(fig_reg)


#Question 6

#Least 10 Registered users:

def Least_10_registered_user(Table, state):

    cursor.execute(f'''select District_Name, SUM(Registered_Users) as registeredusers from {Table}
                    where State = '{state}'
                    group by District_Name
                    ORDER BY registeredusers
                LIMIT 10 ''')


    myconnection.commit()
    table5 = cursor.fetchall()

    df124 = pd.DataFrame(table5, columns=("District Name", "registered Users"))

    fig_reg = px.bar(df124, x = "District Name", y= "registered Users", title="Top 10 Registered Users", color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_reg)

#Question 7

#Top 10 App Opens:

def Top_10_App_opnes(Table, state):

    cursor.execute(f'''select District_Name, SUM(App_opens) as App_Opens from {Table}
                    where State = '{state}'
                    group by District_Name
                    ORDER BY App_Opens desc
                LIMIT 10 ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df124 = pd.DataFrame(table5, columns=("District Name", "App Opens"))

    fig_app = px.bar(df124, x = "District Name", y= "App Opens", title="Top 10 App Opens", color_discrete_sequence=px.colors.sequential.OrRd_r)
    st.plotly_chart(fig_app)

#Question 8

#Least 10 App Opens:

def Least_10_App_opnes(Table, state):

    cursor.execute(f'''select District_Name, SUM(App_opens) as App_Opens from {Table}
                    where State = '{state}'
                    group by District_Name
                    ORDER BY App_Opens 
                LIMIT 10 ''')

    myconnection.commit()
    table5 = cursor.fetchall()

    df124 = pd.DataFrame(table5, columns=("District Name", "App Opens"))

    fig_app = px.bar(df124, x = "District Name", y= "App Opens", title="Top 10 App Opens", color_discrete_sequence=px.colors.sequential.Burgyl)
    st.plotly_chart(fig_app)


st.set_page_config(layout="wide")
st.sidebar.header(":orange[Data] :violet[Visualization]")

options = st.sidebar.radio(("Pick your option"),("HOME","GEO-MAP","TRANSACTION", "USER","TOP CHARTS", "INSIGHTS" ) )


if options == "HOME":

    st.title(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]") 

    st.caption('''The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.

When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?
This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.

This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.

PhonePe Pulse is your window to the world of how India transacts with interesting trends, 
deep insights and in-depth analysis based on our data put together by the PhonePe team.''')
    
    st.image(Image.open(r"C:\Users\ADMIN\Downloads\muthu doc\phonePe.jpg"), width = 300)


if options == "GEO-MAP":

     Year = st.sidebar.slider("Select the year", Aggr_Trans1["Year"].min(), Aggr_Trans1["Year"].max()),
    #ans= Transaction_Trans_User(Aggr_Trans1,Year)
     
     st.title(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]") 
     st.subheader(":green[OVERALL STATE DATA- TRANSACTION DETAILS]", divider='rainbow')


     Transaction_Trans_geo(Aggr_Trans1, Year)
     st.subheader(":orange[OVERALL STATE DATA- COUNT DETAILS]", divider='rainbow')
     Transaction_Count_geo(Aggr_Trans1, Year)

     



if options == "TRANSACTION":

    Year = st.sidebar.slider("Select the year", Aggr_Trans1["Year"].min(), Aggr_Trans1["Year"].max()),
    
   
    quater = st.sidebar.slider("Select the Quater", Aggr_Trans1["Quater"].min(), Aggr_Trans1["Quater"].max()),
   
    st.header(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]")

    st.subheader(":blue[Statewise Total Transaction and count - Details]", divider='rainbow')
    Transaction_Trans_Aggr(Aggr_Trans1,Year,quater)
    

if options == "USER":


     Year = st.sidebar.slider("Select the year", Aggr_Trans1["Year"].min(), Aggr_Trans1["Year"].max()),
    #ans= Transaction_Trans_User(Aggr_Trans1,Year)
   
     quater = st.sidebar.slider("Select the Quater", Aggr_Trans1["Quater"].min(), Aggr_Trans1["Quater"].max()),
    #Transaction_Trans_User_Q(ans, quater)
     
     st.header(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]")
     st.subheader(":green[Registered Users and App opens details in Statewise]", divider='rainbow')
     Transaction_User_Map(Map_Users1, Year, quater)

     st.subheader(":green[Top Brand names and percentage details in statewise]", divider='rainbow')
     Transaction_User_Aggr(Aggr_Users1, Year, quater)


if options == "TOP CHARTS":

    st.header(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]")

    st.subheader(":violet[Top 10 Data's for Transaction and Users - Details]", divider='rainbow')

    Top_10_Brands_users("aggr_users")

    Top_10_State_pincode("top_tr")

    Top_10_state_trans("aggr_trans")

    Top_10_Payment_Type("aggr_trans")


if options == "INSIGHTS":

    st.header(":red[PHONEPE DATA VISUALIZATION & EXPLORATION]")

    st.subheader("Overall Transaction Type - Details ")

    Year = st.slider("Select the year", Aggr_Trans1["Year"].min(), Aggr_Trans1["Year"].max()),
    ans= Transaction_Trans_User(Aggr_Trans1,Year)

    states = st.selectbox("Select the state", ans["State"].unique())
    states_names(ans, states)



    

    Question = st.selectbox("Choose your question", ["1. Top 10 Transaction amount and Counts details",
                                                     "2. Least 10 Transaction amount and Counts details",
                                                     "3. 36 States Transcation amounts Details",
                                                     "4. 36 States Transaction counts details",
                                                     "5. Top 10 Regsitered users details",
                                                     "6. Least 10 Registered users details",
                                                     "7. Top 10 App openers details",
                                                     "8. Least 10 App openers details"])
    
    if Question == "1. Top 10 Transaction amount and Counts details":

        Top_10_Trans_counts("aggr_trans")
    
    elif Question == "2. Least 10 Transaction amount and Counts details":

        Least_10_Trans_Counts("aggr_trans")

    elif Question == "3. 36 States Transcation amounts Details":

        State_36_Trans("aggr_trans")
    
    elif Question == "4. 36 States Transaction counts details":

        State_36_Counts("aggr_trans")

    elif Question == "5. Top 10 Regsitered users details":
        states = st.selectbox("Select the state", Map_Users1["State"].unique())
        Top_registered_users("map_us",states )


    elif Question == "6. Least 10 Registered users details":
        states = st.selectbox("Select the state", Map_Users1["State"].unique())
        Least_10_registered_user("map_us",states)

    elif Question == "7. Top 10 App openers details":
        states = st.selectbox("Select the state", Map_Users1["State"].unique())
        Top_10_App_opnes("map_us", states)

    elif Question == "8. Least 10 App openers details":
        states = st.selectbox("Select the state", Map_Users1["State"].unique())
        Least_10_App_opnes("map_us", states)











 
    
    


    
 
