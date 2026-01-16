# JobSpecMiner Streamlit Web App - Implementation Plan

**Project:** JobSpecMiner Web Application  
**Platform:** Netlify (with stlite) / Alternative: Streamlit Community Cloud  
**Date:** December 2024

---

## Executive Summary

This plan outlines the development of a web-based interface for JobSpecMiner using Streamlit. The app will allow users to:
- Input their Gemini API key
- Paste job descriptions
- Extract structured information
- Download results as TXT and JSON files

**Important Note:** Netlify doesn't natively support Streamlit servers. This plan includes two deployment strategies:
1. **Primary:** Use stlite (browser-based Streamlit) for Netlify deployment
2. **Alternative:** Deploy to Streamlit Community Cloud (recommended for full features)

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Implementation Phases](#4-implementation-phases)
5. [UI/UX Design](#5-uiux-design)
6. [Security Considerations](#6-security-considerations)
7. [Deployment Strategy](#7-deployment-strategy)
8. [Testing Strategy](#8-testing-strategy)
9. [File Structure](#9-file-structure)
10. [Implementation Checklist](#10-implementation-checklist)

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Streamlit Web Interface                 │   │
│  │  - API Key Input (Session State)               │   │
│  │  - Job Description Text Area                   │   │
│  │  - Extract Button                              │   │
│  │  - Results Display                             │   │
│  │  - Download Buttons (TXT & JSON)               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              JobExtractor Service                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │  - JobExtractor Class (from existing code)       │   │
│  │  - Gemini API Client                             │   │
│  │  - Data Validation (Pydantic)                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Google Gemini API                           │
│  - Structured Output Generation                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

1. **Input:** User enters API key → stored in Streamlit session state
2. **Input:** User pastes job description → stored temporarily
3. **Processing:** Click "Extract" → JobExtractor processes text → Gemini API call
4. **Output:** Results displayed in UI
5. **Download:** User clicks download → Files generated and served

### 1.3 Key Components

- **Streamlit App (`app.py`):** Main application entry point
- **JobExtractor Integration:** Reuse existing extraction logic
- **File Generation:** Create TXT and JSON files on-the-fly
- **Download Handler:** Streamlit download buttons for file retrieval

---

## 2. Technology Stack

### 2.1 Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | Streamlit | 1.28+ | UI framework |
| **AI/ML** | google-genai | 0.2.0+ | Gemini API client |
| **Data Validation** | Pydantic | 2.0+ | Data models |
| **Deployment** | stlite / Streamlit Cloud | Latest | Hosting platform |

### 2.2 Additional Dependencies

```txt
streamlit>=1.28.0
google-genai>=0.2.0
pydantic>=2.0.0
```

### 2.3 Deployment Options

**Option A: Netlify with stlite (Browser-based)**
- ✅ Works on Netlify (static hosting)
- ✅ No server required
- ⚠️ Limited to browser capabilities
- ⚠️ API calls from client-side (CORS considerations)

**Option B: Streamlit Community Cloud (Recommended)**
- ✅ Full Streamlit features
- ✅ Free hosting
- ✅ Easy deployment
- ✅ Server-side processing
- ✅ Better security (API key not exposed)

**Option C: Alternative Platforms**
- Render.com
- Heroku
- Railway
- Fly.io

---

## 3. Project Structure

### 3.1 Directory Layout

```
JobSpecMiner-WebApp/
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── models.py              # Pydantic models (reuse from existing)
│   ├── job_extractor.py       # JobExtractor class (reuse from existing)
│   └── file_generator.py       # File generation utilities
├── utils/
│   ├── __init__.py
│   └── validators.py          # Input validation helpers
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── README.md                   # Project documentation
├── .gitignore
└── netlify.toml               # Netlify configuration (if using stlite)
```

### 3.2 File Responsibilities

**app.py:**
- Streamlit UI components
- Session state management
- User input handling
- Results display
- Download functionality

**src/job_extractor.py:**
- Reuse existing JobExtractor class
- Minor modifications for web context

**src/file_generator.py:**
- Generate TXT file (reuse format_output logic)
- Generate JSON file (from JobInformation model)
- Create downloadable file objects

**utils/validators.py:**
- API key format validation
- Job description validation
- Input sanitization

---

## 4. Implementation Phases

### Phase 1: Setup & Foundation (Day 1)

**Tasks:**
1. ✅ Create new project directory structure
2. ✅ Copy existing models.py and job_extractor.py
3. ✅ Create requirements.txt with Streamlit
4. ✅ Set up Streamlit configuration
5. ✅ Create basic app.py skeleton

**Deliverables:**
- Project structure created
- Dependencies installed
- Basic Streamlit app runs locally

### Phase 2: Core UI Development (Day 2)

**Tasks:**
1. ✅ Design and implement input section
   - API key input (password field)
   - Job description text area
   - Extract button
2. ✅ Implement session state management
3. ✅ Add loading indicators
4. ✅ Create results display section
5. ✅ Add error handling UI

**Deliverables:**
- Complete UI layout
- Input handling functional
- Session state working

### Phase 3: Integration & Processing (Day 3)

**Tasks:**
1. ✅ Integrate JobExtractor class
2. ✅ Connect UI to extraction logic
3. ✅ Implement error handling
4. ✅ Add progress indicators
5. ✅ Test API integration

**Deliverables:**
- End-to-end extraction working
- Error messages displayed
- Results shown in UI

### Phase 4: File Generation & Download (Day 4)

**Tasks:**
1. ✅ Create file_generator.py
2. ✅ Implement TXT file generation
3. ✅ Implement JSON file generation
4. ✅ Add Streamlit download buttons
5. ✅ Test file downloads

**Deliverables:**
- TXT download functional
- JSON download functional
- Files properly formatted

### Phase 5: Polish & Enhancement (Day 5)

**Tasks:**
1. ✅ Improve UI/UX
2. ✅ Add input validation
3. ✅ Add success/error messages
4. ✅ Optimize performance
5. ✅ Add help/documentation

**Deliverables:**
- Polished user interface
- Input validation working
- User-friendly error messages

### Phase 6: Deployment (Day 6)

**Tasks:**
1. ✅ Choose deployment platform
2. ✅ Configure deployment files
3. ✅ Set up environment variables (if needed)
4. ✅ Deploy application
5. ✅ Test deployed version

**Deliverables:**
- Application deployed
- Accessible via URL
- All features working in production

---

## 5. UI/UX Design

### 5.1 Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  JobSpecMiner - Job Description Extractor              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [API Configuration Section]                            │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Gemini API Key: [________________]               │  │
│  │ ℹ️ Your API key is stored locally and never     │  │
│  │    sent to our servers                           │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Job Description Input]                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Paste your job description here...              │  │
│  │                                                 │  │
│  │ [Large text area]                               │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Extract Button]                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │          [🔍 Extract Information]              │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Results Section] (shown after extraction)            │
│  ┌─────────────────────────────────────────────────┐  │
│  │ ✅ Extraction Complete!                        │  │
│  │                                                 │  │
│  │ [Results Preview]                              │  │
│  │                                                 │  │
│  │ [📥 Download as TXT]  [📥 Download as JSON]    │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.2 UI Components

**1. Header Section**
- Title: "JobSpecMiner"
- Subtitle: "Extract structured information from job descriptions"
- Optional: Logo/branding

**2. API Key Input**
- Type: Password input (hidden characters)
- Placeholder: "Enter your Gemini API key"
- Info: Explanation about API key security
- Validation: Format check (optional)

**3. Job Description Input**
- Type: Text area (large, resizable)
- Placeholder: "Paste job description here..."
- Character counter: Show character count
- Clear button: Reset input

**4. Extract Button**
- Prominent, centered
- Loading state: Show spinner during processing
- Disabled state: When inputs are invalid

**5. Results Display**
- Expandable sections for each data category
- Clean, readable format
- Copy-to-clipboard option (optional)

**6. Download Buttons**
- Two buttons: TXT and JSON
- Icon indicators
- File size display (optional)

### 5.3 User Experience Features

- **Loading States:** Spinner during API calls
- **Error Messages:** Clear, actionable error messages
- **Success Feedback:** Confirmation when extraction completes
- **Input Validation:** Real-time validation feedback
- **Session Persistence:** Remember API key during session
- **Responsive Design:** Works on mobile/tablet

---

## 6. Security Considerations

### 6.1 API Key Security

**Client-Side Storage (stlite/Netlify):**
- ⚠️ API key stored in browser session
- ⚠️ Visible in browser DevTools
- ✅ Not sent to our servers
- ✅ Cleared when session ends
- ⚠️ **Risk:** User's API key exposed in browser

**Server-Side Storage (Streamlit Cloud):**
- ✅ API key stored in session state (server-side)
- ✅ Not exposed to client
- ✅ More secure option
- ✅ Can use environment variables for default key

### 6.2 Recommendations

1. **Clear Warnings:** Inform users that API key is stored locally
2. **No Persistence:** Don't save API key to disk/cookies
3. **HTTPS Only:** Ensure deployment uses HTTPS
4. **Input Sanitization:** Validate and sanitize all inputs
5. **Rate Limiting:** Consider client-side rate limiting
6. **Error Handling:** Don't expose sensitive info in errors

### 6.3 Best Practices

- Use password input type for API key
- Clear session state on logout/close
- Validate API key format before use
- Handle API errors gracefully
- Don't log API keys

---

## 7. Deployment Strategy

### 7.1 Option A: Netlify with stlite

**What is stlite?**
- Streamlit compiled to WebAssembly
- Runs entirely in the browser
- No server required
- Can be deployed as static site

**Implementation Steps:**

1. **Build stlite App:**
   ```bash
   # Install stlite
   pip install stlite
   
   # Build static files
   stlite build app.py --outdir dist
   ```

2. **Netlify Configuration (`netlify.toml`):**
   ```toml
   [build]
     publish = "dist"
     command = "stlite build app.py --outdir dist"
   
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

3. **Deploy:**
   - Connect GitHub repo to Netlify
   - Set build command
   - Deploy

**Limitations:**
- API calls from browser (CORS issues possible)
- Larger bundle size
- Some Streamlit features may not work

### 7.2 Option B: Streamlit Community Cloud (Recommended)

**Why Recommended:**
- ✅ Full Streamlit features
- ✅ Server-side processing
- ✅ Better security
- ✅ Free hosting
- ✅ Easy deployment

**Implementation Steps:**

1. **Prepare Repository:**
   - Push code to GitHub
   - Ensure `requirements.txt` is present
   - Create `app.py` as entry point

2. **Deploy to Streamlit Cloud:**
   - Go to share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository and branch
   - Set main file: `app.py`
   - Deploy

3. **Configuration:**
   - No special config needed
   - Environment variables can be set in dashboard

**Advantages:**
- Zero configuration
- Automatic deployments on git push
- Built-in analytics
- Custom domain support

### 7.3 Option C: Alternative Platforms

**Render.com:**
- Free tier available
- Easy deployment
- Automatic SSL
- Environment variables support

**Railway:**
- Simple deployment
- Good for Python apps
- Free tier with limits

---

## 8. Testing Strategy

### 8.1 Unit Tests

**Test Files:**
- `tests/test_job_extractor.py` - Test extraction logic
- `tests/test_file_generator.py` - Test file generation
- `tests/test_validators.py` - Test input validation

**Test Cases:**
- API key validation
- Job description processing
- File generation (TXT and JSON)
- Error handling

### 8.2 Integration Tests

- End-to-end extraction flow
- File download functionality
- Error scenarios
- API integration (with mock)

### 8.3 Manual Testing Checklist

- [ ] API key input and storage
- [ ] Job description input
- [ ] Extraction process
- [ ] Results display
- [ ] TXT file download
- [ ] JSON file download
- [ ] Error handling
- [ ] Empty input handling
- [ ] Invalid API key handling
- [ ] Network error handling

---

## 9. File Structure

### 9.1 Complete File Structure

```
JobSpecMiner-WebApp/
│
├── app.py                          # Main Streamlit application
│
├── src/
│   ├── __init__.py
│   ├── models.py                   # Pydantic models (from existing)
│   ├── job_extractor.py            # JobExtractor class (from existing)
│   └── file_generator.py           # NEW: File generation utilities
│
├── utils/
│   ├── __init__.py
│   └── validators.py               # NEW: Input validation
│
├── tests/                          # NEW: Test suite
│   ├── __init__.py
│   ├── test_job_extractor.py
│   ├── test_file_generator.py
│   └── test_validators.py
│
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
│
├── requirements.txt                # Dependencies
├── README.md                       # Documentation
├── .gitignore
├── netlify.toml                    # Netlify config (if using stlite)
└── Procfile                        # For Heroku/Render (if needed)
```

### 9.2 Key Files Content

#### app.py (Main Application)

```python
import streamlit as st
from src.job_extractor import JobExtractor
from src.file_generator import generate_txt_file, generate_json_file
from utils.validators import validate_api_key, validate_job_description

# Page configuration
st.set_page_config(
    page_title="JobSpecMiner",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'extraction_result' not in st.session_state:
    st.session_state.extraction_result = None

# UI Components
st.title("🔍 JobSpecMiner")
st.markdown("Extract structured information from job descriptions using AI")

# API Key Input
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    value=st.session_state.api_key,
    help="Your API key is stored locally and never sent to our servers"
)

# Job Description Input
job_description = st.text_area(
    "Job Description",
    height=300,
    placeholder="Paste the job description here..."
)

# Extract Button
if st.button("🔍 Extract Information", type="primary"):
    # Validation
    if not validate_api_key(api_key):
        st.error("Please enter a valid API key")
    elif not validate_job_description(job_description):
        st.error("Please enter a job description")
    else:
        # Store API key in session
        st.session_state.api_key = api_key
        
        # Process extraction
        with st.spinner("Extracting information..."):
            extractor = JobExtractor(api_key=api_key)
            result = extractor.extract_information(job_description)
            
            if result:
                st.session_state.extraction_result = result
                st.success("✅ Extraction complete!")
            else:
                st.error("❌ Extraction failed. Please check your API key and try again.")

# Display Results
if st.session_state.extraction_result:
    result = st.session_state.extraction_result
    
    # Display results
    st.header("Extracted Information")
    
    # Basic Information
    with st.expander("Basic Information"):
        st.write(f"**Job Title:** {result.job_title}")
        if result.company_name:
            st.write(f"**Company:** {result.company_name}")
        # ... more fields
    
    # Download Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        txt_content = generate_txt_file(result)
        st.download_button(
            label="📥 Download as TXT",
            data=txt_content,
            file_name="job_extraction.txt",
            mime="text/plain"
        )
    
    with col2:
        json_content = generate_json_file(result)
        st.download_button(
            label="📥 Download as JSON",
            data=json_content,
            file_name="job_extraction.json",
            mime="application/json"
        )
```

#### src/file_generator.py

```python
"""File generation utilities for job extraction results."""
from datetime import datetime
from src.models import JobInformation
import json


def generate_txt_file(job_info: JobInformation) -> str:
    """Generate formatted TXT file content.
    
    Args:
        job_info: Extracted job information
        
    Returns:
        Formatted text string
    """
    # Reuse logic from job_extractor.py format_output method
    # ... (same as existing format_output)
    pass


def generate_json_file(job_info: JobInformation) -> str:
    """Generate JSON file content.
    
    Args:
        job_info: Extracted job information
        
    Returns:
        JSON string
    """
    return job_info.model_dump_json(indent=2, exclude_none=True)
```

#### utils/validators.py

```python
"""Input validation utilities."""
import re


def validate_api_key(api_key: str) -> bool:
    """Validate Gemini API key format.
    
    Args:
        api_key: API key string
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not api_key.strip():
        return False
    # Basic format check (adjust based on actual Gemini key format)
    return len(api_key.strip()) > 10


def validate_job_description(description: str) -> bool:
    """Validate job description input.
    
    Args:
        description: Job description text
        
    Returns:
        True if valid, False otherwise
    """
    if not description or not description.strip():
        return False
    # Minimum length check
    return len(description.strip()) > 50
```

#### .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
```

#### requirements.txt

```txt
streamlit>=1.28.0
google-genai>=0.2.0
pydantic>=2.0.0
```

---

## 10. Implementation Checklist

### Phase 1: Setup
- [ ] Create project directory
- [ ] Copy existing models.py
- [ ] Copy existing job_extractor.py
- [ ] Create requirements.txt
- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Create .streamlit/config.toml
- [ ] Create basic app.py skeleton

### Phase 2: UI Development
- [ ] Implement page header
- [ ] Add API key input field
- [ ] Add job description text area
- [ ] Add extract button
- [ ] Implement session state management
- [ ] Add loading spinner
- [ ] Create results display section
- [ ] Add error message display

### Phase 3: Integration
- [ ] Integrate JobExtractor in app.py
- [ ] Connect UI to extraction logic
- [ ] Implement error handling
- [ ] Add success/error feedback
- [ ] Test API integration

### Phase 4: File Generation
- [ ] Create file_generator.py
- [ ] Implement generate_txt_file()
- [ ] Implement generate_json_file()
- [ ] Add download buttons to UI
- [ ] Test file downloads

### Phase 5: Validation & Polish
- [ ] Create validators.py
- [ ] Add input validation
- [ ] Improve error messages
- [ ] Add help text and tooltips
- [ ] Improve UI styling
- [ ] Add character counter
- [ ] Test edge cases

### Phase 6: Testing
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Manual testing checklist
- [ ] Fix bugs
- [ ] Performance testing

### Phase 7: Deployment
- [ ] Choose deployment platform
- [ ] Create deployment configuration
- [ ] Set up repository
- [ ] Deploy application
- [ ] Test deployed version
- [ ] Document deployment process

### Phase 8: Documentation
- [ ] Update README.md
- [ ] Add usage instructions
- [ ] Document API requirements
- [ ] Add screenshots
- [ ] Create user guide

---

## 11. Timeline Estimate

| Phase | Duration | Tasks |
|-------|----------|-------|
| Phase 1: Setup | 2-3 hours | Project setup, dependencies |
| Phase 2: UI Development | 4-6 hours | Streamlit UI components |
| Phase 3: Integration | 3-4 hours | Connect components |
| Phase 4: File Generation | 2-3 hours | Download functionality |
| Phase 5: Polish | 3-4 hours | Validation, styling |
| Phase 6: Testing | 4-6 hours | Unit and integration tests |
| Phase 7: Deployment | 2-3 hours | Deploy and configure |
| Phase 8: Documentation | 2-3 hours | Write documentation |

**Total Estimated Time:** 22-32 hours (3-4 days of focused work)

---

## 12. Risk Mitigation

### 12.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Netlify doesn't support Streamlit | High | Use stlite or alternative platform |
| API key security concerns | Medium | Clear warnings, server-side option |
| CORS issues with browser-based | Medium | Use server-side deployment |
| API rate limits | Low | Add rate limiting, error handling |
| Large file downloads | Low | Optimize file generation |

### 12.2 Deployment Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Platform limitations | High | Have backup deployment options |
| Configuration issues | Medium | Document thoroughly, test locally |
| Environment variables | Low | Use platform's secret management |

---

## 13. Success Criteria

### 13.1 Functional Requirements
- ✅ User can input Gemini API key
- ✅ User can paste job description
- ✅ Extraction works correctly
- ✅ Results are displayed clearly
- ✅ TXT file downloads correctly
- ✅ JSON file downloads correctly
- ✅ Error handling works properly

### 13.2 Non-Functional Requirements
- ✅ App loads in < 3 seconds
- ✅ Extraction completes in < 30 seconds
- ✅ UI is intuitive and user-friendly
- ✅ Works on desktop and mobile browsers
- ✅ Secure API key handling
- ✅ Clear error messages

---

## 14. Future Enhancements

### 14.1 Short-term (Post-MVP)
- [ ] Multiple job descriptions batch processing
- [ ] History of extractions (session-based)
- [ ] Export to CSV format
- [ ] Copy to clipboard functionality
- [ ] Dark mode theme

### 14.2 Medium-term
- [ ] User accounts and saved extractions
- [ ] API endpoint for programmatic access
- [ ] Comparison tool (compare multiple jobs)
- [ ] Analytics dashboard
- [ ] Custom extraction templates

### 14.3 Long-term
- [ ] Database storage
- [ ] Advanced filtering and search
- [ ] Integration with job boards
- [ ] Machine learning improvements
- [ ] Multi-language support

---

## 15. Deployment Instructions

### 15.1 Streamlit Community Cloud (Recommended)

1. **Prepare Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `JobSpecMiner-WebApp`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Access:**
   - App will be available at: `https://your-app-name.streamlit.app`

### 15.2 Netlify with stlite

1. **Install stlite:**
   ```bash
   pip install stlite
   ```

2. **Build:**
   ```bash
   stlite build app.py --outdir dist
   ```

3. **Deploy to Netlify:**
   - Connect GitHub repo
   - Build command: `stlite build app.py --outdir dist`
   - Publish directory: `dist`
   - Deploy

### 15.3 Render.com

1. **Create render.yaml:**
   ```yaml
   services:
     - type: web
       name: jobspecminer
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy:**
   - Connect GitHub repo to Render
   - Select service type: Web Service
   - Configure as above
   - Deploy

---

## 16. Conclusion

This plan provides a comprehensive roadmap for building a Streamlit web application for JobSpecMiner. The implementation can be completed in 3-4 days with focused development.

**Key Recommendations:**
1. **Use Streamlit Community Cloud** for easiest deployment and best features
2. **Reuse existing code** from JobSpecMiner (models.py, job_extractor.py)
3. **Focus on user experience** with clear UI and helpful error messages
4. **Implement proper security** for API key handling
5. **Test thoroughly** before deployment

**Next Steps:**
1. Review and approve this plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Iterate based on testing and feedback

---

**Plan Version:** 1.0  
**Last Updated:** December 2024  
**Status:** Ready for Implementation
