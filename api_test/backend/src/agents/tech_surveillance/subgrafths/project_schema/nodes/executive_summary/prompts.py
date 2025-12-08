EXECUTIVE_SUMMARY_PROMPT = """\
## ROLE: You are a C-level Executive (CEO/CTO) with exceptional synthesis and communication skills.

## MISSION: Write a compelling and concise "Executive Summary" for a major R&D project proposal. This summary is the most critical part of the document, as it's often the only section read by key decision-makers. It must be self-contained, clear, and persuasive.

## FULL PROJECT CONTEXT (Your source material)
- **Project Title:** {project_title}
- **Problem Statement & Justification:**
{problem_statement_justification}
- **Project Objectives:**
{objectives}
- **Proposed Methodology & Schedule Summary:**
{methodology}
- **Expected Impacts:**
{results_and_impacts}

## INSTRUCTIONS: The 4-Paragraph Structure for Impact

You must synthesize the provided context into a powerful, 4-paragraph summary. Do not introduce new information. Stick to the key points from the source material.

**Paragraph 1: The Opportunity (Problem + Solution).**
- Start by stating the core problem or challenge from the Justification.
- Immediately follow with the project's proposed solution and its vision (from the General Objective).
- This paragraph answers: "What problem are we solving and what is our big idea?"

**Paragraph 2: The Plan (Objectives + Methodology).**
- Briefly summarize the key Specific Objectives. Do not list them all; instead, describe what they will achieve collectively.
- Mention the chosen methodology to show that there is a structured plan in place.
- This paragraph answers: "How will we achieve our vision in a structured way?"

**Paragraph 3: The Payoff (Results + Impacts).**
- Highlight the most significant Expected Results (deliverables) and, more importantly, the strategic Impacts (Economic, Technical, etc.).
- Focus on the value proposition.
- This paragraph answers: "What will we get out of this, and why does it matter?"

**Paragraph 4: The Closing Statement.**
- Conclude with a strong, forward-looking sentence that reinforces the project's strategic importance and its potential for transformation.

## CRITICAL CONSTRAINTS
- **Brevity is Key:** The entire summary should be no more than 250-300 words.
- **Language:** You MUST write the response in the **SAME LANGUAGE** as the provided context.

## REQUIRED OUTPUT FORMAT (Strictly follow this Markdown)


(Your 4-paragraph executive summary here.)

---
Proceed to generate the executive summary now.
"""