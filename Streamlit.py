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
    S = st.selectbox("Lists of States", [ "Telangana", "Adhra Pradesh", "Kerala", "Rajasthan", "Himachal",
                                          "South Bengal", "Assam", "Chandigarh", "Punjab", "Bihar"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        select_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = st.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    with col3:
        select_rating = st.radio("Choose star rating", ("All","1", "2", "3", "4", "5"))

    # Time Filters
        departure_time_filter = st.selectbox("Departure Time", ["All","Before 6 am", "6 am to 12 pm", "12 pm to 6 pm", "After 6 pm"])
        arrival_time_filter = st.selectbox("Arrival Time", ["All", "Before 6 am", "6 am to 12 pm", "12 pm to 6 pm", "After 6 pm"])

    # Define time ranges based on the selection
        time_ranges = {
        "Before 6 am": ("00:00:00", "06:00:00"),
        "6 am to 12 pm": ("06:00:00", "12:00:00"),
        "12 pm to 6 pm": ("12:00:00", "18:00:00"),
        "After 6 pm": ("18:00:00", "23:59:59")
         }

    # Initialize time ranges
    dep_start, dep_end = time_ranges.get(departure_time_filter, ("00:00:00", "23:59:59"))
    arr_start, arr_end = time_ranges.get(arrival_time_filter, ("00:00:00", "23:59:59"))

    # telangana bus fare filtering

    if S == "Telangana":
        
        # Ensure lists_t contains unique route names
        unique_routes_t = list(set(lists_t))  # Remove duplicates
    
        # Display unique routes in the selectbox
        T = st.selectbox("List of routes", unique_routes_t)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{T}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)




  #"Adhra Pradesh" bus fare filtering         

    if S == "Adhra Pradesh":

        # Ensure lists_a contains unique route names
        unique_routes_a = list(set(lists_a))  # Remove duplicates
    
        # Display unique routes in the selectbox
        A = st.selectbox("List of routes", unique_routes_a)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{A}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)


    # kerala bus fare filtering
    if S=="Kerala":

        # Ensure lists_k contains unique route names
        unique_routes_k = list(set(lists_k))  # Remove duplicates
    
        # Display unique routes in the selectbox
        K = st.selectbox("List of routes", unique_routes_k)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{K}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)
        

    # RAJASTHAN bus fare filtering

    if S=="Rajasthan":

        # Ensure lists_t contains unique route names
        unique_routes_r = list(set(lists_r))  # Remove duplicates
    
        # Display unique routes in the selectbox
        R = st.selectbox("List of routes", unique_routes_r)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{R}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)

        

    # South Bengal bus fare filtering       
    if S=="South Bengal":

        # Ensure lists_sb contains unique route names
        unique_routes_sb = list(set(lists_sb))  # Remove duplicates
    
        # Display unique routes in the selectbox
        SB = st.selectbox("List of routes", unique_routes_sb)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{SB}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)
    
    # Himachal bus fare filtering
    if S=="Himachal":
 
        # Ensure lists_h contains unique route names
        unique_routes_h = list(set(lists_h))  # Remove duplicates
    
        # Display unique routes in the selectbox
        H = st.selectbox("List of routes", unique_routes_h)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{H}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)

    

     # Assam bus fare filtering
    if S=="Assam":

        # Ensure lists_aS contains unique route names
        unique_routes_as = list(set(lists_as))  # Remove duplicates
    
        # Display unique routes in the selectbox
        AS = st.selectbox("List of routes", unique_routes_as)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{AS}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)
        
               
    
    # Chandigarh bus fare filtering
    if S=="Chandigarh":

        # Ensure lists_t contains unique route names
        unique_routes_c= list(set(lists_c))  # Remove duplicates
    
        # Display unique routes in the selectbox
        C = st.selectbox("List of routes", unique_routes_c)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{C}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)
        
    
    # Punjab bus fare filtering
    if S=="Punjab":

        # Ensure lists_p contains unique route names
        unique_routes_p = list(set(lists_p))  # Remove duplicates
    
        # Display unique routes in the selectbox
        P = st.selectbox("List of routes", unique_routes_p)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{P}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)

      # Bihar bus fare filtering
    if S=="Bihar":
    

        # Ensure lists_b contains unique route names
        unique_routes_b= list(set(lists_b))  # Remove duplicates
    
        # Display unique routes in the selectbox
        B = st.selectbox("List of routes", unique_routes_b)

        # Establish a connection to the MySQL database

        conn = mysql.connector.connect(host="localhost", user="root", password="H@ridhoni7", database="red_bus")
        my_cursor = conn.cursor() 

        # Define fare range based on selection
        if select_fare == "50-1000":
            fare_min, fare_max = 50, 1000
        elif select_fare == "1000-2000":
            fare_min, fare_max = 1000, 2000
        else:
            fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

        # Define bus type condition
        if select_type == "sleeper":
            bus_type_condition = "bus_type LIKE '%Sleeper%'"
        elif select_type == "semi-sleeper":
            bus_type_condition = "bus_type LIKE '%A/c Semi Sleeper %'"
        else:
            bus_type_condition = "bus_type NOT LIKE '%Sleeper%' AND bus_type NOT LIKE '%Semi-Sleeper%'"

        # Define star rating condition
        if select_rating == "All":
            star_rating_condition = "star_rating BETWEEN 1 AND 5"  # Includes all ratings from 1 to 5
        else:
            rating = float(select_rating)
            star_rating_condition = f"star_rating BETWEEN {rating} AND {rating + 0.9}"  # Includes rating from x.0 to x.9

        #Query to retrieve bus details 
        query = f'''
            SELECT * FROM bus_details
            WHERE price BETWEEN {fare_min} AND {fare_max}
            AND route_name = "{B}"
            AND {bus_type_condition}
            AND {star_rating_condition}
            AND departure_time BETWEEN '{dep_start}' AND '{dep_end}'
            AND reaching_time BETWEEN '{arr_start}' AND '{arr_end}'
            ORDER BY price DESC, departure_time DESC
        '''
        
        my_cursor.execute(query)

        #Fetches all rows from the executed query
        out = my_cursor.fetchall()

        # Commits the current transaction
        conn.close()
        
        #converting the executed queries into dataframe

        df_result = pd.DataFrame(out, columns=[
            "ID", "bus_name", "bus_type", "departure_time", "duration", "reaching_time", "star_rating",
            "price", "seat_availability", "route_name", "route_link"
        ])
        
        
        #Displaying the dataframe in streamlit application
        st.dataframe(df_result)

    

        
      






   













