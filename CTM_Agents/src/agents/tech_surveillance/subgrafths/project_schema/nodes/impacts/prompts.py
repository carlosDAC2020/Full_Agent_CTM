

IMPACTS_PROMPT = """\
## ROLE: You are an expert innovation consultant and impact analyst.

## MISSION: Write the "Expected Results and Impacts" section for a formal R&D proposal. Your task is to clearly articulate both the tangible outputs (Results) and the broader strategic benefits (Impacts) of the project.

## CONTEXT FOR YOUR TASK
- **Project Title:** {project_title}
- **Project General Objective:** {general_objective}
- **Project Specific Objectives:**
{specific_objectives_smart}

## INSTRUCTIONS

Your response must be structured into two distinct sub-sections: "Expected Results (Deliverables)" and "Expected Impacts".

### Part 1: Expected Results (Deliverables)
- Analyze the Specific Objectives.
- For each objective, identify the primary TANGIBLE output or deliverable that will be produced.
- Present these as a bulleted list. The results should be concrete items.
- Examples: "A validated predictive maintenance AI model," "A final technical report detailing the system architecture," "A set of training materials for operators," "A peer-reviewed academic publication."

### Part 2: Expected Impacts
- Think bigger picture. How will the successful completion of this project and its results create positive change?
- Describe the impacts across at least three of the following categories:
  - **Technical/Scientific Impact:** How will this project advance the state of the art? Will it create new knowledge or methodologies?
  - **Economic Impact:** Will it reduce costs, create new revenue streams, or improve the competitiveness of the involved organizations?
  - **Social Impact:** Will it create jobs, improve worker safety, or build new skills in the community?
  - **Environmental Impact:** Will it help reduce emissions, save resources, or promote sustainability?
- Write a short paragraph for each impact category you choose.

## LANGUAGE CONSTRAINT
- You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown)

### **8. Resultados e Impactos Esperados**

#### **8.1. Resultados Esperados (Entregables)**
*   **[Nombre del Entregable 1]:** Breve descripción del entregable y a qué objetivo específico corresponde.
*   **[Nombre del Entregable 2]:** Breve descripción del entregable y a qué objetivo específico corresponde.
*   ...

#### **8.2. Impactos Esperados**
*   **Impacto Técnico/Científico:**
    (Párrafo describiendo el impacto en esta área).

*   **Impacto Económico:**
    (Párrafo describiendo el impacto en esta área).

*   **Impacto Social/Ambiental:**
    (Párrafo describiendo el impacto en esta área).

---
Proceed to generate the results and impacts section now.
"""