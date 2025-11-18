# prompts.py

# ... (otros prompts) ...

METHODOLOGY_PROMPT = """\
## ROLE: You are a senior Systems Engineer and Project Management expert.

## MISSION: Write the "Proposed Methodology" section for a formal R&D proposal. Your task is to select a suitable development and management framework and outline its main phases. The tone must be clear, structured, and professional.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Project Objectives:**
  - **General:** {general_objective}
  - **Specifics:** {specific_objectives_smart}

## INSTRUCTIONS

**Step 1: Select an Appropriate Methodology.**
- Based on the project objectives, choose a well-established industry-standard methodology.
- **Good candidates include:**
  - **V-Model:** Excellent for projects with clear requirements and where verification and validation are critical at each stage (common in engineering and hardware integration).
  - **CRISP-DM:** The standard for data science and machine learning projects, focusing on data understanding, modeling, and evaluation.
  - **Agile (Scrum/Kanban):** Best for software-heavy projects where requirements may evolve and iterative development is beneficial.
- You must choose only ONE and state it clearly.

**Step 2: Justify Your Choice.**
- In one paragraph, briefly explain *why* the selected methodology is the best fit for this specific project. Connect it back to the project's objectives (e.g., "The V-Model is selected due to the project's emphasis on integrating physical sensors (IoT) with software systems, requiring rigorous testing at each phase to meet Objective 2...").

**Step 3: Outline the Key Phases.**
- Describe the primary phases or stages of the chosen methodology as they would apply to this project.
- Provide a short (1-2 sentence) description for each phase. This should be a high-level overview, not a detailed task list.

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown)

### **6. Metodología Propuesta**

**Framework Seleccionado:** (e.g., Modelo en V de Ingeniería de Sistemas)

(Your justification paragraph here.)

**Fases Principales de la Metodología:**

*   **Fase 1: [Nombre de la Fase]** - (Breve descripción de la fase).
*   **Fase 2: [Nombre de la Fase]** - (Breve descripción de la fase).
*   **Fase 3: [Nombre de la Fase]** - (Breve descripción de la fase).
*   **(etc., for all key phases)**

---
Proceed to generate the methodology section now.
"""