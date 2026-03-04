import streamlit as st
import pandas as pd

# ==========================================
# SESSION STATE INIT
# ==========================================
if 'completed' not in st.session_state:
    st.session_state.completed = set()

MODULES = [
    "Module 0: Ground Zero",
    "Module 1: The Data Janitor",
    "Module 2: The Matchmaker",
    "Module 3: The Pivot Table Upgrader",
    "Module 4: The Automation Engine",
    "Module 5: The Presentation Layer"
]

NEXT_MODULE = {
    "Module 0: Ground Zero": "Module 1: The Data Janitor",
    "Module 1: The Data Janitor": "Module 2: The Matchmaker",
    "Module 2: The Matchmaker": "Module 3: The Pivot Table Upgrader",
    "Module 3: The Pivot Table Upgrader": "Module 4: The Automation Engine",
    "Module 4: The Automation Engine": "Module 5: The Presentation Layer",
}

def module_label(m):
    return f"✅ {m}" if m in st.session_state.completed else m

# --- Sidebar Navigation ---
st.sidebar.title("🧹 Menu")

if 'current_module' not in st.session_state:
    st.session_state.current_module = MODULES[0]

current_module = st.sidebar.radio(
    "Choose a Module:",
    MODULES,
    format_func=module_label,
    key="nav_radio"
)
st.session_state.current_module = current_module

# --- Sidebar Cheat Sheet ---
st.sidebar.write("---")
with st.sidebar.expander("📋 Cheat Sheet"):
    st.markdown("""
    **Module 0**
    - `import pandas as pd` — load the library
    - `pd.read_csv(r"path")` — open a CSV
    - `df.to_csv(r"path", index=False)` — save a CSV
    - `df.head()` — peek at the first 5 rows

    **Module 1**
    - `.str.title()` — Title Case
    - `.str.lower()` — all lowercase
    - `.str.strip()` — remove extra spaces
    - `.str.replace(r'\\D', '', regex=True)` — strip non-digits
    - `.fillna('value')` — fill blank cells
    - `.dropna(subset=['col'])` — drop rows with blanks
    - `pd.to_datetime(col)` — parse a date string
    - `.dt.strftime('%m/%d/%Y')` — format a date

    **Module 2**
    - `.rename(columns={'old': 'new'})` — rename columns
    - `.drop_duplicates(subset=['col'])` — remove dupes
    - `df[~df['col'].str.contains('x')]` — filter rows out
    - `pd.merge(df1, df2, on='col', how='left')` — join/VLOOKUP

    **Module 3**
    - `.groupby('col')['val'].sum()` — sum by group
    - `.groupby('col')[['a','b']].sum()` — sum multiple cols
    - `.agg({'col1': 'mean', 'col2': 'sum'})` — mixed aggregation
    - `.reset_index()` — flatten the result back to a table

    **Module 4**
    - `import glob` — file finder library
    - `glob.glob(r"path\\*.csv")` — list all CSVs in folder
    - `pd.concat(list, ignore_index=True)` — stack dataframes
    - `import os` — file system library
    - `os.path.basename(path)` — extract filename from path

    **Module 5**
    - `df.plot(kind='line', x=, y=)` — line chart
    - `df.plot(kind='bar', x=, y=)` — bar chart
    - `.value_counts().plot(kind='pie')` — pie chart
    - `plt.show()` — pop open the chart window
    """)

# ==========================================
# HELPER: NEXT MODULE BUTTON
# ==========================================
def next_module_button(current):
    if current in NEXT_MODULE:
        next_m = NEXT_MODULE[current]
        if st.button(f"→ Continue to {next_m}"):
            st.session_state.nav_radio = next_m
            st.rerun()

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
        st.markdown("""
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
        Finally, let's save a copy of your work. We want to save the "Clean" file right back into the same `Python_Playground` folder where the "Messy" one is sitting. 

        Add this as your very last line, using the same folder path you used in Step 3 (but changing the file name at the end):

        ```python
        df.to_csv(r"C:\Users\YOURNAME\Desktop\Python_Playground\Clean_Leads_Output.csv", index=False)
        ```

        **Run the script one more time.** Now go open your `Python_Playground` folder. Did `Clean_Leads_Output.csv` magically appear? 

        If you see that new file, you have successfully:
        1. Imported a library
        2. Connected to a local file
        3. Created a brand new file with code

        **You are officially a developer. See you in Module 1!**
        """)

    with st.expander("⭐ BONUS: The Pro Shortcut (Variables & Sneak Peek)"):
        st.markdown(r"""
        Typing long paths twice is a headache. Pro developers define their **Input** and **Output** paths at the very top of the script using **Variables**.

        Even better, let's look at exactly where the "Data Janitor" work actually happens! 

        **Your Final Mission:** Rewrite your script to look like this. We are going to add **two lines of cleaning code** right in the middle to fix the messy names (like "jOhN") and the messy emails (like "DAVID@email.com").

        ```python
        import pandas as pd

        # 1. SET UP YOUR PATHS AT THE TOP
        input_file = r"C:\Users\YOURNAME\Desktop\Python_Playground\Messy_Leads.csv"
        output_file = r"C:\Users\YOURNAME\Desktop\Python_Playground\Clean_Output.csv"

        # 2. OPEN THE FILE
        df = pd.read_csv(input_file)

        # ----------------------------------------------------
        # 3. THE CLEANING ZONE (This is what you will learn in Module 1!)

        # Sneak Peek 1: Make all First Names proper Title Case (jOhN -> John)
        df['First_Name'] = df['First_Name'].str.title()

        # Sneak Peek 2: Force all Emails to be completely lowercase
        df['Email'] = df['Email'].str.lower()
        # ----------------------------------------------------

        # 4. SAVE THE FILE AND PRINT THE RESULT
        df.to_csv(output_file, index=False)
        print("Cleaning Complete! Here is a peek at your new data:")
        print(df.head())
        ```

        **Run it one last time!** Look at the terminal output at the bottom of PyCharm. "jOhN" is now "John", and the emails are perfectly uniform. 

        If you successfully ran this script, you have mastered the hardest part of Python: getting it to talk to your computer. **You are ready for Module 1!**
        """)

    st.write("---")
    st.success("✅ **What you just learned:** How to import a library, read a CSV from a file path, and save a new file with code. This is the foundation everything else is built on.")
    next_module_button(current_module)

# ==========================================
# MODULE 1: THE DATA JANITOR
# ==========================================
elif current_module == "Module 1: The Data Janitor":
    st.title("🧹 The Data Janitor")
    st.subheader("Module 1: Cleaning Dirty CRM Data")

    st.markdown("""
    Welcome to the big leagues. Your raw CRM export is a disaster. 
    Keep PyCharm open, work through the 4 challenges below, and when you think your script is perfect, 
    run it to generate your final `Clean_Output.csv`.
    """)

    st.write("---")
    st.markdown("### The Janitor Challenges")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Challenge 1: Text",
        "Challenge 2: Blanks",
        "Challenge 3: Phones",
        "Challenge 4: Dates"
    ])

    with tab1:
        st.subheader("Challenge 1: The TRIM and PROPER Replacement")
        st.markdown("""
        **Your Mission:** Write a Python script to clean up the text formatting. 
        1. Capitalize `First_Name` and `Last_Name` (Title Case).
        2. Make `Email` completely lowercase.
        3. Strip accidental blank spaces from `First_Name`.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("You can actually stack commands on top of each other!")
            st.code("""
df['First_Name'] = df['First_Name'].str.title().str.strip()
df['Last_Name'] = df['Last_Name'].str.title().str.strip()
df['Email'] = df['Email'].str.lower()
            """, language="python")

    with tab2:
        st.subheader("Challenge 2: The Dreaded Missing Data")
        st.markdown("""
        **Your Mission:** Handle the blank cells before they break your downstream processes.
        1. Replace completely blank `Phone_Number` cells with 'No Number'.
        2. Delete any rows where the `Email` is completely missing.
        """)
        with st.expander("💡 Need a hint?"):
            st.code("""
# Fill the blanks
df['Phone_Number'] = df['Phone_Number'].fillna('No Number')

# Drop rows missing an email
df = df.dropna(subset=['Email'])
            """, language="python")

    with tab3:
        st.subheader("Challenge 3: The Broken Phone Number Fix")
        st.markdown("""
        **Your Mission:** Standardize the `Phone_Number` column by stripping out all dashes, dots, spaces, and parentheses so it's just raw numbers.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("Use Regular Expressions (Regex) to replace anything that isn't a digit (`\\D`) with nothing.")
            st.code("""
df['Phone_Number'] = df['Phone_Number'].str.replace(r'\\D', '', regex=True)
            """, language="python")

    with tab4:
        st.subheader("Challenge 4: The Timezone & Date Disaster")
        st.markdown("""
        **Your Mission:** Convert the terrifying `System_Timestamp` column into a clean, readable `MM/DD/YYYY` format.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("First, tell Pandas it's a date. Then, format it however you want.")
            st.code("""
# Convert from a string to a DateTime object
df['System_Timestamp'] = pd.to_datetime(df['System_Timestamp'])

# Format it to MM/DD/YYYY
df['System_Timestamp'] = df['System_Timestamp'].dt.strftime('%m/%d/%Y')
            """, language="python")

    st.write("---")

    # ==========================================
    # THE AUTOMATED GRADER
    # ==========================================
    st.subheader("🏁 The Boss Level: Check Your Work")
    st.info("Upload your final `Clean_Output.csv` here. If you successfully cleaned the emails, you pass!")

    uploaded_file = st.file_uploader("Drop Clean_Output.csv here", type="csv")

    if uploaded_file is not None:
        try:
            clean_df = pd.read_csv(uploaded_file)
            st.write("### The Verdict:")

            missing_emails = clean_df['Email'].isnull().sum()
            is_lower = (clean_df['Email'].dropna() == clean_df['Email'].dropna().str.lower()).all()

            if missing_emails == 0 and is_lower:
                st.session_state.completed.add(current_module)
                st.success("🎉 BOOM! You successfully scrubbed the data!")
                st.balloons()
                st.dataframe(clean_df)
                st.write("---")
                st.success("✅ **What you just learned:** `.str` methods for text cleaning, `.fillna()` and `.dropna()` for missing data, regex for pattern replacement, and date parsing with `pd.to_datetime()`.")
                next_module_button(current_module)
            else:
                st.error("🚨 Not quite! The 'Email' column still has some issues.")
                if missing_emails > 0:
                    st.warning(f"Hint: I still see {missing_emails} completely blank email addresses. Check Challenge 2!")
                if not is_lower:
                    st.warning("Hint: Some of the emails still have CAPITAL letters in them. Check Challenge 1!")

        except Exception as e:
            st.error("Oops! Something went wrong reading your file. Did you accidentally delete a column name?")

# ==========================================
# MODULE 2: THE MATCHMAKER
# ==========================================
elif current_module == "Module 2: The Matchmaker":
    st.title("🧩 The Matchmaker")
    st.subheader("Module 2: Mapping, Filtering & Joins")

    st.markdown("""
    Formatting text is great, but real-world data never comes from just one place. 
    When you are combining exports from different systems, you have to force them into the same shape, filter out the junk, and join dataframes together.
    """)

    st.write("---")
    st.write("### 📥 Step 1: Get the New Data")
    st.info("You'll need both of these files for Challenge 4! Download them into your `Python_Playground` folder.")

    col1, col2 = st.columns(2)
    with col1:
        module2_data = """Applicant_First,Last_Name,Mail_Address,Phone_Number,System_Timestamp
Alice,Smith,alice.smith@email.com,555-0100,03/01/2026
Bob,Jones,bjones@email.com,555-0200,03/02/2026
Alice,Smith,alice.smith@email.com,555-0100,03/03/2026
Test,User,test@fullthrottle.ai,555-9999,03/03/2026
Charlie,Brown,charlie.b@email.com,555-0300,03/04/2026
QA,Tester,qa.lead@fullthrottle.ai,555-8888,03/04/2026
Bob,Jones,bjones@email.com,555-0200,03/05/2026"""

        st.download_button(
            label="📥 Download CRM_Export_V2.csv",
            data=module2_data,
            file_name="CRM_Export_V2.csv",
            mime="text/csv"
        )

    with col2:
        roster_data = """Email,Assigned_Property
alice.smith@email.com,Lakeside
bjones@email.com,Riverside
charlie.b@email.com,Parkview"""

        st.download_button(
            label="📥 Download Property_Roster.csv",
            data=roster_data,
            file_name="Property_Roster.csv",
            mime="text/csv"
        )

    st.write("---")
    st.markdown("### The Janitor Challenges: Round 2")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Challenge 1: Mapping",
        "Challenge 2: Duplicates",
        "Challenge 3: The Filter",
        "Challenge 4: Joins (VLOOKUP)"
    ])

    with tab1:
        st.subheader("Challenge 1: The Column Shape-Shifter")
        st.markdown("""
        **Your Mission:** A new CRM export just came in, but the columns are named weirdly. 
        Rename `Applicant_First` to `First_Name` and `Mail_Address` to `Email` so they match our standard format.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("Use `.rename()` with a Python Dictionary! A dictionary is just a mapping of `{'Old_Name': 'New_Name'}`.")
            st.code("""
column_mapping = {
    'Applicant_First': 'First_Name',
    'Mail_Address': 'Email'
}
df = df.rename(columns=column_mapping)
            """, language="python")

    with tab2:
        st.subheader("Challenge 2: The Duplicate Destroyer")
        st.markdown("""
        **Your Mission:** People submit forms multiple times. Find anyone who has the exact same `Email` in the system more than once, and delete the older duplicate.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("Pandas has a built-in assassin for this exact scenario.")
            st.code("""
# Keep the first time they entered the system, drop the rest!
df = df.drop_duplicates(subset=['Email'], keep='first')
            """, language="python")

    with tab3:
        st.subheader("Challenge 3: The Internal Filter")
        st.markdown("""
        **Your Mission:** Our marketing team keeps submitting "test" leads. 
        Find any row where the `Email` contains `@fullthrottle.ai` and completely remove it from the dataset.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("The `~` symbol in Python means 'NOT'. We are telling Pandas: Keep the rows where the email does NOT contain our company domain.")
            st.code("""
# The ~ symbol flips the search to find the opposite!
df = df[~df['Email'].str.contains('@fullthrottle.ai', na=False)]
            """, language="python")

    with tab4:
        st.subheader("Challenge 4: The VLOOKUP Upgrade (Joins)")
        st.markdown("""
        **Your Mission:** Load `Property_Roster.csv` as a second dataframe and merge it into your main data so every lead has an `Assigned_Property` attached to them based on their email.
        """)
        with st.expander("💡 Need a hint?"):
            st.write("In Python, we don't VLOOKUP. We Merge. It's infinitely faster and won't crash your computer.")
            st.code("""
# 1. Load the second file
roster_df = pd.read_csv(r"C:\\Your\\Path\\Property_Roster.csv")

# 2. Merge them together (telling Python to match them on the 'Email' column)
df = pd.merge(df, roster_df, on='Email', how='left')
            """, language="python")

    # ==========================================
    # MODULE 2 GRADER
    # ==========================================
    st.write("---")
    st.subheader("🏁 The Boss Level: Check Your Work")
    st.info("Upload your final mapped, filtered, and merged CSV here!")

    uploaded_mod2 = st.file_uploader("Drop your Module 2 Output here", type="csv")
    if uploaded_mod2 is not None:
        try:
            mod2_df = pd.read_csv(uploaded_mod2)
            st.write("### The Verdict:")

            cols_correct = 'First_Name' in mod2_df.columns and 'Email' in mod2_df.columns and 'Assigned_Property' in mod2_df.columns
            no_dupes = len(mod2_df) <= 3
            no_tests = True
            if 'Email' in mod2_df.columns:
                no_tests = not mod2_df['Email'].str.contains('@fullthrottle.ai', na=False).any()

            if cols_correct and no_dupes and no_tests:
                st.session_state.completed.add(current_module)
                st.success("🎉 INCREDIBLE! You mapped, deduplicated, filtered, and joined like a pro!")
                st.balloons()
                st.dataframe(mod2_df)
                st.write("---")
                st.success("✅ **What you just learned:** `.rename()` to standardize columns, `.drop_duplicates()` to kill dupes, boolean filtering with `~` to remove junk rows, and `pd.merge()` to replace VLOOKUP forever.")
                next_module_button(current_module)
            else:
                st.error("🚨 Not quite! There's still some junk in the trunk.")
                if not cols_correct:
                    st.warning("Hint: Check Challenges 1 & 4. I'm missing 'First_Name', 'Email', or 'Assigned_Property'.")
                if not no_dupes:
                    st.warning("Hint: Check Challenge 2. I'm still seeing duplicate emails in here!")
                if not no_tests:
                    st.warning("Hint: Check Challenge 3. The marketing team's test leads are still showing up!")

        except Exception as e:
            st.error("Oops! Something went wrong. Did you save it as a CSV?")

# ==========================================
# MODULE 3: THE PIVOT TABLE UPGRADER
# ==========================================
elif current_module == "Module 3: The Pivot Table Upgrader":
    st.title("📊 The Pivot Table Upgrader")
    st.subheader("Module 3: Grouping & Summarizing")

    st.markdown("""
    You've cleaned the data. Now it's time to analyze it. 
    Python's `.groupby()` function is like an Excel Pivot Table on steroids. Let's crunch some numbers.
    """)

    st.write("### 📥 Step 1: Get the Transaction Data")
    module3_data = """Sales_Rep,Appointments,Total_Sales,Property,Floorplan,Rent,Occupied
Amanda,10,50000,Lakeside,1B1B,1500,1
David,8,32000,Riverside,2B2B,2000,1
Amanda,5,20000,Lakeside,2B2B,2200,1
David,12,60000,Riverside,1B1B,1400,0
Alice,15,45000,Lakeside,1B1B,1500,1"""

    st.download_button(
        label="📥 Download Transactions.csv",
        data=module3_data,
        file_name="Transactions.csv",
        mime="text/csv"
    )

    # Live preview metrics from the sample data
    st.write("---")
    st.write("### 📌 A Sneak Peek: What This Data Becomes")
    st.caption("This is what your finished groupby output will look like — presented as a real dashboard metric card. By the end of this module, you'll have built the numbers behind these.")
    preview_df = pd.read_csv(pd.io.common.StringIO(module3_data))
    total_sales = preview_df['Total_Sales'].sum()
    top_rep = preview_df.groupby('Sales_Rep')['Total_Sales'].sum().idxmax()
    avg_rent = preview_df['Rent'].mean()
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"${total_sales:,.0f}")
    col2.metric("🏆 Top Sales Rep", top_rep)
    col3.metric("🏠 Avg Rent", f"${avg_rent:,.0f}")

    st.write("---")
    st.markdown("### The Janitor Challenges: Round 3")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Leaderboard", "Challenge 2: Custom Math", "Challenge 3: Roll-Up"])

    with tab1:
        st.subheader("Challenge 1: Sales Rep Leaderboard")
        st.markdown("**Your Mission:** Group the raw data by `Sales_Rep` and sum up their `Total_Sales` for the month.")
        with st.expander("💡 Need a hint?"):
            st.code("df_grouped = df.groupby('Sales_Rep')['Total_Sales'].sum().reset_index()", language="python")

    with tab2:
        st.subheader("Challenge 2: Net Sales Per Appointment")
        st.markdown(
            "**Your Mission:** Calculate the total net sales divided by the total number of appointments for each rep, creating a brand new `Net_Sales_Per_Appt` column.")
        with st.expander("💡 Need a hint?"):
            st.write("First, group multiple columns at once. Then do the math on the new grouped dataframe!")
            st.code("""
# Group both columns
rep_stats = df.groupby('Sales_Rep')[['Total_Sales', 'Appointments']].sum().reset_index()

# Create the custom metric
rep_stats['Net_Sales_Per_Appt'] = rep_stats['Total_Sales'] / rep_stats['Appointments']
            """, language="python")

    with tab3:
        st.subheader("Challenge 3: Rent Roll Roll-Up")
        st.markdown(
            "**Your Mission:** Group the property data by `Floorplan` to find both the *average* `Rent` and the *total* `Occupied` units in one line of code.")
        with st.expander("💡 Need a hint?"):
            st.write("Use the `.agg()` function to do different math on different columns simultaneously!")
            st.code("rent_roll = df.groupby('Floorplan').agg({'Rent': 'mean', 'Occupied': 'sum'}).reset_index()",
                    language="python")

    # ==========================================
    # MODULE 3 GRADER
    # ==========================================
    st.write("---")
    st.subheader("🏁 The Boss Level: Check Your Work")
    st.info("Upload your final leaderboard CSV. It needs the `Net_Sales_Per_Appt` column and should have one row per Sales Rep (3 reps = 3 rows).")

    uploaded_mod3 = st.file_uploader("Drop your Grouped Output here", type="csv")
    if uploaded_mod3 is not None:
        try:
            mod3_df = pd.read_csv(uploaded_mod3)
            has_col = 'Net_Sales_Per_Appt' in mod3_df.columns
            right_rows = len(mod3_df) <= 3

            if has_col and right_rows:
                st.session_state.completed.add(current_module)
                st.success("🎉 NAILED IT! You just out-pivoted Excel!")
                st.balloons()
                st.dataframe(mod3_df)
                st.write("---")
                st.success("✅ **What you just learned:** `.groupby()` for pivot-table-style summaries, grouping multiple columns at once, `.agg()` for mixed math, and creating calculated columns from grouped results.")
                next_module_button(current_module)
            else:
                st.error("🚨 Almost there!")
                if not has_col:
                    st.warning("Hint: I don't see a `Net_Sales_Per_Appt` column. Make sure you completed Challenge 2 and saved that column into your output file.")
                if not right_rows:
                    st.warning(f"Hint: I'm seeing {len(mod3_df)} rows but expected 3 (one per Sales Rep). Make sure you grouped by `Sales_Rep` before saving.")
        except Exception as e:
            st.error("Error reading file. Did you save it as a CSV?")

# ==========================================
# MODULE 4: THE AUTOMATION ENGINE
# ==========================================
elif current_module == "Module 4: The Automation Engine":
    st.title("⚙️ The Automation Engine")
    st.subheader("Module 4: Batch Processing")
    st.markdown(
        "Writing code for one file is cool. Having Python automatically find and process 100 files in 3 seconds is a superpower.")

    st.write("### 📥 Step 1: Get the Regional Data")
    st.write("Download these two files and put them in a new folder called `Monthly_Stack` inside your `Python_Playground` folder.")

    north_data = """Rep,Region,Leads,Closed_Deals,Revenue
Alice,North,45,12,60000
Bob,North,32,8,40000
Carol,North,28,6,30000
Dan,North,51,15,75000
Eve,North,39,10,50000"""

    south_data = """Rep,Region,Leads,Closed_Deals,Revenue
Charlie,South,50,14,70000
Diana,South,28,7,35000
Frank,South,44,11,55000
Grace,South,33,9,45000
Hank,South,60,18,90000"""

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download North_Region.csv", data=north_data,
                           file_name="North_Region.csv", mime="text/csv")
    with col2:
        st.download_button("📥 Download South_Region.csv", data=south_data,
                           file_name="South_Region.csv", mime="text/csv")

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Monthly Stack", "Challenge 2: Multi-CRM", "Challenge 3: Portfolio Loop"])

    with tab1:
        st.subheader("Challenge 1: The Monthly Roll-Up")
        st.markdown(
            "**Your Mission:** Write a script that uses the `glob` library to find all CSVs in your `Monthly_Stack` folder and stacks them into one dataframe.")
        with st.expander("💡 Need a hint?"):
            st.code("""
import pandas as pd
import glob

# 1. Get a list of all CSV files in the folder
all_files = glob.glob(r"C:\\Your\\Path\\Monthly_Stack\\*.csv")

# 2. Loop through them and store the data in a list
dataframes_list = []
for file in all_files:
    temp_df = pd.read_csv(file)
    dataframes_list.append(temp_df)

# 3. Smash them all together!
final_df = pd.concat(dataframes_list, ignore_index=True)
            """, language="python")

    with tab2:
        st.subheader("Challenge 2: Multi-CRM Standardizer")
        st.markdown(
            "**Your Mission:** Modify your loop so that it forces all column names to be lowercase *before* it appends them to the list.")
        with st.expander("💡 Need a hint?"):
            st.code("""
for file in all_files:
    temp_df = pd.read_csv(file)
    temp_df.columns = temp_df.columns.str.lower() # Standardize!
    dataframes_list.append(temp_df)
            """, language="python")

    with tab3:
        st.subheader("Challenge 3: Portfolio Consolidator")
        st.markdown(
            "**Your Mission:** As you loop through the files, extract the file's name and add it as a new column so you know where the data came from.")
        with st.expander("💡 Need a hint?"):
            st.write("You can use the `os` library to extract just the file name from the long file path!")
            st.code("""
import os

for file in all_files:
    temp_df = pd.read_csv(file)
    # Grab the filename and make it a column
    temp_df['Source_File'] = os.path.basename(file)
    dataframes_list.append(temp_df)
            """, language="python")

    # ==========================================
    # MODULE 4 GRADER
    # ==========================================
    st.write("---")
    st.subheader("🏁 The Boss Level: Check Your Work")
    st.info("Stack both region files and save the combined output as a CSV. It should have all 10 reps and a `Source_File` column. Upload it here!")

    uploaded_mod4 = st.file_uploader("Drop your Stacked Output here", type="csv")
    if uploaded_mod4 is not None:
        try:
            mod4_df = pd.read_csv(uploaded_mod4)

            has_source = 'Source_File' in mod4_df.columns or 'source_file' in mod4_df.columns
            enough_rows = len(mod4_df) >= 10
            has_both_regions = False
            if has_source:
                col_name = 'Source_File' if 'Source_File' in mod4_df.columns else 'source_file'
                sources = mod4_df[col_name].str.lower().unique()
                has_both_regions = any('north' in s for s in sources) and any('south' in s for s in sources)

            if has_source and enough_rows and has_both_regions:
                st.session_state.completed.add(current_module)
                st.success("🎉 AUTOMATED! You just processed an entire folder of files in one script!")
                st.balloons()
                st.dataframe(mod4_df)
                st.write("---")
                st.success("✅ **What you just learned:** `glob` to find files by pattern, `for` loops to process them one by one, `pd.concat()` to stack dataframes, and `os.path.basename()` to track data sources.")
                next_module_button(current_module)
            else:
                st.error("🚨 Not quite!")
                if not enough_rows:
                    st.warning(f"Hint: I only see {len(mod4_df)} rows. Both region files together should give you 10 reps. Did you stack both files?")
                if not has_source:
                    st.warning("Hint: I don't see a `Source_File` column. Make sure you completed Challenge 3 and added the filename as a column!")
                if has_source and not has_both_regions:
                    st.warning("Hint: Looks like only one region made it in. Make sure your glob is picking up both North and South files.")

        except Exception as e:
            st.error("Error reading file. Did you save the combined output as a CSV?")

# ==========================================
# MODULE 5: THE PRESENTATION LAYER
# ==========================================
elif current_module == "Module 5: The Presentation Layer":
    st.title("📈 The Presentation Layer")
    st.subheader("Module 5: Simple Visuals")
    st.markdown("Data is only useful if leadership can read it. Let's turn your cleaned CSVs into charts.")

    st.write("### 📥 Step 1: Get the Summarized Data")
    st.download_button(
        "📥 Download Chart_Data.csv",
        data="Month,Revenue,Status\nJan,10000,Won\nFeb,15000,Lost\nMar,12000,Won\nApr,18000,Won",
        file_name="Chart_Data.csv",
        mime="text/csv"
    )

    st.write("---")
    tab1, tab2, tab3 = st.tabs(["Challenge 1: Trend Tracker", "Challenge 2: Portfolio Bar", "Challenge 3: Status Pie"])

    with tab1:
        st.subheader("Challenge 1: The Trend Tracker")
        st.markdown("**Your Mission:** Generate a line chart showing monthly revenue growth.")
        with st.expander("💡 Need a hint?"):
            st.code("""
import matplotlib.pyplot as plt

df.plot(kind='line', x='Month', y='Revenue', title="Monthly Revenue")
plt.show() # This pops open the chart window!
            """, language="python")

    with tab2:
        st.subheader("Challenge 2: The Portfolio Comparison")
        st.markdown("**Your Mission:** Change your code to create a bar chart instead of a line chart.")
        with st.expander("💡 Need a hint?"):
            st.code("df.plot(kind='bar', x='Month', y='Revenue', color='green')", language="python")

    with tab3:
        st.subheader("Challenge 3: The Status Breakdown")
        st.markdown("**Your Mission:** Generate a pie chart showing the ratio of 'Won' vs. 'Lost' leads.")
        with st.expander("💡 Need a hint?"):
            st.code("""
# Count the statuses first, then plot the counts!
status_counts = df['Status'].value_counts()
status_counts.plot(kind='pie', autopct='%1.1f%%')
plt.show()
            """, language="python")

    # ==========================================
    # MODULE 5 GRADER (THE FRIDGE)
    # ==========================================
    st.write("---")
    st.subheader("🖼️ The Boss Level: The Digital Fridge")
    st.info(
        "In PyCharm, click the 'Save' icon on your chart to save it as a .png image. Upload your masterpiece here to complete the course!")

    uploaded_chart = st.file_uploader("Drop your Chart Image (.png or .jpg) here", type=["png", "jpg", "jpeg"])

    if uploaded_chart is not None:
        st.session_state.completed.add(current_module)
        st.success("🎉 GRADUATION COMPLETE! You are officially a Data Janitor!")
        st.balloons()
        st.image(uploaded_chart, caption="Your Python Masterpiece, proudly displayed on the digital fridge.")
        st.write("---")
        st.success("✅ **What you just learned:** `matplotlib` for chart creation, `.plot()` with `kind=` to switch chart types, and `.value_counts()` to summarize categorical data before plotting.")
        st.info("🏆 Head back through the sidebar — any modules without a ✅ are still waiting for you!")
