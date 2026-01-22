template = """Analyze the following text from a "Convocatoria" (Grant Call) and extract its key details into JSON.

**Input Text:**
{last_message}

**EVALUATION CRITERIA:**
1. **Objective & Description:** These are mandatory. 
   - Fill "description" with a summary of the call.
   - Fill "objective" with the main goal. 
   - If only one descriptive block is found, USE IT FOR BOTH FIELDS. Do not leave "objective" null if there is any text available.
2. **Title:** Use the value after "TÍTULO:".
3. **Funding:** Extract any financial information. Use "No especificado" if missing.
4. **Important Dates:** Extract opening/closing dates. Use "Fechas no detectadas" if missing.
5. **Keywords:** Extract or generate 3-5 keywords.
6. **Benefits:** List any advantages or support offered.

**JSON Schema:**
{{
    "title": "str or null",
    "objective": "str (MANDATORY)",
    "description": "str (MANDATORY)",
    "funding": "str or null",
    "keywords": ["str"],
    "important_dates": "str or null",
    "benefits": ["str"],
    "url": "str or null"
}}

Output ONLY the raw JSON."""


