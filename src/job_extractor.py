"""Main application for extracting job information using Gemini API."""
import sys
from datetime import datetime
from typing import Optional

from google import genai
from pydantic import ValidationError

from .models import JobInformation


class JobExtractor:
    """Extracts structured information from job descriptions using Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """Initialize the job extractor with Gemini API.
        
        Args:
            api_key: Gemini API key
            model_name: Name of the Gemini model to use (e.g., gemini-2.5-flash, gemini-2.0-flash)
                       Must support structured outputs
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        
    def extract_information(self, job_description: str) -> Optional[JobInformation]:
        """Extract structured information from a job description using Gemini structured outputs.
        
        Args:
            job_description: Raw job description text
            
        Returns:
            JobInformation object with extracted data, or None if extraction fails
        """
        prompt = f"""Analyze the following job description and extract all relevant structured information.

Extract information about:
- Job title, company name, and department
- Seniority level and years of experience required
- Work arrangement (Remote, Hybrid, or On-site) and location
- Salary or compensation information
- Required criteria and qualifications
- Preferred qualifications
- Scope of responsibilities and duties
- Technical skills and technologies
- Education requirements
- Benefits and perks
- Any additional relevant information

Job Description:
{job_description}

Extract all relevant information. If a field is not mentioned in the job description, use null for optional string fields or an empty array for list fields."""

        try:
            # Use structured outputs with Pydantic schema
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": JobInformation.model_json_schema(),
                },
            )
            
            # Validate and parse the structured response
            job_info = JobInformation.model_validate_json(response.text)
            return job_info
            
        except ValidationError as e:
            print(f"Error validating extracted data: {e}", file=sys.stderr)
            try:
                if hasattr(response, 'text'):
                    print(f"Response was: {response.text[:500]}", file=sys.stderr)
            except NameError:
                pass  # response not defined yet
            return None
        except Exception as e:
            print(f"Error extracting information: {e}", file=sys.stderr)
            if hasattr(e, '__cause__') and e.__cause__:
                print(f"Underlying error: {e.__cause__}", file=sys.stderr)
            return None
    
    def format_output(self, job_info: JobInformation, extraction_date: str) -> str:
        """Format extracted information as a well-formatted text file.
        
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
