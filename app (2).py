import streamlit as st
import pandas as pd
import psycopg2

# Database connection and query function (same as before)
def get_conn():
    return psycopg2.connect(
        host='localhost',
        database='food distribute system',
        user='postgres',
        password='amirkhan',
        port='8532'
    )

def run_query(query):
    with get_conn() as conn:
        df = pd.read_sql_query(query, conn)
    return df


# Different app pages as functions

def home():
    st.title("Welcome to Food Distribution Management App")
    st.image(r"C:\Users\DELL\Downloads\generated-image.png", use_container_width=True)
    st.markdown("### Food Distribution Insights Dashboard")
    st.write("This app provides insights and filtering options for food distribution data.")


def dashboard():
    st.header("Entity Counts by City")
    query1 = """
    SELECT city, 'providers' AS entity_type, COUNT(*) AS total
    FROM providers
    GROUP BY city
    UNION ALL
    SELECT city, 'receivers' AS entity_type, COUNT(*) AS total
    FROM receivers
    GROUP BY city
    ORDER BY city, entity_type
    """
    df1 = run_query(query1)
    st.dataframe(df1)

    st.header("Provider Types and Total Quantity")
    query2 = """
    SELECT p.type AS provider_type, SUM(f.quantity) AS total_quantity
    FROM food_inventory f
    INNER JOIN providers p ON f.provider_id = p.provider_id
    GROUP BY p.type
    ORDER BY total_quantity DESC
    """
    df2 = run_query(query2)
    st.dataframe(df2)
    st.bar_chart(df2.set_index('provider_type'))


def filter_food():
    locations = run_query("SELECT DISTINCT location FROM food_inventory ORDER BY location").location.tolist()
    providers = run_query("SELECT DISTINCT name FROM providers ORDER BY name").name.tolist()
    food_types = run_query("SELECT DISTINCT food_type FROM food_inventory ORDER BY food_type").food_type.tolist()

    st.header("Filter Food Donations")
    selected_location = st.selectbox("Select Location", ["All"] + locations)
    selected_provider = st.selectbox("Select Provider", ["All"] + providers)
    selected_food_type = st.selectbox("Select Food Type", ["All"] + food_types)

    query = """
    SELECT fi.*, p.name AS provider_name
    FROM food_inventory fi
    JOIN providers p ON fi.provider_id = p.provider_id
    WHERE 1=1
    """
    if selected_location != "All":
        query += f" AND fi.location = '{selected_location}'"
    if selected_provider != "All":
        query += f" AND p.name = '{selected_provider}'"
    if selected_food_type != "All":
        query += f" AND fi.food_type = '{selected_food_type}'"

    df = run_query(query)
    st.dataframe(df)


def search_providers():
    st.header("Search Providers")
    providers_df = run_query("SELECT name, address, city, contact FROM providers ORDER BY name")

    name_options = ['All'] + sorted(providers_df['name'].dropna().unique().tolist())
    address_options = ['All'] + sorted(providers_df['address'].dropna().unique().tolist())
    city_options = ['All'] + sorted(providers_df['city'].dropna().unique().tolist())
    contact_options = ['All'] + sorted(providers_df['contact'].dropna().unique().tolist())

    selected_name = st.selectbox("Select Name", name_options)
    selected_address = st.selectbox("Select Address", address_options)
    selected_city = st.selectbox("Select City", city_options)
    selected_contact = st.selectbox("Select Contact", contact_options)

    if st.button("Search Providers"):
        filtered_df = providers_df.copy()

        if selected_name != 'All':
            filtered_df = filtered_df[filtered_df['name'] == selected_name]
        if selected_address != 'All':
            filtered_df = filtered_df[filtered_df['address'] == selected_address]
        if selected_city != 'All':
            filtered_df = filtered_df[filtered_df['city'] == selected_city]
        if selected_contact != 'All':
            filtered_df = filtered_df[filtered_df['contact'] == selected_contact]

        st.subheader(f"Search Results: {len(filtered_df)} providers found")
        st.dataframe(filtered_df)
    else:
        st.info("Select filter criteria and click Search Providers to view results.")


# Sidebar navigation
def main():
    st.sidebar.title("Navigation")
    options = ["Home", "Dashboard", "Filter Food Donations", "Search Providers"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        home()
    elif choice == "Dashboard":
        dashboard()
    elif choice == "Filter Food Donations":
        filter_food()
    elif choice == "Search Providers":
        search_providers()

def main():
    st.sidebar.title("Navigation")
    options = [
        "Home",
        "Dashboard",
        "Filter Food Donations",
        "Search Providers",
        "About / Create Details"   # New navigation option for app details
    ]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        home()
    elif choice == "Dashboard":
        dashboard()
    elif choice == "Filter Food Donations":
        filter_food()
    elif choice == "Search Providers":
        search_providers()
    elif choice == "About / Create Details":
        about_create_details()





# Food Wastage Trends page
def wastage_trends():
    st.title("Food Wastage Trends Analysis")

    # Wastage by Food Category
    query_cat = """
    SELECT
        fi.food_type,
        COUNT(c.claim_id) AS total_wastage_claims
    FROM food_inventory fi
    LEFT JOIN claims c ON fi.food_id = c.food_id AND c.status = 'wasted'
    GROUP BY fi.food_type
    ORDER BY total_wastage_claims DESC;
    """
    df_cat = run_query(query_cat)
    st.subheader("Wastage by Food Category")
    st.dataframe(df_cat)
    st.bar_chart(df_cat.set_index('food_type'))

    # Wastage by Location
    query_loc = """
    SELECT
        fi.location,
        COUNT(c.claim_id) AS total_wastage_claims
    FROM food_inventory fi
    LEFT JOIN claims c ON fi.food_id = c.food_id AND c.status = 'wasted'
    GROUP BY fi.location
    ORDER BY total_wastage_claims DESC;
    """
    df_loc = run_query(query_loc)
    st.subheader("Wastage by Location")
    st.dataframe(df_loc)
    st.bar_chart(df_loc.set_index('location'))

    # Expired Food Items by Category
    query_exp = """
    SELECT
        fi.food_type,
        COUNT(*) AS total_expired_items
    FROM food_inventory fi
    WHERE fi.expiry_date < CURRENT_DATE
    GROUP BY fi.food_type
    ORDER BY total_expired_items DESC;
    """
    df_exp = run_query(query_exp)
    st.subheader("Expired Food Items by Category")
    st.dataframe(df_exp)
    st.bar_chart(df_exp.set_index('food_type'))


# Updated main navigation to include About and Food Wastage Trends

def main():
    st.sidebar.title("Navigation")
    options = [
        "Home",
        "Dashboard",
        "Filter Food Donations",
        "Search Providers",
        "About / Create Details",
        "Food Wastage Trends"
    ]
    choice = st.sidebar.radio("Go to", options)

    if choice == "Home":
        home()
    elif choice == "Dashboard":
        dashboard()
    elif choice == "Filter Food Donations":
        filter_food()
    elif choice == "Search Providers":
        search_providers()
    elif choice == "About / Create Details":
        about_create_details()
    elif choice == "Food Wastage Trends":
        wastage_trends()




# Define the About / Create Details page content
def about_create_details():
    st.title("About This App")
    st.markdown("""
    ### Food Distribution Management App

    This app was created to provide insights, filtering, and search functionality 
    for food donation data involving providers and receivers.

    **Purpose:**  
    - To help efficiently manage food distribution, monitor inventory, and analyze donation patterns.  
    - To enable searching and filtering providers and donations by location, food type, and more.

    **Created By:**  
    Mohd Amir Khan

    **Technologies Used:**  
    - Python  
    - Streamlit for the web app interface  
    - PostgreSQL as the database  
    - psycopg2 to connect the database with Python  

    **Contact Information:**  
    - Email: hasanamir1278@gmail.com
    - GitHub: [YourGitHubProfile](https://github.com/mohdamir1278/streamlit-app.git)

    Feel free to explore the app and provide feedback!
    """)

if __name__ == "__main__":
    main()



