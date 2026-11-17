import streamlit as st
import pandas as pd
import os
from datetime import date

from expense_manager import (
    load_expenses,
    add_expense,
    update_expense,
    delete_expense,
    set_monthly_budget,
    get_monthly_budget
)

# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Student Life Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# FILES
# ==================================================

SUBJECT_FILE = "subjects.csv"
STUDY_FILE = "study_sessions.csv"
SCHEDULE_FILE = "schedule.csv"
FITNESS_FILE = "fitness.csv"
GOAL_FILE = "fitness_goals.csv"

# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #FFF5F5, #FFF0F5, #FFF9EB);
    color: #292929;
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1500px;
}

h1, h2, h3, h4 {
    color: #292929 !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF0F5, #FFF9EB);
}

.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #F4D9E4;
    border-radius: 20px;
    height: 230px;
    width: 100%;
    box-sizing: border-box;
    padding: 20px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    overflow: hidden;
}

.card-icon {
    font-size: 43px;
    margin-bottom: 18px;
}

.card-title {
    font-size: 20px;
    font-weight: 650;
    color: #292929;
    white-space: nowrap;
    margin-bottom: 12px;
}

.card-description {
    font-size: 13px;
    color: #777777;
}

div.stButton > button {
    width: 100%;
    min-height: 43px;
    background: #FFFFFF;
    color: #44334D;
    border: 1px solid #EEC5D7;
    border-radius: 13px;
    font-size: 14px;
}

div.stButton > button:hover {
    background: #FFF0F5;
    color: #8B4768;
    border: 1px solid #E5AFC7;
}

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    border-radius: 10px;
    border: 1px solid #EACDDA;
    background: #FFFFFF;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #F4D9E4;
    border-radius: 15px;
    padding: 16px;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #F4D9E4;
    border-radius: 15px;
    padding: 20px;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #F4D9E4;
    border-radius: 12px;
}

.stProgress > div > div > div {
    background-color: #E9AFC7;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def create_csv(filename, columns):
    if not os.path.exists(filename):
        pd.DataFrame(columns=columns).to_csv(filename, index=False)


def read_csv(filename, columns):
    create_csv(filename, columns)
    df = pd.read_csv(filename)

    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df


def save_csv(filename, df):
    df.to_csv(filename, index=False)


def next_id(df):
    if df.empty or "ID" not in df.columns:
        return 1

    ids = pd.to_numeric(
        df["ID"], errors="coerce"
    ).dropna()

    return int(ids.max()) + 1 if not ids.empty else 1


# ==================================================
# NAVIGATION FUNCTION
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def go_to_page(page):
    st.session_state.page = page
    st.session_state.main_navigation = page


# ==================================================
# CREATE DATA FILES
# ==================================================

subjects = read_csv(
    SUBJECT_FILE, ["ID", "Subject", "Target_Hours"]
)

study = read_csv(
    STUDY_FILE, ["ID", "Date", "Subject", "Duration", "Topic"]
)

schedule = read_csv(
    SCHEDULE_FILE,
    ["ID", "Date", "Time", "Task", "Category", "Priority", "Status"]
)

fitness = read_csv(
    FITNESS_FILE,
    ["ID", "Date", "Steps", "Water_Glasses", "Workout_Minutes", "Notes"]
)

create_csv(
    GOAL_FILE,
    ["Steps", "Water_Glasses", "Workout_Minutes"]
)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.title("🎓 Student Life Hub")
    st.caption("Your personal student dashboard")

    st.divider()

    pages = [
        "Dashboard",
        "Expenses",
        "Study Planner",
        "Fitness",
        "Schedule"
    ]

    if "main_navigation" not in st.session_state:
        st.session_state.main_navigation = st.session_state.page

    selected_page = st.radio(
        "MENU",
        pages,
        key="main_navigation"
    )

    st.session_state.page = selected_page

    st.divider()
    st.caption("Organize your day. Achieve your goals. 🌸")


# ==================================================
# DASHBOARD
# ==================================================

if st.session_state.page == "Dashboard":

    st.title("Welcome to your Dashboard")
    st.write("Choose a section to manage your daily activities.")

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">💰</div>
            <div class="card-title">Expenses</div>
            <div class="card-description">Manage your money</div>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Expenses",
            key="dashboard_expenses",
            on_click=go_to_page,
            args=("Expenses",)
        )

    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">📚</div>
            <div class="card-title">Study Planner</div>
            <div class="card-description">Track academic progress</div>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Study Planner",
            key="dashboard_study",
            on_click=go_to_page,
            args=("Study Planner",)
        )

    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">💪</div>
            <div class="card-title">Fitness</div>
            <div class="card-description">Track your fitness</div>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Fitness",
            key="dashboard_fitness",
            on_click=go_to_page,
            args=("Fitness",)
        )

    with col4:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">📅</div>
            <div class="card-title">Schedule</div>
            <div class="card-description">Plan daily activities</div>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Open Schedule",
            key="dashboard_schedule",
            on_click=go_to_page,
            args=("Schedule",)
        )

    st.write("")
    st.divider()

    st.header("Your Overview")

    expense_df = load_expenses()
    total_expenses = (
        expense_df["Amount"].sum()
        if not expense_df.empty else 0
    )

    subjects = read_csv(
        SUBJECT_FILE, ["ID", "Subject", "Target_Hours"]
    )

    schedule = read_csv(
        SCHEDULE_FILE,
        ["ID", "Date", "Time", "Task", "Category", "Priority", "Status"]
    )

    fitness = read_csv(
        FITNESS_FILE,
        ["ID", "Date", "Steps", "Water_Glasses", "Workout_Minutes", "Notes"]
    )

    pending_tasks = (
        len(schedule[schedule["Status"] != "Completed"])
        if not schedule.empty else 0
    )

    today = str(date.today())

    today_workouts = (
        len(fitness[fitness["Date"].astype(str) == today])
        if not fitness.empty else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    c2.metric("My Subjects", len(subjects))
    c3.metric("Pending Tasks", pending_tasks)
    c4.metric("Today's Workouts", today_workouts)

    st.divider()
    st.subheader("Your Upcoming Activities")

    if schedule.empty:
        st.info("No activities added yet. Open Schedule to add tasks.")
    else:
        pending = schedule[schedule["Status"] != "Completed"]

        if pending.empty:
            st.success("All your tasks are completed!")
        else:
            st.dataframe(
                pending[["Date", "Time", "Task", "Priority", "Status"]],
                use_container_width=True,
                hide_index=True
            )

    st.subheader("Your Study Progress")

    study = read_csv(
        STUDY_FILE, ["ID", "Date", "Subject", "Duration", "Topic"]
    )

    if not study.empty:
        study["Duration"] = pd.to_numeric(
            study["Duration"], errors="coerce"
        ).fillna(0)

        st.bar_chart(study.groupby("Subject")["Duration"].sum())
    else:
        st.info("Your study progress will appear here.")


# ==================================================
# EXPENSES
# ==================================================

elif st.session_state.page == "Expenses":

    st.title("💰 Expense Manager")
    st.write("Manage your daily expenses and monthly budget.")

    tab1, tab2, tab3 = st.tabs(
        ["Add Expense", "Transactions", "Budget & Analytics"]
    )

    with tab1:
        st.subheader("Add New Expense")

        with st.form("expense_form"):
            expense_date = st.date_input("Date", value=date.today())

            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Education", "Shopping",
                 "Entertainment", "Health", "Other"]
            )

            amount = st.number_input(
                "Amount (₹)", min_value=1.0, step=10.0
            )

            description = st.text_input("Description")

            submit = st.form_submit_button("Add Expense")

            if submit:
                add_expense(
                    expense_date, category, amount, description
                )
                st.success("Expense added successfully!")
                st.rerun()

    with tab2:
        st.subheader("Expense Transactions")

        expense_df = load_expenses()

        if expense_df.empty:
            st.info("No expenses recorded yet.")
        else:
            st.dataframe(
                expense_df,
                use_container_width=True,
                hide_index=True
            )

            expense_ids = pd.to_numeric(
                expense_df["ID"], errors="coerce"
            ).dropna().astype(int).tolist()

            if expense_ids:
                selected_id = st.selectbox(
                    "Select Expense ID", expense_ids
                )

                selected = expense_df[
                    pd.to_numeric(
                        expense_df["ID"], errors="coerce"
                    ) == selected_id
                ].iloc[0]

                with st.expander("Edit Selected Expense"):

                    parsed_date = pd.to_datetime(
                        selected["Date"], errors="coerce"
                    )

                    default_date = (
                        parsed_date.date()
                        if pd.notna(parsed_date)
                        else date.today()
                    )

                    categories = [
                        "Food", "Transport", "Education",
                        "Shopping", "Entertainment", "Health", "Other"
                    ]

                    old_category = str(selected["Category"])

                    category_index = (
                        categories.index(old_category)
                        if old_category in categories else 0
                    )

                    with st.form("edit_expense_form"):
                        edit_date = st.date_input(
                            "Date", value=default_date
                        )

                        edit_category = st.selectbox(
                            "Category",
                            categories,
                            index=category_index
                        )

                        edit_amount = st.number_input(
                            "Amount",
                            min_value=1.0,
                            value=max(1.0, float(selected["Amount"]))
                        )

                        edit_description = st.text_input(
                            "Description",
                            value=str(selected["Description"])
                        )

                        update = st.form_submit_button("Update Expense")

                        if update:
                            update_expense(
                                int(selected_id),
                                edit_date,
                                edit_category,
                                edit_amount,
                                edit_description
                            )
                            st.success("Expense updated!")
                            st.rerun()

                if st.button("Delete Selected Expense"):
                    delete_expense(int(selected_id))
                    st.success("Expense deleted!")
                    st.rerun()

    with tab3:
        st.subheader("Monthly Budget")

        budget = get_monthly_budget()

        st.metric("Current Budget", f"₹{budget:,.2f}")

        with st.form("budget_form"):
            new_budget = st.number_input(
                "Set Monthly Budget",
                min_value=1.0,
                value=float(budget),
                step=500.0
            )

            save_budget = st.form_submit_button("Save Budget")

            if save_budget:
                set_monthly_budget(new_budget)
                st.success("Budget updated!")
                st.rerun()

        expense_df = load_expenses()

        if not expense_df.empty:
            total = expense_df["Amount"].sum()
            remaining = budget - total

            c1, c2 = st.columns(2)
            c1.metric("Total Recorded Spending", f"₹{total:,.2f}")
            c2.metric("Remaining Budget", f"₹{remaining:,.2f}")

            st.progress(min(total / budget, 1.0))

            st.subheader("Category-wise Expenses")
            st.bar_chart(
                expense_df.groupby("Category")["Amount"].sum()
            )
        else:
            st.info("Add expenses to view analytics.")


# ==================================================
# STUDY PLANNER
# ==================================================

elif st.session_state.page == "Study Planner":

    st.title("📚 Study Planner")
    st.write("Organize your subjects and study sessions.")

    tab1, tab2, tab3 = st.tabs(
        ["My Subjects", "Study Sessions", "Progress Analytics"]
    )

    with tab1:
        st.subheader("Manage Your Subjects")

        with st.form("subject_form"):
            subject_name = st.text_input("Subject Name")

            target_hours = st.number_input(
                "Target Study Hours", min_value=1.0, step=1.0
            )

            add_subject = st.form_submit_button("Add Subject")

            if add_subject:
                if subject_name.strip():
                    df = read_csv(
                        SUBJECT_FILE,
                        ["ID", "Subject", "Target_Hours"]
                    )

                    new_row = pd.DataFrame([{
                        "ID": next_id(df),
                        "Subject": subject_name.strip(),
                        "Target_Hours": target_hours
                    }])

                    df = pd.concat([df, new_row], ignore_index=True)
                    save_csv(SUBJECT_FILE, df)

                    st.success("Subject added!")
                    st.rerun()
                else:
                    st.warning("Enter a subject name.")

        subjects = read_csv(
            SUBJECT_FILE, ["ID", "Subject", "Target_Hours"]
        )

        if not subjects.empty:
            st.subheader("Your Subjects")

            st.dataframe(
                subjects, use_container_width=True, hide_index=True
            )

            ids = pd.to_numeric(
                subjects["ID"], errors="coerce"
            ).dropna().astype(int).tolist()

            if ids:
                delete_id = st.selectbox(
                    "Select Subject ID to Delete", ids
                )

                if st.button("Delete Subject"):
                    subjects = subjects[
                        pd.to_numeric(
                            subjects["ID"], errors="coerce"
                        ) != delete_id
                    ]
                    save_csv(SUBJECT_FILE, subjects)
                    st.success("Subject deleted!")
                    st.rerun()
        else:
            st.info("No subjects added yet.")

    with tab2:
        st.subheader("Add Study Session")

        subjects = read_csv(
            SUBJECT_FILE, ["ID", "Subject", "Target_Hours"]
        )

        if subjects.empty:
            st.warning("Add a subject first.")
        else:
            subject_names = subjects["Subject"].dropna().tolist()

            with st.form("study_form"):
                study_date = st.date_input(
                    "Date", value=date.today()
                )

                selected_subject = st.selectbox(
                    "Subject", subject_names
                )

                duration = st.number_input(
                    "Study Duration (Hours)",
                    min_value=0.5,
                    step=0.5
                )

                topic = st.text_input("Topic Studied")

                save_study = st.form_submit_button(
                    "Save Study Session"
                )

                if save_study:
                    df = read_csv(
                        STUDY_FILE,
                        ["ID", "Date", "Subject", "Duration", "Topic"]
                    )

                    new_row = pd.DataFrame([{
                        "ID": next_id(df),
                        "Date": str(study_date),
                        "Subject": selected_subject,
                        "Duration": duration,
                        "Topic": topic
                    }])

                    df = pd.concat([df, new_row], ignore_index=True)
                    save_csv(STUDY_FILE, df)

                    st.success("Study session saved!")
                    st.rerun()

    with tab3:
        st.subheader("Study Progress")

        study = read_csv(
            STUDY_FILE, ["ID", "Date", "Subject", "Duration", "Topic"]
        )

        subjects = read_csv(
            SUBJECT_FILE, ["ID", "Subject", "Target_Hours"]
        )

        if not study.empty:
            study["Duration"] = pd.to_numeric(
                study["Duration"], errors="coerce"
            ).fillna(0)

            total_hours = study["Duration"].sum()

            st.metric("Total Study Hours", f"{total_hours:g} Hours")

            subject_hours = study.groupby("Subject")["Duration"].sum()
            st.bar_chart(subject_hours)

            st.subheader("Study History")

            st.dataframe(
                study, use_container_width=True, hide_index=True
            )

            for _, row in subjects.iterrows():
                name = row["Subject"]

                target = pd.to_numeric(
                    pd.Series([row["Target_Hours"]]),
                    errors="coerce"
                ).fillna(0).iloc[0]

                completed = subject_hours.get(name, 0)

                st.write(
                    f"**{name}: {completed:g} / {target:g} hours**"
                )

                progress = (
                    min(completed / target, 1.0)
                    if target > 0 else 0
                )

                st.progress(progress)
        else:
            st.info("Add study sessions to view progress.")


# ==================================================
# FITNESS
# ==================================================

elif st.session_state.page == "Fitness":

    st.title("💪 Fitness Tracker")
    st.write("Monitor your daily fitness activities.")

    tab1, tab2, tab3 = st.tabs(
        ["Daily Activity", "Fitness History", "Fitness Goals"]
    )

    with tab1:
        st.subheader("Record Daily Activity")

        with st.form("fitness_form"):
            fitness_date = st.date_input(
                "Date", value=date.today()
            )

            steps = st.number_input(
                "Steps Walked", min_value=0, step=500
            )

            water = st.number_input(
                "Water Intake (Glasses)", min_value=0
            )

            workout = st.number_input(
                "Workout Duration (Minutes)",
                min_value=0,
                step=5
            )

            notes = st.text_input("Notes")

            save_activity = st.form_submit_button("Save Activity")

            if save_activity:
                df = read_csv(
                    FITNESS_FILE,
                    ["ID", "Date", "Steps", "Water_Glasses",
                     "Workout_Minutes", "Notes"]
                )

                new_row = pd.DataFrame([{
                    "ID": next_id(df),
                    "Date": str(fitness_date),
                    "Steps": steps,
                    "Water_Glasses": water,
                    "Workout_Minutes": workout,
                    "Notes": notes
                }])

                df = pd.concat([df, new_row], ignore_index=True)
                save_csv(FITNESS_FILE, df)

                st.success("Activity saved!")
                st.rerun()

    with tab2:
        st.subheader("Fitness History")

        fitness = read_csv(
            FITNESS_FILE,
            ["ID", "Date", "Steps", "Water_Glasses",
             "Workout_Minutes", "Notes"]
        )

        if not fitness.empty:
            for column in [
                "Steps", "Water_Glasses", "Workout_Minutes"
            ]:
                fitness[column] = pd.to_numeric(
                    fitness[column], errors="coerce"
                ).fillna(0)

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Steps", f"{fitness['Steps'].sum():,.0f}")
            c2.metric(
                "Water Glasses",
                f"{fitness['Water_Glasses'].sum():,.0f}"
            )
            c3.metric(
                "Workout Minutes",
                f"{fitness['Workout_Minutes'].sum():,.0f}"
            )

            st.dataframe(
                fitness, use_container_width=True, hide_index=True
            )

            st.subheader("Steps History")
            st.bar_chart(fitness.set_index("Date")["Steps"])
        else:
            st.info("No fitness history available.")

    with tab3:
        st.subheader("Set Fitness Goals")

        goal_df = pd.read_csv(GOAL_FILE)

        if goal_df.empty:
            default_steps = 8000
            default_water = 8
            default_workout = 30
        else:
            default_steps = int(goal_df.iloc[0]["Steps"])
            default_water = int(goal_df.iloc[0]["Water_Glasses"])
            default_workout = int(goal_df.iloc[0]["Workout_Minutes"])

        with st.form("goal_form"):
            goal_steps = st.number_input(
                "Daily Steps Goal",
                min_value=1000,
                value=default_steps,
                step=500
            )

            goal_water = st.number_input(
                "Daily Water Goal",
                min_value=1,
                value=default_water
            )

            goal_workout = st.number_input(
                "Daily Workout Goal (Minutes)",
                min_value=5,
                value=default_workout,
                step=5
            )

            save_goals = st.form_submit_button("Save Goals")

            if save_goals:
                new_goals = pd.DataFrame([{
                    "Steps": goal_steps,
                    "Water_Glasses": goal_water,
                    "Workout_Minutes": goal_workout
                }])

                save_csv(GOAL_FILE, new_goals)

                st.success("Fitness goals saved!")
                st.rerun()

        st.write(f"🚶 Steps Goal: {default_steps:,}")
        st.write(f"💧 Water Goal: {default_water} glasses")
        st.write(f"🏋️ Workout Goal: {default_workout} minutes")


# ==================================================
# SCHEDULE
# ==================================================

elif st.session_state.page == "Schedule":

    st.title("📅 My Schedule")
    st.write("Plan your daily activities and tasks.")

    tab1, tab2 = st.tabs(["Add Task", "My Schedule"])

    with tab1:
        st.subheader("Add New Task")

        with st.form("schedule_form"):
            task_date = st.date_input(
                "Task Date", value=date.today()
            )

            task_time = st.time_input("Task Time")
            task_name = st.text_input("Task Name")

            category = st.selectbox(
                "Category",
                ["Study", "Assignment", "Exam", "Personal", "Other"]
            )

            priority = st.selectbox(
                "Priority", ["High", "Medium", "Low"]
            )

            add_task = st.form_submit_button("Add to Schedule")

            if add_task:
                if task_name.strip():
                    df = read_csv(
                        SCHEDULE_FILE,
                        ["ID", "Date", "Time", "Task",
                         "Category", "Priority", "Status"]
                    )

                    new_row = pd.DataFrame([{
                        "ID": next_id(df),
                        "Date": str(task_date),
                        "Time": str(task_time),
                        "Task": task_name,
                        "Category": category,
                        "Priority": priority,
                        "Status": "Pending"
                    }])

                    df = pd.concat([df, new_row], ignore_index=True)
                    save_csv(SCHEDULE_FILE, df)

                    st.success("Task added!")
                    st.rerun()
                else:
                    st.warning("Enter a task name.")

    with tab2:
        st.subheader("My Schedule")

        schedule = read_csv(
            SCHEDULE_FILE,
            ["ID", "Date", "Time", "Task",
             "Category", "Priority", "Status"]
        )

        if schedule.empty:
            st.info("No tasks scheduled yet.")
        else:
            schedule = schedule.sort_values(
                by=["Date", "Time"]
            )

            st.dataframe(
                schedule, use_container_width=True, hide_index=True
            )

            st.divider()

            ids = pd.to_numeric(
                schedule["ID"], errors="coerce"
            ).dropna().astype(int).tolist()

            selected_id = st.selectbox("Select Task ID", ids)

            selected_task = schedule[
                pd.to_numeric(
                    schedule["ID"], errors="coerce"
                ) == selected_id
            ].iloc[0]

            statuses = ["Pending", "In Progress", "Completed"]
            old_status = str(selected_task["Status"])

            status_index = (
                statuses.index(old_status)
                if old_status in statuses else 0
            )

            new_status = st.selectbox(
                "Update Task Status",
                statuses,
                index=status_index
            )

            if st.button("Update Task"):
                df = read_csv(
                    SCHEDULE_FILE,
                    ["ID", "Date", "Time", "Task",
                     "Category", "Priority", "Status"]
                )

                df.loc[
                    pd.to_numeric(
                        df["ID"], errors="coerce"
                    ) == selected_id,
                    "Status"
                ] = new_status

                save_csv(SCHEDULE_FILE, df)

                st.success("Task updated!")
                st.rerun()

            if st.button("Delete Selected Task"):
                df = read_csv(
                    SCHEDULE_FILE,
                    ["ID", "Date", "Time", "Task",
                     "Category", "Priority", "Status"]
                )

                df = df[
                    pd.to_numeric(
                        df["ID"], errors="coerce"
                    ) != selected_id
                ]

                save_csv(SCHEDULE_FILE, df)

                st.success("Task deleted!")
                st.rerun()


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown("""
<div style="text-align:center; color:#888888; padding:10px;">
    Made with 💗 | Student Life Hub | 2026
</div>
""", unsafe_allow_html=True)