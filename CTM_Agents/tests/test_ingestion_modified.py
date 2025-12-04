import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.tech_surveillance.nodes.ingestion.squemas import IngestionResult, CallInfo
from agents.tech_surveillance.nodes.ingestion.prompts import template

def test_ingestion_result_schema():
    print("Testing IngestionResult schema...")
    try:
        # Test with only call_info
        call_info = CallInfo(title="Test Call", objective="Test Objective")
        result = IngestionResult(call_info=call_info)
        print("✅ IngestionResult created successfully with call_info.")
        
        # Verify no project_info field
        if hasattr(result, 'project_info'):
            print("❌ Error: IngestionResult still has project_info field.")
        else:
            print("✅ IngestionResult does not have project_info field.")
            
    except Exception as e:
        print(f"❌ Error creating IngestionResult: {e}")

def test_prompt_template():
    print("\nTesting Prompt Template...")
    if "GENERATE a project" in template:
        print("❌ Error: Prompt still contains 'GENERATE a project'.")
    elif "DO NOT generate any project information" in template:
        print("✅ Prompt contains 'DO NOT generate any project information'.")
    else:
        print("⚠️ Warning: Prompt might not be updated correctly. Please check manually.")

if __name__ == "__main__":
    test_ingestion_result_schema()
    test_prompt_template()
