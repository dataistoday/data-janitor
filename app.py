import streamlit as st
import pandas as pd
from io import BytesIO
import streamlit.components.v1 as components
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


# ==========================================
# GOOGLE SHEETS HELPER
# ==========================================
def save_feedback_to_sheet(overall, hardest, fave, recommend, comments):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(st.secrets["feedback_sheet_id"]).sheet1

        if not sheet.get_all_values():
            sheet.append_row(
                ["Timestamp", "Rating", "Hardest Module", "Favorite Module", "Would Recommend", "Comments"])

        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            overall,
            hardest,
            fave,
            recommend,
            comments
        ])
        return True
    except Exception as e:
        return False


def inject_ga():
    components.html("""
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-C5LSF3VNRX"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-C5LSF3VNRX');
        </script>
    """, height=0)


inject_ga()

# ==========================================
# SESSION STATE INIT & NAVIGATION
# ==========================================
if 'completed' not in st.session_state:
    st.session_state.completed = set()

# Add the Phase 1 & 2 modules to the tracking lists
if 'mod1_passed' not in st.session_state: st.session_state['mod1_passed'] = False
if 'mod2_passed' not in st.session_state: st.session_state['mod2_passed'] = False
if 'mod3_passed' not in st.session_state: st.session_state['mod3_passed'] = False
if 'mod4_passed' not in st.session_state: st.session_state['mod4_passed'] = False
if 'mod5_passed' not in st.session_state: st.session_state['mod5_passed'] = False

if 'mod6_passed' not in st.session_state: st.session_state['mod6_passed'] = False
if 'mod7_passed' not in st.session_state: st.session_state['mod7_passed'] = False
if 'mod8_passed' not in st.session_state: st.session_state['mod8_passed'] = False
if 'mod9_passed' not in st.session_state: st.session_state['mod9_passed'] = False

# The Phase 2 Master Lock
if 'phase2_unlocked' not in st.session_state:
    st.session_state['phase2_unlocked'] = False

NEXT_MODULE = {
    "🏠 Home": "🛠️ Setup: Before You Begin",
    "🛠️ Setup: Before You Begin": "--- PHASE 1: THE BASICS ---",
    "--- PHASE 1: THE BASICS ---": "Module 0: Ground Zero",
    "Module 0: Ground Zero": "Module 1: The Data Janitor",
    "Module 1: The Data Janitor": "Module 2: The Matchmaker",
    "Module 2: The Matchmaker": "Module 3: The Pivot Table Upgrader",
    "Module 3: The Pivot Table Upgrader": "Module 4: The Automation Engine",
    "Module 4: The Automation Engine": "Module 5: The Presentation Layer",
    "Module 5: The Presentation Layer": "🎓 Phase 1 Graduation",
    "🎓 Phase 1 Graduation": "📝 Feedback",
    "📝 Feedback": "--- PHASE 2: THE ARCHITECT ---",
    "--- PHASE 2: THE ARCHITECT ---": "Module 6: The Blueprint",
    "Module 6: The Blueprint": "Module 7: The Time Machine",
    "Module 7: The Time Machine": "Module 8: The SQL Surgeon",
    "Module 8: The SQL Surgeon": "Module 9: The Output Architect"
}

COMPLETABLE_MODULES = [
    "Module 1: The Data Janitor", "Module 2: The Matchmaker", "Module 3: The Pivot Table Upgrader",
    "Module 4: The Automation Engine", "Module 5: The Presentation Layer",
    "Module 6: The Blueprint", "Module 7: The Time Machine", "Module 8: The SQL Surgeon",
    "Module 9: The Output Architect"
]


# Function to dynamically add checkmarks to the menu
def format_menu_item(module_name):
    if module_name == "Module 1: The Data Janitor" and st.session_state['mod1_passed']: return f"✅ {module_name}"
    if module_name == "Module 2: The Matchmaker" and st.session_state['mod2_passed']: return f"✅ {module_name}"
    if module_name == "Module 3: The Pivot Table Upgrader" and st.session_state[
        'mod3_passed']: return f"✅ {module_name}"
    if module_name == "Module 4: The Automation Engine" and st.session_state['mod4_passed']: return f"✅ {module_name}"
    if module_name == "Module 5: The Presentation Layer" and st.session_state['mod5_passed']: return f"✅ {module_name}"
    if module_name == "Module 6: The Blueprint" and st.session_state['mod6_passed']: return f"✅ {module_name}"
    if module_name == "Module 7: The Time Machine" and st.session_state['mod7_passed']: return f"✅ {module_name}"
    if module_name == "Module 8: The SQL Surgeon" and st.session_state['mod8_passed']: return f"✅ {module_name}"
    if module_name == "Module 9: The Output Architect" and st.session_state['mod9_passed']: return f"✅ {module_name}"
    return module_name


current_module = st.sidebar.radio(
    "Choose a Module:",
    [
        "🏠 Home",
        "🛠️ Setup: Before You Begin",
        "--- PHASE 1: THE BASICS ---",
        "Module 0: Ground Zero",
        "Module 1: The Data Janitor",
        "Module 2: The Matchmaker",
        "Module 3: The Pivot Table Upgrader",
        "Module 4: The Automation Engine",
        "Module 5: The Presentation Layer",
        "🎓 Phase 1 Graduation",
        "📝 Feedback",
        "--- PHASE 2: THE ARCHITECT ---",
        "Module 6: The Blueprint",
        "Module 7: The Time Machine",
        "Module 8: The SQL Surgeon",
        "Module 9: The Output Architect"
    ],
    format_func=format_menu_item
)
st.session_state.current_module = current_module

# --- Progress Bar ---
st.sidebar.write("---")
completed_count = len(st.session_state.completed)
total_count = len(COMPLETABLE_MODULES)
st.sidebar.markdown(f"**📊 Progress: {completed_count} of {total_count} modules complete**")
st.sidebar.progress(completed_count / total_count)

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
            st.session_state.current_module = next_m
            st.rerun()


# ==========================================
# HELPER: CERTIFICATE GENERATOR
# ==========================================
def generate_certificate(name):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    fig, ax = plt.subplots(figsize=(11, 8.5))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    outer = patches.FancyBboxPatch((0.15, 0.15), 10.7, 8.2,
                                   boxstyle="round,pad=0.1", linewidth=4,
                                   edgecolor='#FFD700', facecolor='none')
    ax.add_patch(outer)

    inner = patches.FancyBboxPatch((0.35, 0.35), 10.3, 7.8,
                                   boxstyle="round,pad=0.05", linewidth=1.5,
                                   edgecolor='#FFD700', facecolor='none', alpha=0.4)
    ax.add_patch(inner)

    ax.text(5.5, 7.5, "🧹  Certificate of Completion",
            ha='center', va='center', fontsize=22, fontweight='bold',
            color='#FFD700', fontfamily='DejaVu Sans')

    ax.text(5.5, 6.8, "This certifies that",
            ha='center', va='center', fontsize=14, color='#cccccc',
            style='italic')

    ax.text(5.5, 5.9, name if name.strip() else "A Proud Data Janitor",
            ha='center', va='center', fontsize=32, fontweight='bold',
            color='#ffffff')

    ax.plot([1.5, 9.5], [5.35, 5.35], color='#FFD700', linewidth=1, alpha=0.5)

    ax.text(5.5, 4.85, "has successfully completed",
            ha='center', va='center', fontsize=14, color='#cccccc',
            style='italic')

    ax.text(5.5, 4.2, "Python for Data Janitors",
            ha='center', va='center', fontsize=26, fontweight='bold',
            color='#4fc3f7')

    ax.text(5.5, 3.55,
            "Mastering data cleaning, automation, and visualization\nusing Python, Pandas, and Matplotlib",
            ha='center', va='center', fontsize=12, color='#aaaaaa',
            linespacing=1.8)

    badges = ["Ground Zero", "Data Janitor", "Matchmaker", "Pivot Pro", "Automation", "Visualization"]
    badge_x = [1.0, 2.9, 4.8, 6.2, 8.0, 9.6]
    for i, (badge, x) in enumerate(zip(badges, badge_x)):
        circ = patches.Circle((x, 2.4), 0.45, color='#FFD700', alpha=0.15)
        ax.add_patch(circ)
        ax.text(x, 2.55, "✅", ha='center', va='center', fontsize=10)
        ax.text(x, 2.1, badge, ha='center', va='center', fontsize=6.5,
                color='#aaaaaa')

    ax.text(5.5, 1.2, "You are officially a Data Janitor. The spreadsheet fears you.",
            ha='center', va='center', fontsize=11, color='#888888', style='italic')

    ax.text(5.5, 0.65, "python4datajanitors.com",
            ha='center', va='center', fontsize=9, color='#555555')

    plt.tight_layout(pad=0)
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close()
    return buf


# ==========================================
# THE PHASE 2 GATEKEEPER (BOUNCER)
# ==========================================
phase_2_modules = [
    "Module 6: The Blueprint",
    "Module 7: The Time Machine",
    "Module 8: The SQL Surgeon",
    "Module 9: The Output Architect"
]

# If they clicked a Phase 2 module, but haven't unlocked it yet...
if current_module in phase_2_modules and st.session_state['phase2_unlocked'] == False:
    st.title("🔒 Phase 2 is Locked")
    st.markdown("### Welcome to The Architect Level.")
    st.warning(
        "You must receive the master password from the instructor to proceed. You should only be here if you have completely mastered Phase 1.")

    # The password input box
    entered_password = st.text_input("Enter Password to Unlock Phase 2:", type="password")

    if st.button("Unlock"):
        if entered_password == "Architect2026":  # <-- You can change this password!
            st.session_state['phase2_unlocked'] = True
            st.success("Access Granted! Reloading...")
            st.rerun()
        else:
            st.error("🚨 Incorrect Password.")

    # This acts as a brick wall, preventing Python from rendering the locked module!
    st.stop()

# ==========================================
# 🏠 HOME / LANDING PAGE
# ==========================================
if current_module == "🏠 Home":
    st.markdown("""
    <style>
    .hero-title { font-size: 3rem; font-weight: 800; margin-bottom: 0; }
    .hero-sub   { font-size: 1.25rem; color: #888; margin-top: 0.25rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="hero-title">🧹 Python for Data Janitors</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">The no-fluff Python course built for people who live in spreadsheets.</p>',
                unsafe_allow_html=True)
    st.write("---")

    st.markdown("""
    ### What is this?
    This is a hands-on Python course for analysts, ops people, and anyone who has ever spent a Friday afternoon copy-pasting between Excel tabs.

    You won't be building apps or websites. You'll be doing the **real stuff** — cleaning messy CRM exports, stacking monthly files automatically, and turning raw numbers into charts your boss can actually read.
    """)

    st.write("---")
    st.markdown("### 📚 What You'll Build")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(
            "**📍 Module 0: Ground Zero**\nGet Python talking to your files. The hardest part — and you'll nail it first.")
    with col2:
        st.info(
            "**🧹 Module 1: The Data Janitor**\nFix broken names, phones, emails, and dates. Automate the cleanup work you do by hand every week.")
    with col3:
        st.info(
            "**🧩 Module 2: The Matchmaker**\nRename columns, kill duplicates, filter junk, and replace VLOOKUP forever with a real merge.")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.info(
            "**📊 Module 3: Pivot Table Pro**\nGroup, sum, and aggregate data the way Excel Pivot Tables always promised but never delivered.")
    with col5:
        st.info(
            "**⚙️ Module 4: The Automation Engine**\nProcess an entire folder of CSV files in one script. No more opening each one by hand.")
    with col6:
        st.info(
            "**📈 Module 5: The Presentation Layer**\nTurn your clean data into line charts, bar charts, and pie charts your leadership can read.")

    st.write("---")
    st.markdown("### 🛠️ What You'll Need")
    st.markdown("""
    - **PyCharm** (free) installed on your computer
    - **Python** installed (PyCharm will walk you through it if not)
    - A willingness to break things and fix them
    - No prior experience required
    """)

    st.write("---")
    col_start, _, _ = st.columns([1, 2, 2])
    with col_start:
        if st.button("🚀 Let's Go → Start Setup", use_container_width=True):
            st.session_state.current_module = "🛠️ Setup: Before You Begin"
            st.rerun()

# ==========================================
# 🛠️ SETUP: BEFORE YOU BEGIN
# ==========================================
elif current_module == "🛠️ Setup: Before You Begin":
    st.title("🛠️ Before You Begin")
    st.subheader("Get Python, PyCharm, and Pandas on your computer")
    st.markdown(
        "This takes about **10–15 minutes** and you only have to do it once. Follow the three steps below in order.")
    st.write("---")

    with st.expander("Step 1: Install Python", expanded=True):
        st.markdown("""
        Python is the engine. We need to install it before anything else.

        1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
        2. Click the big yellow **"Download Python"** button — it will automatically pick the right version for your computer.
        3. Run the installer. 

        🚨 **Critical:** On the very first screen of the installer, check the box that says **"Add Python to PATH"** before you click Install. If you miss this, things will break later.

        4. Click **Install Now** and let it finish.
        5. When it's done, you can close the installer.
        """)
        st.success(
            "✅ How to know it worked: Open your terminal (search 'Command Prompt' on Windows) and type `python --version`. You should see a version number, not an error.")

    with st.expander("Step 2: Install PyCharm"):
        st.markdown("""
        PyCharm is the garage where you'll write and run your Python scripts. We want the free version.

        1. Go to **[jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/)**
        2. Scroll down to **PyCharm Community Edition** — that's the free one. Click **Download**.
        3. Run the installer and click through the defaults — you don't need to change anything.
        4. Open PyCharm once it's installed.
        5. On the welcome screen, click **New Project**, give it any name, and click **Create**.
        """)
        st.success(
            "✅ How to know it worked: You should see a code editor open with a blank file. That's your workspace!")

    with st.expander("Step 3: Install Pandas & Matplotlib"):
        st.markdown("""
        Pandas is the library that lets Python read and work with spreadsheets. Matplotlib makes charts. We install both using a tool called `pip` — it comes bundled with Python automatically.

        1. Inside PyCharm, look at the bottom of the screen and click the **Terminal** tab.
        2. A command line will open at the bottom. Type this and hit Enter:
        ```
        pip install pandas matplotlib
        ```
        3. You'll see a bunch of text scroll by. That's normal — it's downloading the libraries.
        4. Wait for it to finish. It usually takes 30–60 seconds.
        """)
        st.success(
            "✅ How to know it worked: The last line should say something like `Successfully installed pandas...`. If you see that, you're done!")

    with st.expander("🆘 Something went wrong?"):
        st.markdown("""
        **"Python is not recognized as a command"** You probably missed the "Add Python to PATH" checkbox during install. Uninstall Python, re-run the installer, and make sure to check that box.

        **PyCharm says "No Python interpreter selected"** Click the interpreter selector in the bottom-right corner of PyCharm and select the Python version you installed.

        **pip install says "pip is not recognized"** Try `python -m pip install pandas matplotlib` instead.

        Still stuck? Google the exact error message — Stack Overflow will have the answer. This is a rite of passage for every developer. 😅
        """)

    st.write("---")
    st.success("🎉 All three steps done? You're ready to write your first script. Head to Module 0!")
    next_module_button(current_module)


# ==========================================
# PHASE 1 LANDING PAGE
# ==========================================
elif current_module == "--- PHASE 1: THE BASICS ---":
    st.title("🧹 Phase 1: The Data Janitor")
    st.subheader("Mastering the Foundation")

    st.markdown("""
    Welcome to Phase 1. Before you can build skyscrapers, you have to learn how to clear the rubble. 

    In this phase, you will learn the fundamental skills required to take messy, human-entered data and force it into clean, predictable formats that computers can actually read.

    ### Your Curriculum:
    * **Module 0: Ground Zero** - How to open and save files using Python.
    * **Module 1: The Data Janitor** - Formatting text, fixing blanks, and standardizing dates.
    * **Module 2: The Matchmaker** - Mapping headers, dropping duplicates, and VLOOKUPs (Joins).
    * **Module 3: The Pivot Table Upgrader** - Grouping and summarizing massive datasets.
    * **Module 4: The Automation Engine** - Using loops to process 100 files at once.
    * **Module 5: The Presentation Layer** - Turning your clean data into visual charts.

    👈 **Click Module 0 in the sidebar to begin your training!**
    """)


# ==========================================
# MODULE 0: GROUND ZERO
# ==========================================
elif current_module == "Module 0: Ground Zero":
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
barrett,  Williams,Barrett@email.com,,2025-12-01T18:45:00.000Z
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

        **Your Final Mission:** Rewrite your script to look like this. We are going to add **two lines of cleaning code** right in the middle to fix the messy names (like "jOhN") and the messy emails (like "BARRETT@email.com").

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
    st.success(
        "✅ **What you just learned:** How to import a library, read a CSV from a file path, and save a new file with code. This is the foundation everything else is built on.")
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

    tab1, tab2, tab3, tab4, tab_boss = st.tabs([
        "Challenge 1: Text",
        "Challenge 2: Blanks",
        "Challenge 3: Phones",
        "Challenge 4: Dates",
        "🏁 Boss Level"
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

    with tab_boss:
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
                    st.session_state['mod1_passed'] = True
                    st.success("🎉 BOOM! You successfully scrubbed the data!")
                    st.balloons()
                    st.dataframe(clean_df)
                    st.write("---")
                    st.success(
                        "✅ **What you just learned:** `.str` methods for text cleaning, `.fillna()` and `.dropna()` for missing data, regex for pattern replacement, and date parsing with `pd.to_datetime()`.")
                    next_module_button(current_module)
                else:
                    st.error("🚨 Not quite! The 'Email' column still has some issues.")
                    if missing_emails > 0:
                        st.warning(
                            f"Hint: I still see {missing_emails} completely blank email addresses. Check Challenge 2!")
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
Violet,Smith,Violet.smith@email.com,555-0100,03/01/2026
Bob,Jones,bjones@email.com,555-0200,03/02/2026
Violet,Smith,Violet.smith@email.com,555-0100,03/03/2026
Test,User,test@python4u.com,555-9999,03/03/2026
Charlie,Brown,charlie.b@email.com,555-0300,03/04/2026
QA,Tester,qa.lead@python4u.com,555-8888,03/04/2026
Bob,Jones,bjones@email.com,555-0200,03/05/2026"""

        st.download_button(
            label="📥 Download CRM_Export_V2.csv",
            data=module2_data,
            file_name="CRM_Export_V2.csv",
            mime="text/csv"
        )

    with col2:
        roster_data = """Email,Assigned_Property
Violet.smith@email.com,Lakeside
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

    tab1, tab2, tab3, tab4, tab_boss = st.tabs([
        "Challenge 1: Mapping",
        "Challenge 2: Duplicates",
        "Challenge 3: The Filter",
        "Challenge 4: Joins (VLOOKUP)",
        "🏁 Boss Level"
    ])

    with tab1:
        st.subheader("Challenge 1: The Column Shape-Shifter")
        st.markdown("""
        **Your Mission:** A new CRM export just came in, but the columns are named weirdly. 
        Rename `Applicant_First` to `First_Name` and `Mail_Address` to `Email` so they match our standard format.
        """)
        with st.expander("💡 Need a hint?"):
            st.write(
                "Use `.rename()` with a Python Dictionary! A dictionary is just a mapping of `{'Old_Name': 'New_Name'}`.")
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
        Find any row where the `Email` contains `@python4u.com` and completely remove it from the dataset.
        """)
        with st.expander("💡 Need a hint?"):
            st.write(
                "The `~` symbol in Python means 'NOT'. We are telling Pandas: Keep the rows where the email does NOT contain our company domain.")
            st.code("""
# The ~ symbol flips the search to find the opposite!
df = df[~df['Email'].str.contains('@python4u.com', na=False)]
            """, language="python")

    with tab4:
        st.subheader("Challenge 4: The VLOOKUP Upgrade (Joins)")
        st.markdown("""
        **Your Mission:** Load `Property_Roster.csv` as a second dataframe and merge it into your main data so every lead has an `Assigned_Property` attached to them based on their email.
        """)
        with st.expander("💡 Need a hint?"):
            st.write(
                "In Python, we don't VLOOKUP. We Merge. It's infinitely faster and won't crash your computer. ***Bonus-*** Challenge yourself to make a variable at the top of your script, like df2=")
            st.code("""
# 1. Load the second file
roster_df = pd.read_csv(r"C:\\Your\\Path\\Property_Roster.csv")

# 2. Merge them together (telling Python to match them on the 'Email' column)
df = pd.merge(df, roster_df, on='Email', how='left')
            """, language="python")

    with tab_boss:
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
                    no_tests = not mod2_df['Email'].str.contains('@python4u.com', na=False).any()

                if cols_correct and no_dupes and no_tests:
                    st.session_state.completed.add(current_module)
                    st.session_state['mod2_passed'] = True
                    st.success("🎉 INCREDIBLE! You mapped, deduplicated, filtered, and joined like a pro!")
                    st.balloons()
                    st.dataframe(mod2_df)
                    st.write("---")
                    st.success(
                        "✅ **What you just learned:** `.rename()` to standardize columns, `.drop_duplicates()` to kill dupes, boolean filtering with `~` to remove junk rows, and `pd.merge()` to replace VLOOKUP forever.")
                    next_module_button(current_module)
                else:
                    st.error("🚨 Not quite! There's still some junk in the trunk.")
                    if not cols_correct:
                        st.warning(
                            "Hint: Check Challenges 1 & 4. I'm missing 'First_Name', 'Email', or 'Assigned_Property'.")
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
Olivia,10,50000,Lakeside,1B1B,1500,1
Barrett,8,32000,Riverside,2B2B,2000,1
Olivia,5,20000,Lakeside,2B2B,2200,1
Barrett,12,60000,Riverside,1B1B,1400,0
Violet,15,45000,Lakeside,1B1B,1500,1"""

    st.download_button(
        label="📥 Download Transactions.csv",
        data=module3_data,
        file_name="Transactions.csv",
        mime="text/csv"
    )

    # Live preview metrics from the sample data
    st.write("---")
    st.write("### 📌 A Sneak Peek: What This Data Becomes")
    st.caption(
        "This is what your finished groupby output will look like — presented as a real dashboard metric card. By the end of this module, you'll have built the numbers behind these.")
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
    tab1, tab2, tab3, tab_boss = st.tabs(
        ["Challenge 1: Leaderboard", "Challenge 2: Custom Math", "Challenge 3: Roll-Up", "🏁 Boss Level"])

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

    with tab_boss:
        st.subheader("🏁 The Boss Level: Check Your Work")
        st.info(
            "Upload your final leaderboard CSV. It needs the `Net_Sales_Per_Appt` column and should have one row per Sales Rep (3 reps = 3 rows).")

        uploaded_mod3 = st.file_uploader("Drop your Grouped Output here", type="csv")
        if uploaded_mod3 is not None:
            try:
                mod3_df = pd.read_csv(uploaded_mod3)
                has_col = 'Net_Sales_Per_Appt' in mod3_df.columns
                right_rows = len(mod3_df) <= 3

                if has_col and right_rows:
                    st.session_state.completed.add(current_module)
                    st.session_state['mod3_passed'] = True
                    st.success("🎉 NAILED IT! You just out-pivoted Excel!")
                    st.balloons()
                    st.dataframe(mod3_df)
                    st.write("---")
                    st.success(
                        "✅ **What you just learned:** `.groupby()` for pivot-table-style summaries, grouping multiple columns at once, `.agg()` for mixed math, and creating calculated columns from grouped results.")
                    next_module_button(current_module)
                else:
                    st.error("🚨 Almost there!")
                    if not has_col:
                        st.warning(
                            "Hint: I don't see a `Net_Sales_Per_Appt` column. Make sure you completed Challenge 2 and saved that column into your output file.")
                    if not right_rows:
                        st.warning(
                            f"Hint: I'm seeing {len(mod3_df)} rows but expected 3 (one per Sales Rep). Make sure you grouped by `Sales_Rep` before saving.")
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
    st.write(
        "Download these two files and put them in a new folder called `Monthly_Stack` inside your `Python_Playground` folder.")

    north_data = """Rep,Region,Leads,Closed_Deals,Revenue
Violet,North,45,12,60000
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
    tab1, tab2, tab3, tab_boss = st.tabs(
        ["Challenge 1: Monthly Stack", "Challenge 2: Multi-CRM", "Challenge 3: Portfolio Loop", "🏁 Boss Level"])

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

    with tab_boss:
        st.subheader("🏁 The Boss Level: Check Your Work")
        st.info(
            "Stack both region files and save the combined output as a CSV. It should have all 10 reps and a `Source_File` column. Upload it here!")

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
                    st.session_state['mod4_passed'] = True
                    st.success("🎉 AUTOMATED! You just processed an entire folder of files in one script!")
                    st.balloons()
                    st.dataframe(mod4_df)
                    st.write("---")
                    st.success(
                        "✅ **What you just learned:** `glob` to find files by pattern, `for` loops to process them one by one, `pd.concat()` to stack dataframes, and `os.path.basename()` to track data sources.")
                    next_module_button(current_module)
                else:
                    st.error("🚨 Not quite!")
                    if not enough_rows:
                        st.warning(
                            f"Hint: I only see {len(mod4_df)} rows. Both region files together should give you 10 reps. Did you stack both files?")
                    if not has_source:
                        st.warning(
                            "Hint: I don't see a `Source_File` column. Make sure you completed Challenge 3 and added the filename as a column!")
                    if has_source and not has_both_regions:
                        st.warning(
                            "Hint: Looks like only one region made it in. Make sure your glob is picking up both North and South files.")

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
    tab1, tab2, tab3, tab_boss = st.tabs(
        ["Challenge 1: Trend Tracker", "Challenge 2: Portfolio Bar", "Challenge 3: Status Pie", "🏁 Boss Level"])

    with tab1:
        st.subheader("Challenge 1: The Trend Tracker")
        st.markdown("**Your Mission:** Generate a line chart showing monthly revenue growth.")
        with st.expander("💡 Need a hint?"):
            st.code("""
# If you get an ImportError, run: pip install matplotlib
""")
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

    with tab_boss:
        st.subheader("🖼️ The Boss Level: The Digital Fridge")
        st.info(
            "In your script, use `plt.savefig()` to save your chart directly to your Python_Playground folder on your Desktop:\n\n"
            "`plt.savefig(r'C:/Users/YourName/Desktop/Python_Playground/my_chart.png')`\n\n"
            "Then upload your masterpiece here to complete the course!"
        )
        uploaded_chart = st.file_uploader("Drop your Chart Image (.png or .jpg) here", type=["png", "jpg", "jpeg"])

        if uploaded_chart is not None:
            st.session_state.completed.add(current_module)
            st.session_state['mod5_passed'] = True
            st.success("🎉 GRADUATION COMPLETE! You are officially a Data Janitor!")
            st.balloons()
            st.image(uploaded_chart, caption="Your Python Masterpiece, proudly displayed on the digital fridge.")
            st.write("---")
            st.success(
                "✅ **What you just learned:** `matplotlib` for chart creation, `.plot()` with `kind=` to switch chart types, and `.value_counts()` to summarize categorical data before plotting.")

# ==========================================
# PHASE 1 GRADUATION
# ==========================================
elif current_module == "🎓 Phase 1 Graduation":
    st.title("🎓 Phase 1 Graduation")

    # Check if they actually passed everything!
    passed_all = all([
        st.session_state['mod1_passed'],
        st.session_state['mod2_passed'],
        st.session_state['mod3_passed'],
        st.session_state['mod4_passed'],
        st.session_state['mod5_passed']
    ])

    if not passed_all:
        st.warning(
            "🚨 You haven't completed all the Phase 1 modules yet! Check the sidebar menu to see which ✅ checkmarks you are missing.")
    else:
        st.balloons()
        st.success("🎉 CONGRATULATIONS! You have successfully completed Phase 1: The Data Janitor.")
        st.markdown("""
        You've proven you can write Python code to format text, destroy duplicates, group massive datasets, automate file loops, and generate visual charts.

        **The spreadsheet fears you.**
        """)

        st.write("---")
        st.subheader("📜 Claim Your Certificate")
        grad_name = st.text_input("Enter your name as you want it to appear on the certificate:",
                                  placeholder="e.g. Amanda Salvador")

        if grad_name:
            cert_buf = generate_certificate(grad_name)
            st.image(cert_buf, caption="Right-click the image to save it, or use the download button below!")
            st.download_button(
                label="📥 Download Official Certificate",
                data=cert_buf,
                file_name="DataJanitor_Certificate.png",
                mime="image/png"
            )

        st.write("---")
        st.info(
            "Ready for the next challenge? Get the master password from your instructor and click on **Module 6** to begin Phase 2: The Architect.")
# ==========================================
# PHASE 2 LANDING PAGE
# ==========================================

elif current_module == "--- PHASE 2: THE ARCHITECT ---":
    st.title("🏗️ Phase 2: The Architect")
    st.subheader("From Writing Scripts to Building Systems")

    st.markdown("""
    You have mastered the broom. Now it is time to build. 

    In the real world, developers rarely write code from scratch. **SharePoint connections, APIs, and custom functions can be incredibly challenging to set up.** That is part of the reason it is almost always easier to take an old script that already has the hard parts figured out, strip it down, and modify it for your new needs.

    In this phase, we are going to take an existing production script and repurpose it to build a brand new Journey Suppression tool.

    ### Your Curriculum:
    * **Module 6: The Blueprint** - Changing where a script looks for its input files.
    * **Module 7: The Time Machine** - Replacing hardcoded dates with dynamic, automated calendars.
    * **Module 8: The SQL Surgeon** - Injecting Python variables directly into Snowflake queries.
    * **Module 9: The Output Architect** - Generating dynamic filenames based on today's date.

    🚨 **Note:** Phase 2 is locked! 
    👈 **Click Module 6 in the sidebar and enter the master password to unlock this phase.**
    """)
# ==========================================
# MODULE 6: THE BLUEPRINT
# ==========================================
elif current_module == "Module 6: The Blueprint":
    st.title("🏗️ The Blueprint")
    st.subheader("Phase 2 | Module 6: Rewiring the Inputs")
    st.markdown("""
    Welcome to Phase 2. You are taking a massive, 300-line production script (`sp_lookbacks.py`) and stripping it down to build something new. 

    The first step in rewiring a script is changing where it looks for instructions.
    """)
    st.write("---")

    st.subheader("Challenge: The SharePoint Reroute")
    st.markdown("""
    **The Scenario:** The old script looks for a template file in `Data Analytics/Shopper Suite/Lookbacks/Templates`. 

    Before writing any code, go to SharePoint and physically build this new folder path: `Data Governance/Suppression/By Journey/Templates`. Then, upload your new, simpler CSV template there.

    Our new CSV template is much simpler. We only need to pull 5 specific columns from it to power our script.
    """)

    with st.expander("💡 See how to strip it down"):
        st.write(
            "In Python, we use variables to store these paths so we only have to type them once. Here is what your new setup block should look like:")
        st.code("""
# 1. Update the folder locations
MAIN_FOLDER = 'Data Governance/Suppression/By Journey'
TEMPLATE_FOLDER = f'{MAIN_FOLDER}/Templates'
TEMPLATE_FILENAME = 'Journey_Suppression_Template.csv'

# 2. Pretend we loaded the CSV. Now we extract just the 5 variables we need for this specific run:
client_name = str(row.get('client_name', '')).strip()
ohq = str(row.get('ohq', '')).strip()
source_client_id = str(row.get('source_client_id', '')).strip()
segment = str(row.get('segment', '')).strip()
        """, language="python")

    st.info("Check off this module once you understand how to re-route folder paths in an existing script!")
    if st.button("✅ I understand how to change inputs"):
        st.session_state['mod6_passed'] = True
        st.session_state.completed.add(current_module)
        st.balloons()  # <-- Celebration added!
        st.success("🎉 Blueprint Secured! Great job.")
        next_module_button(current_module)

# ==========================================
# MODULE 7: THE TIME MACHINE
# ==========================================
elif current_module == "Module 7: The Time Machine":
    st.title("⏳ The Time Machine")
    st.subheader("Phase 2 | Module 7: Static vs. Dynamic Dates")
    st.markdown("""
    If you hardcode dates into a script, you have to manually edit the code every single time you run it. We want Python to be smart enough to figure out the dates itself.

    Our business rule: **We always want the data from the 1st of the current month up to today.**
    """)
    st.write("---")

    tab1, tab2 = st.tabs(["Step 1: The Static Way (Beginner)", "Step 2: The Dynamic Way (Pro)"])

    with tab1:
        st.markdown(
            "**The Static Way** means typing the exact strings into the code. It works, but it requires human intervention next month.")
        st.code("""
# This works today, but it will be wrong next month!
start_date = '2026-03-01'
end_date = '2026-03-12'
        """, language="python")

    with tab2:
        st.markdown(
            "**The Dynamic Way** uses Python's built-in `datetime` library to act as a calendar. It calculates the 1st of the month automatically, no matter what day you run the script.")
        st.code("""
from datetime import date

# Get today's exact date
today = date.today()

# Tell Python: "Take today's date, but rewind the day to the 1st"
start_of_month = today.replace(day=1)

# Format them into strings so the SQL database can read them (YYYY-MM-DD)
start_date = start_of_month.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

print(f"Running data from {start_date} to {end_date}")
        """, language="python")

    st.info(
        "Dynamic dates are the secret to true automation. Once you master `strftime`, you never have to type a date manually again.")
    if st.button("✅ I've mastered time travel"):
        st.session_state['mod7_passed'] = True
        st.session_state.completed.add(current_module)
        st.balloons()  # <-- Celebration added!
        st.success("🎉 Time Machine activated! Next stop: SQL.")
        next_module_button(current_module)

# ==========================================
# MODULE 8: THE SQL SURGEON
# ==========================================
elif current_module == "Module 8: The SQL Surgeon":
    st.title("🩺 The SQL Surgeon")
    st.subheader("Phase 2 | Module 8: Injecting Variables into Queries")
    st.markdown("""
    The original `sp_lookbacks.py` script has a massive, 50-line SQL query with complex joins. Our new script doesn't need all that. 

    We need to write a clean, simple query and **inject** the variables we created in Modules 6 and 7 directly into the SQL text.
    """)
    st.write("---")

    st.markdown("### Python f-strings")
    st.write(
        "By putting an `f` before the quotes, we can inject Python variables directly into our SQL query using curly braces `{}`.")

    st.code("""
# Notice the 'f' right before the triple quotes!
sql_query = f'''
    SELECT 
        addressid,
        full_address,
        segment,
        result_date
    FROM 
        daily_client_households
    WHERE 
        source_client_id = '{source_client_id}'
        AND result_date BETWEEN '{start_date}' AND '{end_date}'
        AND LOWER(segment) LIKE '%{segment}%'
'''

# Now we send that dynamic query to Snowflake
df_raw = sfc(sql_query)
    """, language="python")

    st.success(
        "By doing it this way, the SQL query rebuilds itself perfectly for every single row in your SharePoint CSV template!")
    if st.button("✅ I understand SQL injection"):
        st.session_state['mod8_passed'] = True
        st.session_state.completed.add(current_module)
        st.balloons()  # <-- Celebration added!
        st.success("🎉 Surgery complete! The variables are in.")
        next_module_button(current_module)

# ==========================================
# MODULE 9: THE OUTPUT ARCHITECT
# ==========================================
elif current_module == "Module 9: The Output Architect":
    st.title("📦 The Output Architect")
    st.subheader("Phase 2 | Module 9: Dynamic Filenames")
    st.markdown("""
    You've pulled the data. Now we need to save it exactly the way the business asked for it. 

    The requirement is strict: Every output file must follow the exact naming convention: `ohq__generic__sales__{firstdayofthemonth}.csv`.
    """)
    st.write("---")

    st.markdown("### Constructing the Filename")
    st.write(
        "We will use our dynamic date tool from Module 7 to figure out the 1st of the current month, format it as `yymmdd`, and use an f-string to piece it all together.")

    st.code("""
from datetime import date

# 1. Grab the 1st of the current month and format it as YYMMDD (e.g., 260301)
first_day_of_month = date.today().replace(day=1).strftime('%y%m%d')

# 2. Build the filename using the OHQ variable we grabbed in Module 6
# It will look like: 12345__generic__sales__260301.csv
final_filename = f"{ohq}__generic__sales__{first_day_of_month}.csv"

# 3. Save the dataframe to that file
df_raw.to_csv(final_filename, index=False)

print(f"Successfully saved: {final_filename}")
    """, language="python")

    st.info(
        "Check this off to complete Phase 2. You now have all the puzzle pieces to strip down the Lookbacks script and build the new Journey Suppression script!")

    if st.button("✅ I am officially a Script Architect", use_container_width=True):
        st.session_state['mod9_passed'] = True
        st.session_state.completed.add(current_module)
        st.balloons()

        # THE BIG PHASE 2 PAYOFF REVEAL
        st.write("---")
        st.markdown("""
        <h1 style='text-align: center; color: #4fc3f7; font-size: 3em;'>🏗️ SYSTEM ONLINE 🏗️</h1>
        <h3 style='text-align: center; color: #aaaaaa;'>You are officially a Data Architect.</h3>
        <br>
        """, unsafe_allow_html=True)

        st.success(
            "🎉 **PHASE 2 COMPLETE!** You have successfully learned how to dismantle a production script and rewire it into a brand new automation tool.")

        # Displaying their new "Architect Stats"
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Folder Inputs", "Rewired 🔌")
        col2.metric("Date Logic", "Automated ⏳")
        col3.metric("SQL Queries", "Injected 💉")
        col4.metric("File Outputs", "Dynamic 📦")

        st.write("---")
        st.markdown("""
        ### 🚀 Your Final Mission
        You no longer just clean data. You build the systems that process it. 

        Your training is complete. Open up PyCharm, make a copy of the old `sp_lookbacks.py` script, and start building the real **Journey Suppression** tool for the business!
        """)

# ==========================================
# 📝 FEEDBACK
# ==========================================
elif current_module == "📝 Feedback":
    st.title("📝 Course Feedback")
    st.markdown("Thank you for taking the course! Your feedback helps make it better for the next person.")
    st.write("---")

    overall = st.select_slider(
        "Overall, how would you rate the course?",
        options=["⭐ Poor", "⭐⭐ Fair", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Great", "⭐⭐⭐⭐⭐ Excellent"],
        value="⭐⭐⭐⭐ Great"
    )

    hardest = st.selectbox(
        "Which module was the hardest?",
        ["Module 0: Ground Zero", "Module 1: The Data Janitor", "Module 2: The Matchmaker",
         "Module 3: The Pivot Table Upgrader", "Module 4: The Automation Engine",
         "Module 5: The Presentation Layer", "They were all equally brutal 😅"]
    )

    fave = st.selectbox(
        "Which module was your favorite?",
        ["Module 0: Ground Zero", "Module 1: The Data Janitor", "Module 2: The Matchmaker",
         "Module 3: The Pivot Table Upgrader", "Module 4: The Automation Engine",
         "Module 5: The Presentation Layer"]
    )

    comments = st.text_area(
        "Any other thoughts? What was confusing? What did you love?",
        placeholder="Write anything here...",
        height=150
    )

    recommend = st.radio(
        "Would you recommend this course to a coworker?",
        ["Yes, absolutely!", "Maybe", "Probably not"]
    )

    st.write("")
    if st.button("Submit Feedback ✅", use_container_width=False):
        saved = save_feedback_to_sheet(overall, hardest, fave, recommend, comments)
        st.success("🙏 Thank you! Your feedback means a lot and will help make this course better.")
        st.balloons()
        st.markdown(f"""
        **Here's what you submitted:**
        - Rating: {overall}
        - Hardest module: {hardest}
        - Favorite module: {fave}
        - Would recommend: {recommend}
        """)
        if comments:
            st.info(f"💬 Your comment: *\"{comments}\"*")
        if not saved:
            st.warning("⚠️ Feedback couldn't be saved to the sheet — but thank you anyway!")