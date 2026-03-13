import streamlit as st
import fitz
from model import JobRecommendationSystem
from chatbot import CareerChatbot
from resume_scorer import ResumeScorer

# Initialize components
job_recommender = JobRecommendationSystem("JobsFE.csv")
chatbot = CareerChatbot("career_faq.csv")
scorer = ResumeScorer()

# ==================== THEME & STYLING ====================
# Color palette from the new screenshot
TUFTS_BLUE = "#437FC7"
FRENCH_SKY_BLUE = "#6DAFFE"
ALICE_BLUE = "#EDF6FF"
WHITE = "#FFFFFF"
COPPER = "#B9732F"

# Background image URL
BACKGROUND_IMAGE_URL = "https://blog.verifirst.com/hubfs/Blog_Images/Employment%2C%20Hiring%20and%20Background%20Screening%20Trends%20for%202022.jpg"

# Apply custom CSS with background image
st.markdown(f"""
    <style>
    /* Background image with light overlay */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.93), rgba(255, 255, 255, 0.97)),
                    url('{BACKGROUND_IMAGE_URL}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #333333;
    }}
    
    /* Main content container with semi-transparent background */
    .main-container {{
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(109, 175, 254, 0.3);
        box-shadow: 0 8px 32px rgba(67, 127, 199, 0.1);
    }}
    
    /* Headers with blue gradient */
    h1, h2, h3, h4, h5, h6 {{
        color: {TUFTS_BLUE};
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    h1 {{
        font-size: 3rem;
        background: linear-gradient(90deg, {TUFTS_BLUE}, {FRENCH_SKY_BLUE});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }}
    
    /* Buttons with gradient and hover effects */
    .stButton > button {{
        background: linear-gradient(135deg, {TUFTS_BLUE}, {FRENCH_SKY_BLUE});
        color: {WHITE};
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(67, 127, 199, 0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(67, 127, 199, 0.3);
        background: linear-gradient(135deg, {FRENCH_SKY_BLUE}, {TUFTS_BLUE});
    }}
    
    /* Secondary buttons (copper theme) */
    .copper-button > button {{
        background: {WHITE};
        color: {COPPER};
        border: 2px solid {COPPER};
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .copper-button > button:hover {{
        background: {COPPER};
        color: {WHITE};
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(185, 115, 47, 0.3);
    }}
    
    /* File uploader styling */
    .stFileUploader > div > div {{
        background: rgba(237, 246, 255, 0.7);
        border: 2px dashed {FRENCH_SKY_BLUE};
        border-radius: 16px;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader > div > div:hover {{
        border-color: {TUFTS_BLUE};
        background: rgba(237, 246, 255, 0.9);
    }}
    
    /* Text input */
    .stTextInput > div > div > input {{
        background: rgba(255, 255, 255, 0.9);
        color: #333333;
        border: 2px solid {FRENCH_SKY_BLUE};
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {TUFTS_BLUE};
        box-shadow: 0 0 0 3px rgba(67, 127, 199, 0.1);
    }}
    
    /* Cards for job recommendations */
    .job-card {{
        background: linear-gradient(135deg, rgba(237, 246, 255, 0.9), rgba(255, 255, 255, 0.9));
        border: 2px solid {FRENCH_SKY_BLUE};
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        box-shadow: 0 4px 20px rgba(109, 175, 254, 0.1);
    }}
    
    .job-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(109, 175, 254, 0.2);
        border-color: {TUFTS_BLUE};
    }}
    
    /* Score display - modern circular progress */
    .score-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }}
    
    .score-circle {{
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: conic-gradient({TUFTS_BLUE} 0% var(--score-percent), 
                                 rgba(109, 175, 254, 0.2) var(--score-percent) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 8px 25px rgba(67, 127, 199, 0.15);
    }}
    
    .score-inner {{
        width: 160px;
        height: 160px;
        background: {WHITE};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-shadow: inset 0 4px 15px rgba(0, 0, 0, 0.05);
    }}
    
    /* Success messages */
    .stAlert {{
        background: linear-gradient(135deg, rgba(237, 246, 255, 0.9), rgba(255, 255, 255, 0.9));
        border-left: 4px solid {TUFTS_BLUE};
        border-radius: 12px;
        border: 1px solid rgba(109, 175, 254, 0.3);
    }}
    
    /* Warning messages */
    .stWarning {{
        background: rgba(255, 248, 225, 0.9);
        border-left: 4px solid {COPPER};
        border-radius: 12px;
        border: 1px solid rgba(185, 115, 47, 0.3);
    }}
    
    /* Section headers */
    .section-header {{
        background: linear-gradient(90deg, rgba(67, 127, 199, 0.1), rgba(109, 175, 254, 0.1));
        padding: 1.5rem 2rem;
        border-radius: 18px;
        margin: 3rem 0 2rem 0;
        border: 2px solid {FRENCH_SKY_BLUE};
        position: relative;
        overflow: hidden;
    }}
    
    /* Divider */
    .custom-divider {{
        height: 3px;
        background: linear-gradient(90deg, 
            {FRENCH_SKY_BLUE}, 
            {TUFTS_BLUE}, 
            {COPPER}, 
            {FRENCH_SKY_BLUE});
        margin: 3rem 0;
        border-radius: 3px;
        opacity: 0.5;
    }}
    
    /* Chat bubble */
    .chat-bubble {{
        background: linear-gradient(135deg, rgba(237, 246, 255, 0.9), rgba(255, 255, 255, 0.9));
        border-radius: 20px 20px 20px 0;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid {FRENCH_SKY_BLUE};
        box-shadow: 0 4px 15px rgba(109, 175, 254, 0.1);
    }}
    
    /* Sidebar styling */
    .sidebar .sidebar-content {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(109, 175, 254, 0.3);
    }}
    
    /* Metric cards */
    .metric-card {{
        background: linear-gradient(135deg, rgba(237, 246, 255, 0.9), rgba(255, 255, 255, 0.9));
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid {FRENCH_SKY_BLUE};
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(109, 175, 254, 0.1);
    }}
    
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(109, 175, 254, 0.2);
        border-color: {TUFTS_BLUE};
    }}
    
    /* Status indicators */
    .status-indicator {{
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-online {{
        background-color: #4CAF50;
        box-shadow: 0 0 10px #4CAF50;
    }}
    
    .status-offline {{
        background-color: #FF5252;
    }}
    
    /* Navigation tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(237, 246, 255, 0.7);
        border-radius: 12px 12px 0 0;
        padding: 1rem 2rem;
        border: 1px solid rgba(109, 175, 254, 0.3);
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {TUFTS_BLUE};
        color: {WHITE} !important;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(237, 246, 255, 0.5);
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, {FRENCH_SKY_BLUE}, {TUFTS_BLUE});
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, {TUFTS_BLUE}, {COPPER});
    }}
    
    /* Copper accent elements */
    .copper-accent {{
        color: {COPPER};
        font-weight: 600;
    }}
    
    .copper-border {{
        border-color: {COPPER} !important;
    }}
    
    /* Badge styling */
    .badge {{
        background: linear-gradient(135deg, {COPPER}, #D4A056);
        color: {WHITE};
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}
    </style>
""", unsafe_allow_html=True)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com',
        'Report a bug': 'https://www.example.com',
        'About': '# AI Career Assistant v4.0'
    }
)

# ==================== FUNCTIONS ====================
def extract_text(pdf):
    """Extract text from PDF file"""
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def display_score(score):
    """Display resume score in a modern circular progress chart"""
    st.markdown(f"""
        <div class="score-circle" style="--score-percent: {score}%">
            <div class="score-inner">
                <h1 style="color: {TUFTS_BLUE}; margin: 0; font-size: 3.5rem;">{score}</h1>
                <p style="color: #666666; margin: 0; font-size: 1.1rem;">out of 100</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Score interpretation with badges
    if score >= 85:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span class="badge">EXCELLENT</span>
                <p style="color: #2E7D32; margin: 0.5rem 0;">Your resume is highly competitive! 🎯</p>
            </div>
        """, unsafe_allow_html=True)
    elif score >= 70:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span class="badge">STRONG</span>
                <p style="color: {TUFTS_BLUE}; margin: 0.5rem 0;">Great potential with some improvements 💪</p>
            </div>
        """, unsafe_allow_html=True)
    elif score >= 55:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span class="badge">GOOD</span>
                <p style="color: {COPPER}; margin: 0.5rem 0;">Solid foundation, needs optimization 📈</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <span class="badge">NEEDS WORK</span>
                <p style="color: #D32F2F; margin: 0.5rem 0;">Focus on adding key achievements 🛠️</p>
            </div>
        """, unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo and Title
    st.markdown(f"""
        <div style="text-align: center; padding: 2rem 0; margin-bottom: 1rem;">
            <h1 style="color: {TUFTS_BLUE}; margin: 0; font-size: 2.5rem;">💼</h1>
            <h2 style="color: {TUFTS_BLUE}; margin: 0.5rem 0;">AI Career</h2>
            <h3 style="color: {TUFTS_BLUE}; margin: 0;">Assistant</h3>
            <div style="margin: 1rem 0;">
                <span class="status-indicator status-online"></span>
                <span style="color: #666; font-size: 0.9rem;">AI Assistant Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 📋 Navigation")
    nav_option = st.radio(
        "Choose Section",
        ["🏠 Dashboard", "📄 Resume Analysis", "💼 Job Search", "💬 AI Assistant"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Resume Upload in Sidebar
    st.markdown("### 📎 Upload Resume")
    file = st.file_uploader(
        "Choose PDF file",
        type=["pdf"],
        help="Upload your resume for analysis and job matching",
        label_visibility="collapsed"
    )
    
    if file:
        resume_text = extract_text(file)
        st.session_state['resume_text'] = resume_text
        words = len(resume_text.split())
        st.success(f"**✓ {words} words extracted**")
        st.session_state['resume_uploaded'] = True
        
        # Quick action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Score", use_container_width=True):
                st.session_state['check_score'] = True
        with col2:
            if st.button("🔍 Jobs", use_container_width=True):
                st.session_state['find_jobs'] = True
    
    st.markdown("---")
    
    # Stats in Sidebar
    st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {TUFTS_BLUE}; text-align: center; margin: 0 0 1rem 0;">📈 Quick Stats</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="text-align: center;">
                    <h5 style="color: {COPPER}; margin: 0;">1,250+</h5>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Jobs</p>
                </div>
                <div style="text-align: center;">
                    <h5 style="color: {COPPER}; margin: 0;">85%</h5>
                    <p style="color: #666; margin: 0; font-size: 0.9rem;">Match Rate</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Color Palette Display
    st.markdown("### 🎨 Theme Colors")
    colors = [
        (TUFTS_BLUE, "Tufts Blue"),
        (FRENCH_SKY_BLUE, "French Sky Blue"),
        (ALICE_BLUE, "Alice Blue"),
        (WHITE, "White"),
        (COPPER, "Copper")
    ]
    
    for color, name in colors:
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <div style="width: 25px; height: 25px; background-color: {color}; 
                          border-radius: 50%; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                          margin-right: 10px;"></div>
                <span style="color: #666; font-size: 0.9rem;">{name} <code>{color}</code></span>
            </div>
        """, unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 3rem 0;">
        <h1 style="margin-bottom: 1rem;">AI Career Assistant</h1>
        <p style="color: #666; font-size: 1.2rem; max-width: 800px; margin: 0 auto;">
            Your intelligent partner for career growth. 
            Get personalized job recommendations, resume analysis, and career advice.
        </p>
        <div style="margin-top: 2rem;">
            <span class="badge" style="margin: 0 0.5rem;">Smart Matching</span>
            <span class="badge" style="margin: 0 0.5rem;">AI Analysis</span>
            <span class="badge" style="margin: 0 0.5rem;">24/7 Support</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Navigation based on sidebar selection
if nav_option == "🏠 Dashboard":
    st.markdown('<div class="section-header"><h2 style="margin: 0;">📊 Dashboard Overview</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: {TUFTS_BLUE}; margin: 0;">🔍</h3>
                <h4 style="color: {TUFTS_BLUE}; margin: 1rem 0;">Resume Analysis</h4>
                <p style="color: #666;">Get your resume scored and optimized</p>
                <div class="stButton" style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
        if st.button("Analyze Now", key="dashboard_score"):
            st.session_state['check_score'] = True
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: {COPPER}; margin: 0;">💼</h3>
                <h4 style="color: {COPPER}; margin: 1rem 0;">Job Matching</h4>
                <p style="color: #666;">Find jobs that match your profile</p>
                <div class="stButton" style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
        if st.button("Find Jobs", key="dashboard_jobs"):
            st.session_state['find_jobs'] = True
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: {FRENCH_SKY_BLUE}; margin: 0;">💬</h3>
                <h4 style="color: {FRENCH_SKY_BLUE}; margin: 1rem 0;">AI Assistant</h4>
                <p style="color: #666;">Get career advice anytime</p>
                <div class="stButton" style="margin-top: 1rem;">
                """, unsafe_allow_html=True)
        if st.button("Chat Now", key="dashboard_chat"):
            st.session_state['show_chat'] = True

elif nav_option == "📄 Resume Analysis" or ('check_score' in st.session_state and st.session_state['check_score']):
    st.markdown('<div class="section-header"><h2 style="margin: 0;">📊 Resume Analysis Score</h2></div>', unsafe_allow_html=True)
    
    if 'resume_text' in st.session_state:
        with st.spinner("Analyzing your resume..."):
            score = scorer.score_resume(st.session_state['resume_text'])
            st.session_state['resume_score'] = score
            if 'check_score' in st.session_state:
                st.session_state['check_score'] = False
        
        # Display score
        display_score(score)
        
        # Score breakdown in columns
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📈 Detailed Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div style="background: rgba(237, 246, 255, 0.7); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    <h4 style="color: {TUFTS_BLUE}; margin: 0 0 1rem 0;">✅ Strengths</h4>
                    <p style="color: #666; margin: 0.5rem 0;">• Clear structure and formatting</p>
                    <p style="color: #666; margin: 0.5rem 0;">• Relevant technical skills included</p>
                    <p style="color: #666; margin: 0.5rem 0;">• Good use of action verbs</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style="background: rgba(255, 248, 225, 0.7); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border: 2px solid rgba(185, 115, 47, 0.3);">
                    <h4 style="color: {COPPER}; margin: 0 0 1rem 0;">💡 Recommendations</h4>
                    <p style="color: #666; margin: 0.5rem 0;">• Add more quantifiable achievements</p>
                    <p style="color: #666; margin: 0.5rem 0;">• Include specific project results</p>
                    <p style="color: #666; margin: 0.5rem 0;">• Update with latest certifications</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("📁 Please upload a resume first using the sidebar uploader")

elif nav_option == "💼 Job Search" or ('find_jobs' in st.session_state and st.session_state['find_jobs']):
    st.markdown('<div class="section-header"><h2 style="margin: 0;">💼 Personalized Job Recommendations</h2></div>', unsafe_allow_html=True)
    
    if 'resume_text' in st.session_state:
        with st.spinner("Finding the perfect matches for you..."):
            result = job_recommender.recommend_jobs(st.session_state['resume_text'])
            jobs = result["recommended_jobs"][:5]
            st.session_state['recommended_jobs'] = jobs
            if 'find_jobs' in st.session_state:
                st.session_state['find_jobs'] = False
        
        st.markdown(f"### 🎯 Top {len(jobs)} Matches for Your Profile")
        
        for i, job in enumerate(jobs, 1):
            match_score = 95 - (i * 5)
            
            st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h3 style="color: {TUFTS_BLUE}; margin: 0 0 1rem 0;">{job['position']}</h3>
                            <p style="color: #666; margin: 0.5rem 0;">
                                <strong style="color: {COPPER};">🏢 Company:</strong> {job['workplace']}
                            </p>
                            <p style="color: #666; margin: 0.5rem 0;">
                                <strong style="color: {COPPER};">🌍 Mode:</strong> {job['working_mode']}
                            </p>
                            <p style="color: #666; margin: 0.5rem 0;">
                                <strong style="color: {COPPER};">🛠️ Skills:</strong> {job['requisite_skill']}
                            </p>
                        </div>
                        <div style="text-align: center; min-width: 120px;">
                            <div style="background: linear-gradient(135deg, {TUFTS_BLUE}, {FRENCH_SKY_BLUE}); 
                                      padding: 0.75rem; border-radius: 16px; color: white; 
                                      font-weight: bold; font-size: 1.3rem; margin-bottom: 0.5rem;">
                                {match_score}%
                            </div>
                            <span style="color: #666; font-size: 0.9rem;">Match Score</span>
                            <div style="margin-top: 1rem;">
                                <span class="stButton">
                            """, unsafe_allow_html=True)
            if st.button(f"Apply #{i}", key=f"apply_{i}"):
                st.success(f"Application initiated for {job['position']}!")
            st.markdown("</div></div></div>", unsafe_allow_html=True)
    else:
        st.warning("📁 Please upload a resume first to get job recommendations")

elif nav_option == "💬 AI Assistant" or ('show_chat' in st.session_state and st.session_state['show_chat']):
    st.markdown('<div class="section-header"><h2 style="margin: 0;">💬 AI Career Assistant</h2></div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        question = st.text_input(
            "",
            placeholder="Ask about careers, interviews, salary negotiation, or resume tips...",
            key="chat_input"
        )
    with col2:
        if st.button("🚀 Send", use_container_width=True, type="primary"):
            if question:
                with st.spinner("Thinking..."):
                    answer = chatbot.ask(question)
                    st.session_state['chat_history'] = st.session_state.get('chat_history', []) + [
                        {"question": question, "answer": answer}
                    ]
            else:
                st.warning("Please enter a question")
    
    # Display chat history
    if 'chat_history' in st.session_state:
        for chat in st.session_state['chat_history'][-5:]:  # Show last 5 conversations
            st.markdown(f"""
                <div class="chat-bubble">
                    <p style="color: {TUFTS_BLUE}; margin: 0 0 0.5rem 0; font-weight: 600;">
                        👤 You: {chat['question']}
                    </p>
                    <p style="color: #666; margin: 0; padding-left: 1rem; border-left: 3px solid {FRENCH_SKY_BLUE};">
                        🤖 AI: {chat['answer']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    # Quick questions
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 💡 Quick Questions")
    
    quick_cols = st.columns(4)
    questions = [
        ("Best resume format?", "format"),
        ("Interview tips?", "interview"),
        ("Salary negotiation?", "salary"),
        ("Career growth?", "growth")
    ]
    
    for idx, (q_text, q_key) in enumerate(questions):
        with quick_cols[idx]:
            if st.button(f"❓ {q_text}", key=f"quick_{q_key}"):
                answer = chatbot.ask(q_text)
                st.session_state['chat_history'] = st.session_state.get('chat_history', []) + [
                    {"question": q_text, "answer": answer}
                ]
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

# ==================== FOOTER ====================
st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 3rem 0 1rem 0; margin-top: 2rem; border-top: 2px solid rgba(109, 175, 254, 0.3);">
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem; flex-wrap: wrap;">
            <span style="color: {TUFTS_BLUE}; font-weight: 600;">Tufts Blue #437FC7</span>
            <span style="color: {FRENCH_SKY_BLUE}; font-weight: 600;">French Sky Blue #6DAFFE</span>
            <span style="color: {COPPER}; font-weight: 600;">Copper #B9732F</span>
        </div>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">
            AI Career Assistant v4.0 • Professional Edition • Made with ❤️ for Career Growth
        </p>
        <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">
            © 2024 CareerAI Solutions • Empowering Professionals Worldwide
        </p>
    </div>
""", unsafe_allow_html=True)