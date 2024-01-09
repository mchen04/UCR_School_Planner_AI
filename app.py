import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo

# Read the API key from keys.txt and set it as an environment variable
with open('keys.txt', 'r') as file:
    api_key = file.read().strip()
os.environ['OPENAI_API_KEY'] = api_key

# Initialize the language model with specified temperature
llm = OpenAI(temperature=0.9)

# Streamlit interface setup
st.set_page_config(layout="wide", page_title="UCR Academic Planner")

# Schools, majors, and their respective specializations
schools_majors = {
    "Marlan and Rosemary Bourns College of Engineering": {
        "Bioengineering": [],
        "Chemical Engineering": [],
        "Computer Engineering": [],
        "Computer Science": [],
        "Computer Science and Business Applications": [],
        "Data Science": [],
        "Electrical Engineering": [],
        "Environmental Engineering": [],
        "Materials Science and Engineering": [],
        "Mechanical Engineering": [],
        "Robotics Engineering": []
    },
    "College of Humanities, Arts, and Social Sciences": {
        "African American Studies": [],
        "Anthropology": [],
        "Art (Studio)": [],
        "Art History": ["Administrative Studies", "Religious Studies"],
        "Asian American Studies": [],
        "Asian Studies": [],
        "Business Economics": [],
        "Chicano Studies": [],
        "Creative Writing": [],
        "Dance": [],
        "Economics": ["Administrative Studies"],
        "English": [],
        "Ethnic Studies": [],
        "Gender and Sexuality Studies": [],
        "Global Studies": [],
        "History": ["Administrative Studies"],
        "Languages and Literatures": ["Chinese", "Classical Studies", "Comparative Ancient Civilizations", "Comparative Literature", "French", "Germanic Studies", "Japanese", "Russian Studies"],
        "Latin American Studies": [],
        "Liberal Studies": [],
        "Linguistics": [],
        "Media and Cultural Studies": [],
        "Middle East and Islamic Studies": [],
        "Music": ["Music and Culture"],
        "Native American Studies": [],
        "Neuroscience": [],
        "Philosophy": [],
        "Political Science": ["Administrative Studies", "International Affairs", "Public Service"],
        "Psychology": [],
        "Religious Studies": [],
        "Sociology": ["Administrative Studies"],
        "Spanish": [],
        "Sustainability Studies": [],
        "Theatre, Film and Digital Production": []
    },
    "College of Natural and Agricultural Sciences": {
        "Biochemistry": [],
        "Biology": [],
        "Cell, Molecular, and Developmental Biology": [],
        "Chemistry": [],
        "Data Science": [],
        "Earth Sciences": [],
        "Entomology": [],
        "Environmental Sciences": [],
        "Geology": [],
        "Geophysics": [],
        "Mathematics": ["Mathematics for Secondary School Teachers"],
        "Microbiology": [],
        "Neuroscience": [],
        "Physics": [],
        "Plant Biology": [],
        "Statistics": []
    },
    "School of Education": {
        "Education, Society, and Human Development": ["Community Leadership, Policy, and Social Justice", "Learning and Behavioral Studies", "Student-Designed Comparative Concentration"]
    },
    "School of Business": {
        "Actuarial Science": [],
        "Business Administration": ["Accounting and Auditing", "Business Analytics", "Finance", "Information Systems", "Management", "Marketing", "Operations and Supply Chain Management"]
    },
    "School of Public Policy": {
        "Public Policy": ["Economic Policy", "Health/Population Policy", "International/Foreign Policy", "Policy Institutions and Processes", "Social/Cultural/Family Policy", "Urban/Environmental Policy"]
    },
    # Additional Minors and Specializations
    "Additional Minors and Specializations": {
        "Applied Statistics": [],
        "Global Climate Change": [],
        "International Relations": [],
        "Journalism": [],
        "Labor Studies": [],
        "Languages and Literatures": ["Arabic", "Italian", "Korean", "Southeast Asian"],
        "Law and Society": [],
        "Lesbian, Gay, Bisexual, Intersex, and Transgender Studies": [],
        "Marxist Studies": [],
        "Peace and Conflict": [],
        "Science Fiction and Technoculture Studies": [],
        "Southeast Asian Studies": [],
        "Urban Studies": [],
        "Western American Studies": []
    }
}

# Initialize session state for storing conversation and controlling the reset of the text input
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'reset_text_input' not in st.session_state:
    st.session_state['reset_text_input'] = False

# Sidebar for user inputs
with st.sidebar:
    st.header("Student Profile")
    st.subheader("Enter your details")
    name = st.text_input("Name")
    # School selection
    school = st.selectbox("School", list(schools_majors.keys()))
    # Update majors based on selected school
    majors = schools_majors[school]
    major = st.selectbox("Major", list(majors.keys()))
    # Specializations for the selected major
    specializations = majors[major]
    specialization = st.selectbox("Specialization", specializations) if specializations else None
    # Academic Year and Quarter Selection
    academic_year = st.slider("Academic Year", 1, 4, 1)
    current_quarter = st.selectbox("Current Quarter", ["Fall", "Winter", "Spring"])
    # File uploader
    upload_transcript = st.file_uploader("Upload Transcript", type=["pdf"])

# Main content area
st.title("UCR Academic Planner")
st.markdown("## Plan Your Academic Journey")

# Responsive columns for content
col1, col2 = st.columns([1, 1])  # This will create two columns of equal width

# User input area in the second column
with col1:
    # Using a container for better control over the layout
    with st.container():
        # Text input for user message
        user_message = st.text_input("Ask the AI", key=f"user_message_{st.session_state['reset_text_input']}")

        # Button to send the message
        if st.button("Send"):
            if user_message:
                # Add user message to conversation
                st.session_state['conversation'].append("You: " + user_message)

                # Generate AI response
                #response = agent_executor.run(user_message)
                response = "Response from AI"

                # Add AI response to conversation
                st.session_state['conversation'].append("AI: " + response)

                # Toggle the reset state to clear the text input box
                st.session_state['reset_text_input'] = not st.session_state['reset_text_input']

# AI conversation area in the first column
with col2:
    st.subheader("Conversation with AI")
    with st.expander("See conversation", expanded=True):
        for message in st.session_state['conversation']:
            st.text(message)
                
st.write("") 
st.write("") 
                
# Feedback and Support
st.subheader("Feedback")
feedback = st.text_area("Any suggestions for us?")
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")