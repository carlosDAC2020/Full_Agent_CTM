// Shared State
export const store = {
    selectedValue: "",
    selectedCallText: "", // New: Store the full text
    sessionId: null,      // New: Store the session ID
    currentSelectedIdea: null,
    maxReachedStep: 1,
    convocatorias: [],     // Real convocatorias from DB
    callInfo: null,        // NEW: Current analyzed call details
    statusFilter: 'active',
    categoryFilter: 'all',
    // NEW: Store selected thematic line and methodology for idea generation
    selectedThematicLine: null,
    selectedMethodology: null,

    // NEW: Store final project results for modal population
    finalResult: null
};
