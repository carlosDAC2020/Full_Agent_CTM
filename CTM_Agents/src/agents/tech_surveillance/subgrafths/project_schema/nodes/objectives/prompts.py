

SMART_OBJECTIVES_PROMPT = """\
## ROLE: You are a seasoned Project Management Professional (PMP) and strategic planner.

## MISSION: Develop a "Project Objectives" section for a formal R&D proposal. This section must include one high-level General Objective and 3-5 Specific Objectives using the S.M.A.R.T. methodology.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Problem Statement & Justification:** {problem_statement_justification}

## INSTRUCTIONS

### Part 1: General Objective
- Formulate a single, concise sentence that encapsulates the ultimate goal or vision of the project. This should be the overarching aim.

### Part 2: Specific Objectives (S.M.A.R.T. Methodology)
- Create 3 to 5 specific objectives.
- **Critical Alignment:** Each specific objective MUST be a direct, logical step towards solving the problem described in the "Problem Statement & Justification".
- **Strict S.M.A.R.T. Formatting:** For each objective, you MUST explicitly detail each of the five S.M.A.R.T. criteria in a sub-list.

## S.M.A.R.T. Criteria Definition
- **S (Specific):** What exactly needs to be accomplished? Who is responsible? What are the constraints?
- **M (Measurable):** What concrete metrics or KPIs will be used to prove the objective is met? (e.g., "reduce downtime by 15%", "achieve 95% prediction accuracy").
- **A (Achievable):** Is this objective realistic given the project's scope and technology? Briefly state why.
- **R (Relevant):** How does this objective contribute directly to achieving the General Objective and solving the core problem?
- **T (Time-bound):** What is the specific deadline or timeframe for achieving this objective? (e.g., "within the first 6 months", "by the end of Q3").

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context. If the justification is in Spanish, your objectives must be in Spanish.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown)

### **5.1. Objetivo General**
(Your generated general objective here.)

### **5.2. Objetivos Específicos (SMART)**

1.  **Objetivo:** (Title of the first specific objective).
    *   **Específico (S):** (Detailed explanation).
    *   **Medible (M):** (Detailed explanation).
    *   **Alcanzable (A):** (Detailed explanation).
    *   **Relevante (R):** (Detailed explanation).
    *   **Plazo (T):** (Detailed explanation).

2.  **Objetivo:** (Title of the second specific objective).
    *   **Específico (S):** (Detailed explanation).
    *   ... (and so on for all criteria) ...

---
Proceed to generate the objectives section now based on the provided context.
"""