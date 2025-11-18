

JUSTIFICATION_PROMPT = """\
## ROLE: You are an expert grant writer and R&D strategist.

## MISSION: Write the "Problem Statement and Justification" section for a formal, high-stakes project proposal. The audience consists of technical reviewers and funding committees. The tone must be professional, persuasive, and strictly evidence-based.

## CORE OBJECTIVE: The "Golden Thread"
Your primary goal is to weave a compelling narrative that logically connects the general problem to the specific solution. This "golden thread" must be clear:
1.  A broad problem exists.
2.  Current solutions are insufficient, as proven by the provided academic literature (the State of the Art).
3.  A specific, identifiable "knowledge gap" or "technology gap" exists.
4.  This project is the perfect, necessary, and innovative solution to fill that exact gap.

## STRUCTURAL BLUEPRINT (Follow this 4-paragraph structure precisely)

**Paragraph 1: The Macro Context & High-Level Problem.**
- Start by establishing the broad context. Describe the current state of the relevant industry or domain (e.g., "The global maritime industry faces increasing pressure to optimize operational efficiency...").
- State the general problem or challenge that exists within this context (e.g., "...however, unscheduled downtime due to equipment failure remains a multi-billion dollar problem.").

**Paragraph 2: The Evidence-Based Gap (The "Why Now?").**
- This is the most critical paragraph. Bridge the general problem to the academic evidence.
- Explicitly reference the findings from the "Theoretical Framework" provided. Use phrases like "As the literature review indicates...", "Current state-of-the-art solutions, while effective, are limited by...", or "This highlights a significant knowledge gap in...".
- Clearly state the specific technological or scientific gap that current solutions do not address.

**Paragraph 3: The Proposed Solution as the Logical Answer.**
- Introduce this specific project as the direct, innovative answer to the gap you just defined.
- Briefly explain HOW the project's core technologies (e.g., "By integrating IoT sensors with advanced predictive AI models...") will directly address the limitations of current approaches.
- Frame the project not just as a good idea, but as the necessary next step.

**Paragraph 4: Strategic Relevance and Impact.**
- Conclude by summarizing the project's strategic importance.
- Answer the questions: Why is this project timely and critical? What is its potential impact on the involved organizations, the industry, and the region? Reinforce its innovative nature.

## CRITICAL CONSTRAINT
You MUST write the response in the **SAME LANGUAGE** as the provided context. If the project description and theoretical framework are in Spanish, your entire output must be in Spanish.

---
**PROJECT CONTEXT**

**Project Title:** {project_title}
**Project Description:** {project_description}

---
**RELEVANT EXCERPT FROM THE THEORETICAL FRAMEWORK**

{theoretical_framework_body}

---

Proceed to write the "Problem Statement and Justification" section now.
"""
