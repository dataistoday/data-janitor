import streamlit as st
import pandas as pd

# --- Sidebar Navigation ---
st.sidebar.title("🧹 Menu")
current_module = st.sidebar.radio("Choose a Module:", [
    "Module 0: Ground Zero",
    # "Module 1: The Data Janitor",
    # "Module 2: The VLOOKUP Killer",
    # "Module 3: The Pivot Table Upgrader",
    # "Module 4: The Automation Engine",
    # "Module 5: The Presentation Layer"
])

# ==========================================
# MODULE 0: GROUND ZERO
# ==========================================
if current_module == "Module 0: Ground Zero":
    st.title("📍 Ground Zero")
    st.subheader("Module 0: Making Python Talk to Your Files")
    st.info(
        "**Crucial Note:** You aren't doing this challenge on this website! Open PyCharm on your computer and follow the steps below.")

    st.markdown("""
    Before you can clean data, you have to know how to open it. In the programming world, 80% of the battle is just getting your script to successfully find the file on your computer.
    """)

    st.write("---")

    with st.expander("Step 1: Get the Data & The Workspace", expanded=True):
        # The magical download button!
        messy_data = """First_Name,Last_Name,Email,Phone_Number,System_Timestamp
jOhN,Smith,john.smith@email.com ,(555) 123-4567,2026-02-28T14:30:00.000Z
MARY  ,Johnson,,555.987.6543,2026-01-15T09:15:00.000Z
david,  Williams,DAVID@email.com,,2025-12-01T18:45:00.000Z
sara,Jones , sara.j@email.com ,+1 555 555 5555,2026-03-01T08:00:00.000Z
MICHAEL, Brown,michael.b@email.com,555-111-2222,2026-02-10T11:20:00.000Z"""

        st.download_button(
            label="📥 Click here to download Messy_Leads.csv",
            data=messy_data,
            file_name="Messy_Leads.csv",
            mime="text/csv"
        )
        st.markdown("""f
        1. Click the button above to download our dummy data.
        2. Go to your computer's Desktop and create a folder called `Python_Playground`.
        3. Move that `Messy_Leads.csv` file into your new folder.
        4. Open **PyCharm**.
        5. Right-click the folder name inside PyCharm, select **New > File**, and name it `sandbox.py` (or whatever you like, just end it in `.py`).
        """)

    with st.expander("Step 2: The Magic Word"):
        st.markdown("""
        Python is smart, but it doesn't know how to read spreadsheets out of the box. We have to invite our data-crunching library to the party.

        At the very top of your new file, type exactly this:
        ```python
        import pandas as pd
        ```
        """)

    with st.expander("Step 3: The Boss Fight (File Paths)"):
        st.markdown(r"""
        Now you have to tell Python exactly where your file lives. 

        Since your downloaded data and your Python script are located in different places on your computer, we need to give Python the exact address. This is called an **Absolute Path**.

        🚨 **The Windows Trap:** If you copy a file path directly from your computer, it uses backslashes (`\`). Python thinks backslashes are secret codes, which will instantly crash your script! 

        **The Fix:** We put a tiny `r` (for "raw") right before the quotation marks so Python reads it normally.

        Type this on line 3, making sure to replace the path with wherever your file actually saved:

        ```python
        df = pd.read_csv(r"C:\Users\YOURNAME\Desktop\Python_Playground\Messy_Leads.csv")
        ```
        """)

    with st.expander("Step 4: The Payoff"):
        st.markdown("""
        If you run your code right now, Python will read the file in a millisecond and silently close. We want to *see* it.

        Add this line to the bottom:
        ```python
        print(df.head())
        ```
        Now, right-click anywhere in your code and hit **Run**. If you see the messy spreadsheet pop up in the terminal at the bottom of PyCharm, you win!
        """)

    with st.expander("Step 5: The Output"):
        st.markdown(r"""
        Finally, let's save a copy of your work. We want to save the "Clean" file right back into the same folder where the "Messy" one is sitting. 

        Add this as your very last line, using the same path you used in Step 3 (but changing the file name at the end):

        ```python
        df.to_csv(r"C:Users\YOURNAME\Desktop\Python_Playground\Clean_Leads_Output.csv", index=False)
        ```

        **Run the script one more time.** Now, go open your **Downloads folder** on your computer. Did `Clean_Leads_Output.csv` magically appear? 

        If you see that new file, you have successfully:
        1. Imported a library
        2. Connected to a local file
        3. Created a brand new file with code

        **You are officially a developer. See you in Module 1!**
        """)

    # THE GRAND FINALE BONUS
    with st.expander("⭐ BONUS: The Pro Shortcut (Variables)"):
        st.markdown(r"""
        Typing long paths twice is a headache. Pro developers define their **Input** and **Output** paths at the very top of the script using **Variables**.

        **Your Goal:** Rewrite your script to look like this. It’s cleaner, faster, and much easier to update.

        ```python
        import pandas as pd

        # 1. SET UP YOUR PATHS AT THE TOP
        input_file = r"C:\Users\YOURNAME\Desktop\Python_Playground\Messy_Leads.csv"
        output_file = r"C:\Users\YOURNAME\Desktop\Python_Playground\Clean_Output.csv"

        # 2. RUN THE COMMANDS USING THE VARIABLES
        df = pd.read_csv(input_file)

        # (This is where your cleaning code will go later!)

        df.to_csv(output_file, index=False)

        print("Done! Check your folder for the output file.")
        ```

        **Why do this?** If you move your folder, you only have to change the path **once** at the top instead of hunting through your entire script!
        """)

# ==========================================
# MODULE 1: THE DATA JANITOR
# ==========================================
elif current_module == "Module 1: The Data Janitor":
    st.title("🧹 The Data Janitor")
    st.subheader("Module 1: Cleaning Dirty CRM Data")
    st.write("Upload your messy export, click through the challenges, and let Python do the dirty work.")

    uploaded_file = st.file_uploader("Upload Messy_Leads.csv here", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### The Raw Data:")
        st.dataframe(df)

    st.write("---")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Challenge 1: Text", "Challenge 2: Blanks", "Challenge 3: Phones", "Challenge 4: Dates"])

    with tab1:
        st.subheader("Challenge 1: The TRIM and PROPER Replacement")
        st.markdown(
            "**Your Mission:** Write a Python script to clean up the data. \n1. Capitalize names (Title Case).\n2. Make emails lowercase.\n3. Strip accidental blank spaces.")
        with st.expander("💡 Need a hint?"):
            st.write("Look into `.str.title()`, `.str.lower()`, and `.str.strip()`.")

    with tab2:
        st.subheader("Challenge 2: The Dreaded Missing Data")
        st.markdown(
            "**Your Mission:** Handle the missing data.\n1. Replace completely blank `Phone_Number` cells with 'No Number Provided'.\n2. Delete rows where `Email_Address` is missing.")
        with st.expander("💡 Need a hint?"):
            st.write("Look into `.fillna('Text')` and `.dropna(subset=['Column_Name'])`.")

    with tab3:
        st.subheader("Challenge 3: The Broken Phone Number Fix")
        st.markdown(
            "**Your Mission:** Standardize the `Applicant_Phone` column by stripping out all dashes, dots, and parentheses.")
        with st.expander("💡 Need a hint?"):
            st.write("Use `.str.replace(r'\D', '', regex=True)`.")

    with tab4:
        st.subheader("Challenge 4: The Timezone & Date Disaster")
        st.markdown("**Your Mission:** Convert the messy `System_Timestamp` column into a clean `MM/DD/YYYY` format.")
        with st.expander("💡 Need a hint?"):
            st.write("Use `pd.to_datetime()` on the column, then add `.dt.strftime('%m/%d/%Y')`.")

# ==========================================
# MODULE 2: THE VLOOKUP KILLER
# ==========================================
elif current_module == "Module 2: The VLOOKUP Killer":
    st.title("🤝 The VLOOKUP Killer")
    st.subheader("Module 2: Joining Datasets without crashing Excel")

    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload File 1 (e.g., Lead_List.csv)", type="csv")
    with col2:
        file2 = st.file_uploader("Upload File 2 (e.g., Closed_Won.csv)", type="csv")

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Inner Join", "Challenge 2: Anti-Join", "Challenge 3: Outer Join"])

    with tab1:
        st.subheader("Challenge 1: Who actually bought?")
        st.markdown(
            "**Your Mission:** Merge the two lists so only the matching rows remain. Join using their Email addresses as the match key.")
        with st.expander("💡 Need a hint?"):
            st.write("Use `pd.merge(file1_df, file2_df, how='inner', on='Email')`.")

    with tab2:
        st.subheader("Challenge 2: The Do-Not-Mail / Eviction Scrubber")
        st.markdown(
            "**Your Mission:** Perform an Anti-Join. Filter the results so you are left with ONLY the prospects who *do not* appear on the eviction list.")
        with st.expander("💡 Need a hint?"):
            st.write(
                "Use `how='left'` and add `indicator=True` inside your merge. Then, filter for `_merge == 'left_only'`!")

    with tab3:
        st.subheader("Challenge 3: System Reconciliation")
        st.markdown(
            "**Your Mission:** Merge the lists so you don't lose any data from either side. Perform an outer join based on the Transaction ID.")
        with st.expander("💡 Need a hint?"):
            st.write("Use `pd.merge(ledger_df, bank_df, how='outer', on='Transaction_ID')`.")

# ==========================================
# MODULE 3: THE PIVOT TABLE UPGRADER
# ==========================================
elif current_module == "Module 3: The Pivot Table Upgrader":
    st.title("📊 The Pivot Table Upgrader")
    st.subheader("Module 3: Grouping & Summarizing")
    st.write("Upload your transaction data below to start grouping.")

    uploaded_file = st.file_uploader("Upload Transactions.csv here", type="csv")

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Leaderboard", "Challenge 2: Custom Math", "Challenge 3: Roll-Up"])

    with tab1:
        st.subheader("Challenge 1: Sales Rep Leaderboard")
        st.markdown("**Your Mission:** Group the raw data by Sales Rep and sum up their total revenue for the month.")
        with st.expander("💡 Need a hint?"):
            st.write("Use `df.groupby('Sales_Rep')['Revenue'].sum().reset_index()`.")

    with tab2:
        st.subheader("Challenge 2: Net Sales Per Appointment")
        st.markdown(
            "**Your Mission:** Pivot tables struggle with custom metrics. Calculate the total net sales divided by the total number of appointments for each property, creating a brand new 'Net Sales Per Appointment' column.")
        with st.expander("💡 Need a hint?"):
            st.write(
                "First, group and sum the sales and appointments. Then create a new column: `grouped_df['Net_Sales_Per_Appt'] = grouped_df['Total_Sales'] / grouped_df['Appointments']`.")

    with tab3:
        st.subheader("Challenge 3: Rent Roll Roll-Up")
        st.markdown(
            "**Your Mission:** Group the property data by Floorplan to find both the *average* rent and the *total* occupied units in one line of code.")
        with st.expander("💡 Need a hint?"):
            st.write("Use the `.agg()` function! `df.groupby('Floorplan').agg({'Rent': 'mean', 'Occupied': 'sum'})`.")

# ==========================================
# MODULE 4: THE AUTOMATION ENGINE
# ==========================================
elif current_module == "Module 4: The Automation Engine":
    st.title("⚙️ The Automation Engine")
    st.subheader("Module 4: Batch Processing")
    st.info(
        "Note: For this module, you won't upload a file here. You will write a script to loop through a folder on your computer!")

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Monthly Stack", "Challenge 2: Multi-CRM", "Challenge 3: Portfolio Loop"])

    with tab1:
        st.subheader("Challenge 1: The Monthly Roll-Up")
        st.markdown(
            "**Your Mission:** Write a script that automatically finds 30 daily CSVs in a folder and stacks them into one massive dataframe.")
        with st.expander("💡 Need a hint?"):
            st.write(
                "Use the `glob` library to find the files: `files = glob.glob('folder_path/*.csv')`, then loop through them with a `for` loop!")

    with tab2:
        st.subheader("Challenge 2: Multi-CRM Standardizer")
        st.markdown(
            "**Your Mission:** Stack exports from two different CRMs, but dynamically rename the columns so they match *before* stacking them.")

    with tab3:
        st.subheader("Challenge 3: Portfolio Consolidator")
        st.markdown(
            "**Your Mission:** As you loop through property files, extract the property name directly from the file's title and add it as a new column so you know where the data came from.")

# ==========================================
# MODULE 5: THE PRESENTATION LAYER
# ==========================================
elif current_module == "Module 5: The Presentation Layer":
    st.title("📈 The Presentation Layer")
    st.subheader("Module 5: Simple Visuals")
    st.write("Upload your summarized data to instantly generate charts.")

    uploaded_file = st.file_uploader("Upload Summarized_Data.csv here", type="csv")

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Trend Tracker", "Challenge 2: Portfolio Bar", "Challenge 3: Status Pie"])

    with tab1:
        st.subheader("Challenge 1: The Trend Tracker")
        st.markdown("**Your Mission:** Generate a line chart showing monthly revenue growth over the last 12 months.")
        with st.expander("💡 Need a hint?"):
            st.write("Ensure your dates are sorted, then use `df.plot(kind='line', x='Date', y='Revenue')`.")

    with tab2:
        st.subheader("Challenge 2: The Portfolio Comparison")
        st.markdown("**Your Mission:** Create a side-by-side bar chart leaderboard comparing total sales per rep.")
        with st.expander("💡 Need a hint?"):
            st.write("Once grouped, use `df.plot(kind='bar', x='Sales_Rep', y='Total_Sales')`.")

    with tab3:
        st.subheader("Challenge 3: The Status Breakdown")
        st.markdown("**Your Mission:** Generate a pie chart showing the ratio of 'Closed Won' vs. 'Closed Lost' leads.")
        with st.expander("💡 Need a hint?"):
            st.write("Count the statuses first, then plot: `df['Status'].value_counts().plot(kind='pie')`.")