"""File generation utilities for job extraction results."""
from datetime import datetime
from .models import JobInformation


def format_output_text(job_info: JobInformation, extraction_date: str) -> str:
    """Format extracted information as a well-formatted text file.
    
    This is a standalone version of the format_output method from JobExtractor
    to avoid needing an API key just for formatting.
    
    Args:
        job_info: Extracted job information
        extraction_date: Date string when extraction was performed
        
    Returns:
        Formatted text string
    """
    output = []
    output.append("=" * 80)
    output.append("JOB INFORMATION EXTRACTION")
    output.append("=" * 80)
    output.append(f"\nExtraction Date: {extraction_date}\n")
    output.append("-" * 80)
    
    # Basic Information
    output.append("\nBASIC INFORMATION")
    output.append("-" * 80)
    if job_info.job_title:
        output.append(f"Job Title: {job_info.job_title}")
    if job_info.company_name:
        output.append(f"Company: {job_info.company_name}")
    if job_info.department:
        output.append(f"Department: {job_info.department}")
    if job_info.seniority_level:
        output.append(f"Seniority Level: {job_info.seniority_level}")
    if job_info.years_of_experience:
        output.append(f"Years of Experience: {job_info.years_of_experience}")
    
    # Work Arrangement
    output.append("\nWORK ARRANGEMENT")
    output.append("-" * 80)
    if job_info.work_type:
        output.append(f"Work Type: {job_info.work_type}")
    if job_info.location:
        output.append(f"Location: {job_info.location}")
    
    # Compensation
    if job_info.salary:
        output.append("\nCOMPENSATION")
        output.append("-" * 80)
        output.append(f"Salary: {job_info.salary}")
    
    # Education
    if job_info.education_requirements:
        output.append("\nEDUCATION REQUIREMENTS")
        output.append("-" * 80)
        output.append(job_info.education_requirements)
    
    # Required Criteria
    if job_info.required_criteria:
        output.append("\nREQUIRED CRITERIA")
        output.append("-" * 80)
        for i, criterion in enumerate(job_info.required_criteria, 1):
            output.append(f"{i}. {criterion}")
    
    # Preferred Qualifications
    if job_info.preferred_qualifications:
        output.append("\nPREFERRED QUALIFICATIONS")
        output.append("-" * 80)
        for i, qual in enumerate(job_info.preferred_qualifications, 1):
            output.append(f"{i}. {qual}")
    
    # Skills
    if job_info.skills:
        output.append("\nSKILLS & TECHNOLOGIES")
        output.append("-" * 80)
        for i, skill in enumerate(job_info.skills, 1):
            output.append(f"{i}. {skill}")
    
    # Scope of Responsibilities
    if job_info.scope_of_responsibilities:
        output.append("\nSCOPE OF RESPONSIBILITIES")
        output.append("-" * 80)
        for i, responsibility in enumerate(job_info.scope_of_responsibilities, 1):
            output.append(f"{i}. {responsibility}")
    
    # Benefits
    if job_info.benefits:
        output.append("\nBENEFITS & PERKS")
        output.append("-" * 80)
        for i, benefit in enumerate(job_info.benefits, 1):
            output.append(f"{i}. {benefit}")
    
    # Additional Information
    if job_info.additional_info:
        output.append("\nADDITIONAL INFORMATION")
        output.append("-" * 80)
        output.append(job_info.additional_info)
    
    output.append("\n" + "=" * 80)
    return "\n".join(output)


def generate_txt_file(job_info: JobInformation) -> str:
    """Generate formatted TXT file content.
    
    Args:
        job_info: Extracted job information
        
    Returns:
        Formatted text string
    """
    extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return format_output_text(job_info, extraction_date)


def generate_json_file(job_info: JobInformation) -> str:
    """Generate JSON file content.
    
    Args:
        job_info: Extracted job information
        
    Returns:
        JSON string with indentation
    """
    return job_info.model_dump_json(indent=2, exclude_none=True)
