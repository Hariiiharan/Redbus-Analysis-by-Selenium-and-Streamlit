# importing libraries
import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import time

#creating list for all states from csv file:

# Kerala bus
lists_k=[]
df_k=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\kerala_buses.csv")
for i,r in df_k.iterrows():
    lists_k.append(r["route_name"])

# Telangana bus
lists_t=[]
df_t=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\tsrtc_buses.csv")
for i,r in df_t.iterrows():
    lists_t.append(r["route_name"])

# Andhra pradesh bus
lists_a=[]
df_a=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\apsrtc_buses.csv")
for i,r in df_a.iterrows():
    lists_a.append(r["route_name"])


# Rajasthan bus
lists_r=[]
df_r=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\rsrtc_buses.csv")
for i,r in df_r.iterrows():
    lists_r.append(r["route_name"])


# South Bengal bus
lists_sb=[]
df_sb=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\sbstc_buses.csv")
for i,r in df_sb.iterrows():
    lists_sb.append(r["route_name"])


# Himachal bus
lists_h=[]
df_h=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\hrtc_buses.csv")
for i,r in df_h.iterrows():
    lists_h.append(r["route_name"])


# Assam bus
lists_as=[]
df_as=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\astc_buses.csv")
for i,r in df_as.iterrows():
    lists_as.append(r["route_name"])


# CHANDIGARH bus
lists_c=[]
df_c=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\ctu_buses.csv")
for i,r in df_c.iterrows():
    lists_c.append(r["route_name"])


# punjab bus
lists_p=[]
df_p=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\pepsu_buses.csv")
for i,r in df_p.iterrows():
    lists_p.append(r["route_name"])

# Bihar bus
lists_b=[]
df_b=pd.read_csv(r"C:\Users\haris\OneDrive\Documents\hariii_note\Project 1\bsrtc_buses.csv")
for i,r in df_b.iterrows():
    lists_b.append(r["route_name"])



#setting up streamlit page

st.set_page_config(layout="wide")
st.image(r"C:\Users\haris\Downloads\redbus.png", width=200)

web=option_menu(menu_title="🚌 Welcome .... Enjoy your bookings ",
                options=["Home","States and Routes"],
                icons=["house","info-circle"],
                orientation="horizontal"
                )

# Home page setting
if web == "Home":
    
    st.title("Redbus Data Insights with Streamlit")
    
    st.header("🚀 Project Overview")
    st.subheader("Domain: Transportation")
    
    st.markdown(
        """
        Welcome to the Redbus Data Insights app! This tool uses Selenium for web scraping to gather bus travel data from Redbus, including routes, schedules, and fares. With a user-friendly Streamlit interface, you can easily visualize and filter this data to support better decision-making.
        """
    )
    
    st.subheader("🔧 Technologies Used")
    
    st.markdown(
        """
        - **Selenium**: Automates web browsing for data extraction.
        - **Pandas**: Processes and analyzes data.
        - **MySQL**: Stores and manages data.
        - **Streamlit**: Creates interactive web applications.
        """
    )
    
    st.subheader("🛠️ Skills Acquired")
    st.markdown("Learn Selenium, Python, Pandas, MySQL, and Streamlit.")
    
    st.subheader("👤 Developed by")
    st.markdown("HARIHARAN M")


 

# States and Routes page setting
if web == "States and Routes":
    S = st.selectbox("Lists of States", [ "Telangana", "Adhra Pradesh", "Kerala", "Rajasthan","Himachal",
                                          "South Bengal","Assam", "Chandigarh", "Punjab", "Bihar"])
    
    col1,col2=st.columns(2)
    with col1:
        select_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
        TIME=st.time_input("select the time")

 # telangana bus fare filtering
    if S == "Telangana":
        T = st.selectbox("List of routes",lists_t)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()

            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{T}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "duration","reaching_time",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)

        st.dataframe(df_result)

   # Adhra Pradesh bus fare filtering
    if S=="Adhra Pradesh":
        A=st.selectbox("list of routes",lists_a)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{A}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)


    # kerala bus fare filtering
    if S=="Kerala":
        K=st.selectbox("list of routes",lists_k)
        
        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{K}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

    # RAJASTHAN bus fare filtering

    if S=="Rajasthan":
        R=st.selectbox("list of routes",lists_r)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{R}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)



    # South Bengal bus fare filtering       
    if S=="South Bengal":
        SB=st.selectbox("list of rotes",lists_sb)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{SB}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

    # Himachal bus fare filtering
    if S=="Himachal":
        H=st.selectbox("list of rotes",lists_h)
    
        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{H}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

        # Assam bus fare filtering
    if S=="Assam":
        AS=st.selectbox("list of rotes",lists_as)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{AS}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

    
    # Chandigarh bus fare filtering
    if S=="Chandigarh":
        C=st.selectbox("list of rotes",lists_c)

        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{C}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

    
    # Punjab bus fare filtering
    if S=="Punjab":
        P=st.selectbox("list of rotes",lists_p)

    
        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{P}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

      # Bihar bus fare filtering
    if S=="Bihar":
        B=st.selectbox("list of rotes",lists_b)
        def type_and_fare(bus_type, fare_range):
            conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {fare_min} AND {fare_max}
                AND route_name = "{B}"
                AND {bus_type_condition} AND departure_time>='{TIME}'
                ORDER BY price and departure_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "bus_name", "bus_type", "departure_time", "reaching_time", "duration",
                "price", "seat_availability", "star_rating", "route_link", "route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare)
        st.dataframe(df_result)

    

        
      






   













