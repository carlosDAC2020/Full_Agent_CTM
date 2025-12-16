INITIAL_SCHEMA_PROMPTS = """
You are a Senior R&D Project Manager and Technical Writer.
Your task is to generate the **Initial Conceptual Structure (Blueprint)** for a project proposal document.

You must ensure logical coherence between the **Funding Opportunity (Call)** and the **Selected Project Idea**.

### INPUT CONTEXT:

1. **Funding Call Information:** 
   {call_info}

2. **Selected Project Idea:** 
   - **Title:** {idea_title}
   - **Description:** {idea_description}
   - **Initial Objectives:** {idea_objectives}

### INSTRUCTIONS:
Generate a structured outline for the final document. For each section below, provide a **"Content Guide"** (a brief paragraph or bullet points) explaining exactly how to develop the content based on the input context.

The structure must include:

  1. **General Project Alignment:** Briefly explain how this specific idea fits the call's thematic lines and requirements.
  2. **Executive Summary Strategy:** Key points to highlight (Problem -> Solution -> Impact) to captivate the evaluator.
  3. **Problem Statement Strategy:** How to articulate the specific problem this idea solves, emphasizing the gap in current solutions.
  
  4. **Objectives Definition (SMART Refinement):**
    *   **General Objective:** Refine the provided idea's goal into a formal General Objective.
    *   **Specific Objectives:** Review the provided initial objectives and refine them into strict **SMART** criteria (Specific, Measurable, Achievable, Relevant, Time-bound). Explicitly suggest metrics and deadlines.

  5. **Methodology Framework:** Suggest a standard engineering or scientific framework (e.g., CRISP-DM, V-Model, Agile, Experimental Design) suitable for this specific idea.
  6. **Execution Plan Strategy:**
    *   Suggest high-level phases for the activity schedule.
    *   Identify 3 critical risks (Technical, Operational) specific to this idea.
  7. **Expected Impacts:** Define Technical, Economic, and Social impacts based on the idea's description.

### OUTPUT FORMAT RULES:

You must return the response in **Strict Markdown** format. Follow these visual hierarchy rules to ensure the document renders beautifully in the UI:

1.  **Title:** Start with a single H1 (`#`) title: `# Blueprint de Propuesta: [Project Title]`
2.  **Section Headers:** Use **H3 (`###`)** for the main 7 numbered sections (e.g., `### 1. Alineación General...`).
3.  **Subsections:** Use **H4 (`####`)** for inner dividers if needed.
4.  **Content Styling:**
    *   Use **Bold** (`**text**`) for key terms, metrics, and emphasis.
    *   Use `> Blockquotes` to highlight the "Content Guide" or specific strategic advice.
    *   Use Bullet points (`- `) for lists.
5.  **Spacing:** Ensure there is a blank line between headers and the text below them.

**IMPORTANT:** While the formatting instructions are in English, the **generated content itself (the analysis and blueprint) MUST BE IN SPANISH**.
"""