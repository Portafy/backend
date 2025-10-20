import fitz

PROMPT = """
You are an intelligent AI assistant.

You will receive raw text extracted from a user's resume, portfolio, or bio. Your task is to analyze the content and return a structured JSON object **strictly matching the format provided** below.

RETURN RULES:
- Return only valid, raw JSON.
- DO NOT wrap the output in markdown (no ```json, no ```).
- DO NOT escape characters like `\\n`, `\\t`, or `\\"`.
- DO NOT include commentary or any non-JSON text.
- Output MUST be a **parseable JSON object** — no explanation, formatting, or decoration.

If any field is missing from the input, set its corresponding `"has_*"` key to `false` and use appropriate empty defaults (e.g. `[]`, `""`, `null`).

JSON STRUCTURE TO RETURN:
{
  "has_personal_info": bool,
  "personal_info": {
    "full_name": str,
    "title": str,
    "profile_picture_url": str,
    "bio": str,
    "contact": {
      "email": str,
      "phone": str,
      "location": str
    },
    "links": {
      "linkedin": str,
      "github": str,
      "twitter": str,
      "website": str
    }
  },
  "has_summary": bool,
  "summary": str,
  "has_experience": bool,
  "experience": [
    {
      "job_title": str,
      "company": str,
      "location": str,
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "responsibilities": [str]
    }
  ],
  "has_education": bool,
  "education": [
    {
      "degree": str,
      "institution": str,
      "location": str,
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "description": str
    }
  ],
  "has_skills": bool,
  "skills": {
    "languages": [str],
    "frameworks": [str],
    "databases": [str],
    "cloud": [str],
    "tools": [str],
    "soft": [str]
  },
  "has_projects": bool,
  "projects": [
    {
      "title": str,
      "description": str,
      "technologies": [str],
      "live_demo_url": str,
      "github_url": str,
      "case_study_url": str,
      "media": [str]
    }
  ],
  "has_awards": bool,
  "awards": [
    {
      "title": str,
      "issuer": str,
      "date": "YYYY-MM",
      "description": str
    }
  ],
  "has_certifications": bool,
  "certifications": [
    {
      "title": str,
      "issuer": str,
      "date": "YYYY-MM",
      "url": str
    }
  ],
  "has_languages": bool,
  "languages": [
    {
      "name": str,
      "proficiency": str
    }
  ]
}
RAW INPUT TEXT STARTS HERE:

{pdf text here}
"""


PROMPT = """
You are a highly intelligent and detail-oriented AI assistant specialized in parsing, interpreting, and normalizing unstructured data from resumes, portfolios, or bios.

You will receive raw text extracted from a user-uploaded PDF file. This input may contain irregular formatting, broken lines, missing labels, inconsistent date formats, or mixed metadata. Your task is to clean, normalize, and extract structured data into a well-formed JSON strictly following the schema below.

--- YOUR OBJECTIVES ---

1. **Understand and Normalize**:
   - Fix obfuscated or broken lines (e.g., “Expe\nrience” → “Experience”).
    - Correct inconsistent date formats (e.g., "2021_05" → "2021-05").
   - Deduce and fix improperly split paragraphs or headings.
   - Use context clues to infer missing labels when possible (e.g., if a GitHub URL is present, map it to `"github"` even if unlabeled).

2. **Clean and Recover**:
   - Strip out headers/footers, repeated sections, or page numbers if they appear.
   - Correct text alignment or encoding issues.
   - Trim excessive whitespace, control characters, or filler words.

3. **Validate Strictly**:
   - Output **raw, valid JSON only**. Do NOT include markdown formatting or commentary.
   - Escape nothing. DO NOT include `\\n`, `\\t`, or any escape sequences.
   - Ensure the result is machine-parseable with no syntax errors.

4. **Handle Missing Data Gracefully**:
   - If any section is not found, set the `"has_*"` key to `false` and use appropriate empty defaults (`[]`, `""`, or `null`).

--- OUTPUT FORMAT TO FOLLOW EXACTLY ---
{
  "has_personal_info": bool,
  "personal_info": {
    "full_name": str,
    "title": str,
    "profile_picture_url": str,
    "bio": str,
    "contact": {
      "email": str,
      "phone": str,
      "location": str
    },
    "links": {
      "linkedin": str,
      "github": str,
      "twitter": str,
      "website": str
    }
  },
  "has_summary": bool,
  "summary": str,
  "has_experience": bool,
  "experience": [
    {
      "job_title": str,
      "company": str,
      "location": str,
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "responsibilities": [str]
    }
  ],
  "has_education": bool,
  "education": [
    {
      "degree": str,
      "institution": str,
      "location": str,
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM",
      "description": str
    }
  ],
  "has_skills": bool,
  "skills": {
    "languages": [str],
    "frameworks": [str],
    "databases": [str],
    "cloud": [str],
    "tools": [str],
    "soft": [str]
  },
  "has_projects": bool,
  "projects": [
    {
      "title": str,
      "description": str,
      "technologies": [str],
      "live_demo_url": str,
      "github_url": str,
      "case_study_url": str,
      "media": [str]
    }
  ],
  "has_awards": bool,
  "awards": [
    {
      "title": str,
      "issuer": str,
      "date": "YYYY-MM",
      "description": str
    }
  ],
  "has_certifications": bool,
  "certifications": [
    {
      "title": str,
      "issuer": str,
      "date": "YYYY-MM",
      "url": str
    }
  ],
  "has_languages": bool,
  "languages": [
    {
      "name": str,
      "proficiency": str
    }
  ]
}

--- RAW INPUT TEXT STARTS HERE ---
{pdf text here}
"""

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""

    for page in doc:
        text_blocks = page.get_text(
            "blocks"
        )  # (x0, y0, x1, y1, "text", block_no, block_type)
        sorted_blocks = sorted(
            text_blocks, key=lambda b: (b[1], b[0])
        )  # top to bottom, left to right

        for block in sorted_blocks:
            if block[4].strip():  # ignore empty
                all_text += block[4].strip() + "\n\n"

    return all_text.strip()


def convert_text_to_json(text):
    print("text", text)
    """
    Convert the extracted text to a structured JSON format.
    """
    import json
    import re

    # extract content inside triple backticks
    match = re.search(r"```json\n(.*?)```", text, re.DOTALL)
    
    if match:
        raw_json = match.group(1)
        parsed_json = json.loads(raw_json)  # Now this is a usable Python dict
    else:
        return None

    return parsed_json
