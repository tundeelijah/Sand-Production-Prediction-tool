import streamlit as st
import pandas as pd
import numpy as np
import os
import time
if 'page' not in st.session_state:
    st.session_state['page'] = 0
if 'user_db' not in st.session_state:
        st.session_state['user_db'] = {}
if 'show_auth_dropdown' not in st.session_state:
    st.session_state['show_auth_dropdown'] = False 
# Call the function to load CSS for the specific page
if 'show_login' not in st.session_state:
    st.session_state['show_login'] = False
par1=0
par2=0
par3=0
par4=0
if 'par1' not in st.session_state:
    st.session_state['par1'] = 0
if 'par2' not in st.session_state:
    st.session_state['par2'] = 0
if 'par3' not in st.session_state:
    st.session_state['par3'] = 0
if 'par4' not in st.session_state:
    st.session_state['par4'] = 0

weights=[]
def all_inputs_filled(inputs):
    return all(bool(input_value) for input_value in inputs)

if 'criteria' not in st.session_state:
    st.session_state.criteria = {
        "core_sample": False,
        "formation_depth": False,
        "sonic_log": False,
        "porosity_data": False,
        "offset_field_data": False
    }

class ProductionEvaluator:
    def assign_weight(self, par1, par2, par3, par4):
        weights = []
        if par1 is None:
            par1 = 0
        if par2 is None:
            par2 = 0
        if par3 is None:
            par3 = 0
        if par4 is None:
            par4 = 0
        if par1 <= 50:
            weights.append(1)
        elif 50 < par1 < 95:
            weights.append(3)
        else:
            weights.append(5)

        if par2 < 20:
            weights.append(1)
        elif 20 < par2 < 30:
            weights.append(3)
        else:
            weights.append(5)

        if par3 <= 5000:
            weights.append(5)
        elif 5000 < par3 < 10000:
            weights.append(3)
        else:
            weights.append(1)

        if par4 >= 10000:
            weights.append(1)
        elif 8000 < par4 < 10000:
            weights.append(3)
        else:
            weights.append(5)

        return np.array(weights)

    def create_pairwise_matrix(self):
        return np.array([
            [1,  1/2,   1/3,   1/3,],
            [2,  1,   1/3,   1/3,],
            [3,  3,   1,   3, ],
            [3,  2,   1/3,   1, ],
        
        ])

    def can_produce_sand(self,par1, par2, par3, par4):
        weights = self.assign_weight(par1, par2, par3, par4)
        pairwise_matrix = self.create_pairwise_matrix()
        column_sums = np.sum(pairwise_matrix, axis=0)
        normalized_matrix = pairwise_matrix / column_sums
        
        # Calculate the horizontal mean of the pairwise matrix
        horizontal_mean = np.mean(normalized_matrix, axis=1)

        # Multiply the horizontal mean by the weights
        weighted_results = horizontal_mean * weights
        
        # Calculate the sum of the results
        total_weighted_sum = np.sum(weighted_results)
        
        if total_weighted_sum > 2.4:
            return f"High likelihood of sand production. Total Score: {total_weighted_sum:.2f}"
        elif total_weighted_sum > 1.5 and total_weighted_sum <2.4:
            return f"Moderate likelihood of sand production. Total Score: {total_weighted_sum:.2f}"
        else:
            return f"Low likelihood of sand production. Total Score: {total_weighted_sum:.2f}"
########################################################################################
# MY STREAMLIT APP
###########################################################################################

# Initialize session state for page number and user database
# Sidebar with left-aligned titles and buttons
st.sidebar.title("Navigator")
st.sidebar.markdown("<div style='text-align: left;'>", unsafe_allow_html=True)
if st.sidebar.button("WELCOME AND LOGIN PAGE"):
    st.session_state.page = 0
if st.sidebar.button("RESERVOIR DESCRIPTION/ DATA AVAILABILITY PAGE"):
    st.session_state.page = 1
if st.sidebar.button("PAIRWISE COMPARISON PAGE"):  # Update navigation
    st.session_state.page = 2  # Update index for pairwise page
if st.sidebar.button("DATA INPUT PAGE"):
    st.session_state.page = 3  # Update index for data input page
if st.sidebar.button("RESULT AND RECOMMENDATION PAGE"):
    st.session_state.page = 4  # Update index for results page

    # Display the selected page
#pages[st.session_state['page']]()
st.sidebar.markdown("</div>", unsafe_allow_html=True)
def login():
    st.write("### Log In")

    email = st.text_input("Login Email")
    password = st.text_input("Login Password", type="password")
    
    if st.button("Log In"):
        if email in st.session_state['user_db']:
            if  st.session_state['user_db'][email]['password'] == password:
                st.success(f"Welcome back, {st.session_state['user_db'][email]['name']}!")
                #st.session_state.page = 1  # Move to the next page
            else:
                 st.error("Incorrect password. Please try again.")
        else:
            st.warning("User not found. Please sign up.")

# Function to handle signup

# Function to check if all fields are filled
import streamlit as st
import time

# Helper function to check if all fields are filled
def all_inputs_filled(inputs):
    return all(bool(input_value) for input_value in inputs)

# Function to handle the login process
def login():
    st.write("### Log In")

    # Create input fields for login
    email = st.text_input("Login Email")
    password = st.text_input("Login Password", type="password")
    
    if st.button("Log In"):
        if email in st.session_state.get('user_db', {}):
            if st.session_state['user_db'][email]['password'] == password:
                st.success(f"Welcome back, {st.session_state['user_db'][email]['name']}!")
                st.session_state['authenticated'] = True  # Set authentication flag to True
                # Optionally, redirect to another page here after login
                st.session_state.page = 1
            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.warning("User not found. Please sign up.")

# Function to handle the signup process
def signup():
    st.write("### Sign Up")
    
    # Get input from the user
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    company = st.text_input("Company")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    # Combine the inputs into a list
    inputs = [name, phone, email, company, password, confirm_password]
    
    # Check if all fields are filled and passwords match
    form_valid = True
    error_message = ""

    # Check if all fields are filled
    if not all_inputs_filled(inputs):
        form_valid = False
        error_message = "All fields are required for sign up."
    # Check if passwords match
    elif password != confirm_password:
        form_valid = False
        error_message = "Passwords do not match."
    # Check if the email already exists in the user database
    elif email in st.session_state.get('user_db', {}):
        form_valid = False
        error_message = "User already exists. Please log in."
    
    # Show an error message if the form is not valid
    if not form_valid:
        st.error(error_message)
    
    # Only allow the user to submit if the form is valid
    if form_valid:
        submit_button = st.button("Submit")
        
        if submit_button:  # When user clicks "Submit"
            # Initialize user_db if it doesn't exist
            if 'user_db' not in st.session_state:
                st.session_state['user_db'] = {}
            
            # Add the new user to the user_db
            st.session_state['user_db'][email] = {
                "name": name,
                "phone": phone,
                "company": company,
                "password": password,
            }
            st.success("Signup successful! Please log in.")
            
            # Automatically switch to the login form after signup success
            time.sleep(2)  # Wait for a moment to show the success message
            st.session_state['show_auth_dropdown'] = False  # Hide the dropdown after signup and show login form
            st.session_state['show_auth_dropdown'] = True  # Show the login option automatically

# Main function to control user authentication flow
def user_authenticator():
    # Sidebar content with custom HTML for top-right positioning
    with st.sidebar:
        # Create a container for the image and add custom CSS to position it
        st.markdown("<div style='position: relative; text-align: right;'>", unsafe_allow_html=True)

        # Display the login icon as a clickable image
        img_path = "images/icon_for_login.png"  # Ensure this path is correct relative to your project directory
        try:
            # Clicking on the image will toggle the dropdown visibility
            if st.image(img_path, width=40, use_column_width=False):
                # Toggle visibility of the dropdown when the image is clicked
                st.session_state['show_auth_dropdown'] = not st.session_state.get('show_auth_dropdown', False)
        except Exception as e:
            st.error(f"Error loading image: {e}")

        # End the container for the image
        st.markdown("</div>", unsafe_allow_html=True)

        # Show the dropdown menu if the icon is clicked
        if st.session_state.get('show_auth_dropdown', False):
            auth_option = st.selectbox("🔑 User Authentication", ["Sign In", "Log In"], key="auth_dropdown")
            if auth_option == "Sign In":
                signup()  # Show signup form
            elif auth_option == "Log In":
                login()  # Show login form

# Initialize session state for authentication and user database
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'show_auth_dropdown' not in st.session_state:
    st.session_state['show_auth_dropdown'] = False

# Run the authenticator on the main page
if not st.session_state['authenticated']:
    user_authenticator()
else:
    st.write("You are already logged in.")
    # Here you can include any content or pages after successful login



# Main application logic
#def main():
    # Call the user authenticator UI


 #Page 1: Sign Up / Log In
def page_one():
    st.image("images/icon_for_welcome.png", caption="Passport Image", width=250)
    st.title("WELCOME to SPPT")
    st.subheader(" This is a software that predicts sand production")
    
    user_authenticator()
    #st.text('This code was written to develop a sand production prediction tool...')

    #st.sidebar.title("User Authentication")
    #choice = st.sidebar.radio("Choose an option", ["Sign Up", "Log In"])

    #if choice == "Sign Up":
        #signup()
    #elif choice == "Log In":
        #login()
    #if st.button("Next Page"):
        #st.session_state.page += 1

# Page 2: Core and Offset Data Availability
def page_two():
    st.title("RESERVOIR DESCIPTION/ DATA AVAILABILITY PAGE")
    st.title("Reservoir Description Input")

    # Create a 2x2 grid for inputs
    col1, col2 = st.columns(2)

    with col1:
        oml = st.text_input("OML", key=st.session_state.get("oml", ""))
        well_name = st.text_input("Well Name", key=st.session_state.get("well_name", ""))

    with col2:
        reservoir_name = st.text_input("Reservoir Name", key=st.session_state.get("reservoir_name", ""))
        location_map = st.file_uploader("Location Map", type=["png", "jpg", "jpeg"], key=st.session_state.get("location_map"))

    st.write("### Confirm Data Availability")
    # Create checkboxes for sand control criteria
    st.session_state.criteria["core_sample"] = st.checkbox("Core Sample", value=st.session_state.criteria["core_sample"])
    st.session_state.criteria["formation_depth"] = st.checkbox("Formation Depth", value=st.session_state.criteria["formation_depth"])
    st.session_state.criteria["sonic_log"] = st.checkbox("Sonic Log", value=st.session_state.criteria["sonic_log"])
    st.session_state.criteria["porosity_data"] = st.checkbox("Porosity Data", value=st.session_state.criteria["porosity_data"])
    st.session_state.criteria["offset_field_data"] = st.checkbox("Offset Field Data", value=st.session_state.criteria["offset_field_data"])
    
    # Show selected criteria
    st.subheader("Selected Criteria:")
    selected_criteria = [key.replace("_", " ").title() for key, value in st.session_state.criteria.items() if value]

    if selected_criteria:
        st.write(", ".join(selected_criteria))
    else:
        st.write("No criteria selected.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Previous Page"):
            if 'page' in st.session_state:
                st.session_state.page -= 1

    with col2:
        # Check if all inputs are filled before proceeding
        if st.button("Next Page"):
            done = st.radio("Are you done selecting?", options=["Yes", "No"])
            if done == "Yes":
        # Proceed to the next page if the user is done selecting
                st.session_state.page += 1
            elif done == "No":
                st.write("you can continue")
    # Navigation buttons
def pairwise_comparison_page():
    st.title("Pairwise Comparison Matrix Modification")

    modify = st.radio("Would you like to modify the pairwise comparison matrix?", ["Yes", "No"])

    # Default pairwise comparison matrix
    default_matrix = np.array([
        [1,   1/2,   1/3,   1/3, ],
        [2,     1,   1/3,   1/3,],
        [3,   3,   1,   3, ],
        [3,     2,   1/3,   1, ]
       
    ])

    if modify == "Yes":
        st.subheader("Enter your custom values:")
        
        # Create input fields for the matrix
        matrix_input = []
        for i in range(4):
            row_input = []
            for j in range(4):
                value = st.number_input(f"Value for ({i+1}, {j+1})", value=default_matrix[i, j], key=f"input_{i}_{j}")
                row_input.append(value)
            matrix_input.append(row_input)
        
        # Convert input list to a NumPy array
        custom_matrix = np.array(matrix_input)
        st.write("Your custom pairwise comparison matrix:")
        st.write(custom_matrix)

    else:
        st.write("Using the default pairwise comparison matrix:")
        st.write(default_matrix)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page -= 1

    with col2:
        if st.button("Next"):
            st.session_state.page += 1

# Page 3: Input Parameters
def page_three(): 
    st.title("DATA INPUT PAGE")

    # Create columns to arrange inputs in 3 columns    cols = st.columns(3)

    # Input for Interval Transit Time (only show if Sonic Log is selected)
    cols = st.columns(2)
    if st.session_state.criteria.get("sonic_log", False):  # Check if Sonic Log is selected
        st.session_state.par1 = cols[0].number_input('Interval Transit Time', step=1)
    else:
       st.session_state.par1 = None  # Don't show if Sonic Log is not selected


    # Input for Porosity Measurement (only show if Porosity Log is selected)
    if st.session_state.criteria.get("porosity_data", False):  # Check if Porosity Log is selected
        st.session_state.par2 = cols[1].number_input('Porosity Measurement', step=1)
    else:
       st.session_state.par2 = None  # Don't show if Porosity Log is not selected

    # Create another set of columns to arrange further inputs
    cols = st.columns(2)

    # Input for Formation Strength (only show if Core Sample is selected)
    if st.session_state.criteria.get("core_sample", False):  # Check if Core Sample is selected
        st.session_state.par3 = cols[0].number_input('Formation Strength', step=1)
    else:
       st.session_state.par3= None  # Don't show if Core Sample is not selected

    # Input for Reservoir Depth (only show if Formation Depth is selected)
    if st.session_state.criteria.get("formation_depth", False):  # Check if Formation Depth is selected
        st.session_state.par4 = cols[1].number_input('Reservoir Depth', step=1)
    else:
        st.session_state.par4= None  # Don't show if Formation Depth is not selected

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Previous Page"):
            if 'page' in st.session_state:
                st.session_state.page -= 1

    with col2:
        # Check if all inputs are filled before proceeding
        if st.button("Next Page"):
            done = st.radio("Are you done selecting?", options=["Yes", "No"])
            if done == "Yes":
        # Proceed to the next page if the user is done selecting
                st.session_state.page += 1
            elif done == "No":
        # User can continue selecting, no change to page
                st.write("You can continue selecting or modify your inputs.")
    
    # Ensure the page variable is properly initialized
    #if 'page' not in st.session_state:
        #st.session_state.page = 1  # or set it to your desired initial page


def page_four(): 
    import streamlit as st

# Ensure the ProductionEvaluator class is defined elsewhere
    evaluator = ProductionEvaluator()
# Get the weights from the evaluator
    weights = evaluator.assign_weight( 
        par1=st.session_state.get('par1', 0),  # Default to 0 if not set
    par2=st.session_state.get('par2', 0),
    par3=st.session_state.get('par3', 0),
    par4=st.session_state.get('par4', 0),
)

# Traffic light indicators
    parameter_names = [
    'Interval Transit Time',
    'Porosity Measurement',
    'Formation Strength',
    'Reservoir Depth',
]

    color_mapping = {
    5: "red",     # High weight - Red
    3: "orange",  # Medium weight - Orange
    1: "green"    # Low weight - Green
}

    def generate_colored_bars(weights, parameter_names):
        bars_html = ""
        for i, weight in enumerate(weights):
        # Determine the color based on the weight
            color = color_mapping.get(weight, "gray")  # Default to gray if no mapping

        # Length of the bar is proportional to the weight (the bigger the weight, the longer the bar)
            bar_length = weight * 30  # You can adjust the multiplier for the bar length

        # Create the horizontal bar and add the corresponding color
            bar = f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="width: 200px; text-align: right; padding-right: 10px; font-weight: bold;">{parameter_names[i]}</span>
            <div style="height: 20px; width: {bar_length}px; background-color: {color};"></div>
        </div>
        """
            bars_html += bar

        return bars_html

# Display the custom horizontal bar chart
    st.title("Parameter Weights with Custom Colored Bars")
    bars_html = generate_colored_bars(weights, parameter_names)
    st.markdown(bars_html, unsafe_allow_html=True)
    result = evaluator.can_produce_sand(
    par1=st.session_state.get('par1', 0),  # Use session state to get the latest values
    par2=st.session_state.get('par2', 0),
    par3=st.session_state.get('par3', 0),
    par4=st.session_state.get('par4', 0),
    )

    st.write(result)


# Navigation logic
pages = [page_one, page_two, pairwise_comparison_page, page_three, page_four]
def run_pages():
    if st.session_state.page == 0:
        page_one()
    elif st.session_state.page == 1:
        page_two()
    elif st.session_state.page == 2:
        pairwise_comparison_page()
    elif st.session_state.page == 3:
        page_three()
    elif st.session_state.page == 4:
        page_four()



if __name__ == "__main__":
    run_pages()