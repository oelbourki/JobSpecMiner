"""Main Streamlit application for JobSpecMiner Web App."""
import streamlit as st
from datetime import datetime

from src.job_extractor import JobExtractor
from src.file_generator import generate_txt_file, generate_json_file
from utils.validators import validate_api_key, validate_job_description

# Page configuration
st.set_page_config(
    page_title="JobSpecMiner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sample job description for demo
SAMPLE_JOB_DESCRIPTION = """We are looking for a Senior Software Engineer to join our growing team.

About the Role:
You will be responsible for designing, developing, and maintaining scalable software solutions. You'll work closely with cross-functional teams to deliver high-quality products.

Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python, JavaScript, and cloud technologies
- Experience with microservices architecture
- Bachelor's degree in Computer Science or related field
- Excellent problem-solving and communication skills

Preferred Qualifications:
- Master's degree in Computer Science
- Experience with AWS or Google Cloud Platform
- Knowledge of machine learning frameworks
- Previous experience in a startup environment

Benefits:
- Competitive salary: $120,000 - $150,000
- Remote work options
- Health, dental, and vision insurance
- 401(k) matching
- Flexible PTO
- Professional development budget

Location: Remote (US-based preferred)
Work Type: Remote/Hybrid"""

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'extraction_result' not in st.session_state:
    st.session_state.extraction_result = None
if 'extraction_error' not in st.session_state:
    st.session_state.extraction_error = None
if 'job_description_text' not in st.session_state:
    st.session_state.job_description_text = ""
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = {}

# Header
st.title("🔍 JobSpecMiner")
st.markdown("### Extract structured information from job descriptions using AI")
st.markdown("---")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input")
    
    # API Key Input
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        help="Your API key is stored locally in this session and never sent to our servers. Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    # Store API key in session state
    if api_key:
        st.session_state.api_key = api_key
    
    st.markdown("---")
    
    # Job Description Input with Clear button
    input_col1, input_col2 = st.columns([3, 1])
    
    with input_col1:
        job_description = st.text_area(
            "Job Description",
            height=400,
            value=st.session_state.job_description_text,
            placeholder="Paste the job description here...\n\nExample:\nWe are looking for a Senior Software Engineer with 5+ years of experience...",
            help="Paste the complete job description text. Minimum 50 characters required.",
            key="job_desc_input"
        )
    
    with input_col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🗑️ Clear", use_container_width=True, help="Clear the job description"):
            st.session_state.job_description_text = ""
            st.rerun()
        
        if st.button("📋 Sample", use_container_width=True, help="Load a sample job description"):
            st.session_state.job_description_text = SAMPLE_JOB_DESCRIPTION
            st.rerun()
    
    # Update session state
    st.session_state.job_description_text = job_description
    
    # Character and word counter
    if job_description:
        char_count = len(job_description)
        word_count = len(job_description.split())
        st.caption(f"📊 {char_count} characters | {word_count} words")
    
    st.markdown("---")
    
    # Extract Button
    extract_button = st.button(
        "🔍 Extract Information",
        type="primary",
        use_container_width=True
    )

with col2:
    st.header("📊 Results")
    
    # Show extraction status
    if st.session_state.extraction_error:
        st.error(f"❌ {st.session_state.extraction_error}")
        
        # Retry button
        if st.button("🔄 Retry Extraction", use_container_width=True):
            st.session_state.extraction_error = None
            st.rerun()
    
    # Process extraction when button is clicked
    if extract_button:
        # Validation
        if not validate_api_key(api_key):
            st.error("⚠️ Please enter a valid Gemini API key")
            st.stop()
        elif not validate_job_description(job_description):
            st.error("⚠️ Please enter a job description (minimum 50 characters)")
            st.stop()
        else:
            # Process extraction
            with st.spinner("🔄 Extracting information from job description..."):
                try:
                    extractor = JobExtractor(api_key=api_key)
                    result = extractor.extract_information(job_description)
                    
                    if result:
                        st.session_state.extraction_result = result
                        st.session_state.extraction_error = None
                        st.success("✅ Extraction complete!")
                        st.balloons()  # Celebration animation
                    else:
                        st.session_state.extraction_result = None
                        st.session_state.extraction_error = "Extraction failed. Please check your API key and try again."
                        st.error("❌ Extraction failed. Please check your API key and try again.")
                except Exception as e:
                    st.session_state.extraction_result = None
                    st.session_state.extraction_error = f"Error: {str(e)}"
                    st.error(f"❌ Error: {str(e)}")
    
    # Display Results
    if st.session_state.extraction_result:
        result = st.session_state.extraction_result
        
        # Summary Stats Card
        st.markdown("### 📈 Summary")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Skills", len(result.skills) if result.skills else 0)
        with stats_col2:
            st.metric("Requirements", len(result.required_criteria) if result.required_criteria else 0)
        with stats_col3:
            st.metric("Responsibilities", len(result.scope_of_responsibilities) if result.scope_of_responsibilities else 0)
        with stats_col4:
            st.metric("Benefits", len(result.benefits) if result.benefits else 0)
        
        st.markdown("---")
        
        # Expand/Collapse All Controls
        control_col1, control_col2 = st.columns([1, 1])
        with control_col1:
            expand_all = st.button("📖 Expand All", use_container_width=True)
        with control_col2:
            collapse_all = st.button("📕 Collapse All", use_container_width=True)
        
        if expand_all:
            st.session_state.expanded_sections = {key: True for key in range(10)}
        if collapse_all:
            st.session_state.expanded_sections = {key: False for key in range(10)}
        
        # Basic Information
        with st.expander("📋 Basic Information", expanded=st.session_state.expanded_sections.get(0, True)):
            info_text = f"Job Title: {result.job_title}\n"
            if result.company_name:
                info_text += f"Company: {result.company_name}\n"
            if result.department:
                info_text += f"Department: {result.department}\n"
            if result.seniority_level:
                info_text += f"Seniority Level: {result.seniority_level}\n"
            if result.years_of_experience:
                info_text += f"Years of Experience: {result.years_of_experience}"
            
            st.write(f"**Job Title:** {result.job_title}")
            if result.company_name:
                st.write(f"**Company:** {result.company_name}")
            if result.department:
                st.write(f"**Department:** {result.department}")
            if result.seniority_level:
                st.write(f"**Seniority Level:** {result.seniority_level}")
            if result.years_of_experience:
                st.write(f"**Years of Experience:** {result.years_of_experience}")
            
            # Copy button - show text in code block for easy selection
            if st.button("📋 Show to Copy", key="copy_basic", use_container_width=True):
                st.code(info_text, language=None)
                st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Work Arrangement
        if result.work_type or result.location:
            with st.expander("📍 Work Arrangement", expanded=st.session_state.expanded_sections.get(1, False)):
                work_text = ""
                if result.work_type:
                    st.write(f"**Work Type:** {result.work_type}")
                    work_text += f"Work Type: {result.work_type}\n"
                if result.location:
                    st.write(f"**Location:** {result.location}")
                    work_text += f"Location: {result.location}"
                
                if st.button("📋 Show to Copy", key="copy_work", use_container_width=True):
                    st.code(work_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Compensation
        if result.salary:
            with st.expander("💰 Compensation", expanded=st.session_state.expanded_sections.get(2, False)):
                st.write(f"**Salary:** {result.salary}")
                if st.button("📋 Copy", key="copy_salary", use_container_width=True):
                    try:
                        pyperclip.copy(f"Salary: {result.salary}")
                        st.success("Copied to clipboard!")
                    except:
                        st.info("Copy functionality requires pyperclip. Install with: pip install pyperclip")
        
        # Education
        if result.education_requirements:
            with st.expander("🎓 Education Requirements", expanded=st.session_state.expanded_sections.get(3, False)):
                st.write(result.education_requirements)
                if st.button("📋 Show to Copy", key="copy_education", use_container_width=True):
                    st.code(result.education_requirements, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Required Criteria
        if result.required_criteria:
            with st.expander("✅ Required Criteria", expanded=st.session_state.expanded_sections.get(4, False)):
                criteria_text = "\n".join([f"{i}. {criterion}" for i, criterion in enumerate(result.required_criteria, 1)])
                for i, criterion in enumerate(result.required_criteria, 1):
                    st.write(f"{i}. {criterion}")
                
                if st.button("📋 Show to Copy", key="copy_criteria", use_container_width=True):
                    st.code(criteria_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Preferred Qualifications
        if result.preferred_qualifications:
            with st.expander("⭐ Preferred Qualifications", expanded=st.session_state.expanded_sections.get(5, False)):
                pref_text = "\n".join([f"{i}. {qual}" for i, qual in enumerate(result.preferred_qualifications, 1)])
                for i, qual in enumerate(result.preferred_qualifications, 1):
                    st.write(f"{i}. {qual}")
                
                if st.button("📋 Show to Copy", key="copy_pref", use_container_width=True):
                    st.code(pref_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Skills
        if result.skills:
            with st.expander("🛠️ Skills & Technologies", expanded=st.session_state.expanded_sections.get(6, False)):
                skills_text = "\n".join([f"{i}. {skill}" for i, skill in enumerate(result.skills, 1)])
                for i, skill in enumerate(result.skills, 1):
                    st.write(f"{i}. {skill}")
                
                if st.button("📋 Show to Copy", key="copy_skills", use_container_width=True):
                    st.code(skills_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Responsibilities
        if result.scope_of_responsibilities:
            with st.expander("📋 Scope of Responsibilities", expanded=st.session_state.expanded_sections.get(7, False)):
                resp_text = "\n".join([f"{i}. {responsibility}" for i, responsibility in enumerate(result.scope_of_responsibilities, 1)])
                for i, responsibility in enumerate(result.scope_of_responsibilities, 1):
                    st.write(f"{i}. {responsibility}")
                
                if st.button("📋 Show to Copy", key="copy_resp", use_container_width=True):
                    st.code(resp_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Benefits
        if result.benefits:
            with st.expander("🎁 Benefits & Perks", expanded=st.session_state.expanded_sections.get(8, False)):
                benefits_text = "\n".join([f"{i}. {benefit}" for i, benefit in enumerate(result.benefits, 1)])
                for i, benefit in enumerate(result.benefits, 1):
                    st.write(f"{i}. {benefit}")
                
                if st.button("📋 Show to Copy", key="copy_benefits", use_container_width=True):
                    st.code(benefits_text, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        # Additional Information
        if result.additional_info:
            with st.expander("ℹ️ Additional Information", expanded=st.session_state.expanded_sections.get(9, False)):
                st.write(result.additional_info)
                if st.button("📋 Show to Copy", key="copy_additional", use_container_width=True):
                    st.code(result.additional_info, language=None)
                    st.success("Select the text above and copy (Ctrl+C / Cmd+C)")
        
        st.markdown("---")
        
        # Download Section
        st.subheader("📥 Download Results")
        
        download_col1, download_col2 = st.columns(2)
        
        with download_col1:
            try:
                txt_content = generate_txt_file(result)
                st.download_button(
                    label="📄 Download as TXT",
                    data=txt_content,
                    file_name=f"job_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating TXT file: {e}")
        
        with download_col2:
            try:
                json_content = generate_json_file(result)
                st.download_button(
                    label="📦 Download as JSON",
                    data=json_content,
                    file_name=f"job_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating JSON file: {e}")
    else:
        st.info("👆 Enter your API key and job description, then click 'Extract Information' to get started.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>JobSpecMiner - Powered by Google Gemini AI</p>
        <p>Your API key is stored locally in your session and never sent to our servers.</p>
    </div>
    """,
    unsafe_allow_html=True
)
