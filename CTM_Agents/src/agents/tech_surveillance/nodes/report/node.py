from agents.tech_surveillance.state import GraphState

def report_mode(state: GraphState):
    """ gnera los reportes de investigacion """

    print("----------------- REPORTE NODE -----------------")
    # With latest_value: get the last update
    report = state.get("academic_research_results", "No report generated")
    
    
    print(report)
    return {"academic_research_results": report}