# prompts.py

# ... (otros prompts) ...

ACTIVITY_SCHEDULE_PROMPT = """\
## ROLE: You are a senior Project Manager with extensive experience planning complex R&D projects.

## MISSION: Create a detailed "Activity Schedule" for a formal project proposal. Your task is to break down the project's methodological phases into specific activities, key milestones, and their primary deliverables. The final output MUST be a professional Markdown table.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Proposed Methodology (High-Level Phases):**
{methodology}
- **Specific Project Objectives (which this schedule must achieve):**
{specific_objectives_smart}

## INSTRUCTIONS

1.  **Adopt the Structure:** Use the high-level phases provided in the "Proposed Methodology" as the main sections of your schedule.
2.  **Define Activities:** For each phase, define 2-4 specific, actionable activities or milestones.
3.  **CRITICAL ALIGNMENT:** Ensure that the activities you define are concrete steps required to meet the "Specific Project Objectives". The schedule must be a practical roadmap for achieving those goals.
4.  **Identify Deliverables:** For each activity, specify the main tangible output (e.g., "Technical Requirements Document", "Trained AI Model v1.0", "Final Report").
5.  **Estimate Duration:** Provide a realistic time estimate in weeks for each activity.

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown table)

### 7.1. Cronograma de Actividades

| Fase | Actividad / Hito Clave | Entregable Principal | Duración Estimada (Semanas) |
| :--- | :--- | :--- | :--- |
| **Fase 1: [Nombre de la Fase]** | *Resumen de la fase* | | **[Duración Total Fase]** |
| | 1.1. [Nombre de la Actividad] | [Nombre del Entregable] | [Número] |
| | 1.2. [Nombre de la Actividad] | [Nombre del Entregable] | [Número] |
| **Fase 2: [Nombre de la Fase]** | *Resumen de la fase* | | **[Duración Total Fase]** |
| | 2.1. [Nombre de la Actividad] | [Nombre del Entregable] | [Número] |
| | ... | ... | ... |

---
Proceed to generate the activity schedule now.
"""