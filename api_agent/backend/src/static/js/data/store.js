// Shared State
export const store = {
    selectedValue: "",
    selectedCallText: "", // New: Store the full text
    sessionId: null,      // New: Store the session ID
    currentSelectedIdea: null,
    maxReachedStep: 1,
    convocatorias: [],     // Real convocatorias from DB
    statusFilter: 'active',
    categoryFilter: 'all'
};
