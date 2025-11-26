import unittest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage
from agents.tech_surveillance.nodes.ingestion.squemas import IngestionResult, ProjectInfo, CallInfo
from agents.tech_surveillance.state import GraphState, ReportSchema, GeneralInfo

# Mocking the node module to avoid importing real LLM classes at top level if they fail
import sys
from types import ModuleType

# We need to patch the extraction_llm in the node module
with patch('agents.tech_surveillance.nodes.ingestion.node.extraction_llm') as mock_llm:
    from agents.tech_surveillance.nodes.ingestion.node import ingestion_node

class TestIngestionNode(unittest.TestCase):

    def setUp(self):
        self.mock_state = {
            "messages": [HumanMessage(content="Test Input")],
            "report_components": None,
            "call_info": None
        }

    @patch('agents.tech_surveillance.nodes.ingestion.node.extraction_llm')
    def test_ingestion_call_only_generation(self, mock_llm):
        # Setup mock return value for Call Only scenario (Generation)
        mock_result = IngestionResult(
            call_info=CallInfo(title="Call Title", url="http://example.com"),
            project_info=ProjectInfo(
                title="Generated Project",
                description="Generated Description",
                keywords=["k1", "k2"]
            ),
            is_generated_project=True
        )
        mock_llm.invoke.return_value = mock_result

        # Run node
        result = ingestion_node(self.mock_state)

        # Verify State Updates
        self.assertIsNotNone(result.get("call_info"))
        self.assertEqual(result["call_info"].title, "Call Title")
        self.assertEqual(result["call_info"].url, "http://example.com")
        
        # Verify Report Components
        report = result.get("report_components")
        self.assertIsInstance(report, ReportSchema)
        self.assertEqual(report.general_info.project_title, "Generated Project")

        # Verify Message
        messages = result.get("messages")
        self.assertTrue(len(messages) > 0)
        self.assertIn("✨ **Proyecto Generado:**", messages[0].content)
        self.assertIn("✅ **Convocatoria Detectada:**", messages[0].content)

    @patch('agents.tech_surveillance.nodes.ingestion.node.extraction_llm')
    def test_ingestion_call_and_project(self, mock_llm):
        # Setup mock return value for Call + Project scenario
        mock_result = IngestionResult(
            call_info=CallInfo(title="Call Title"),
            project_info=ProjectInfo(
                title="User Project",
                description="User Description",
                keywords=["k1"]
            ),
            is_generated_project=False
        )
        mock_llm.invoke.return_value = mock_result

        # Run node
        result = ingestion_node(self.mock_state)

        # Verify State
        self.assertIsNotNone(result.get("call_info"))
        self.assertEqual(result["call_info"].title, "Call Title")
        
        # Verify Message
        messages = result.get("messages")
        self.assertIn("📋 **Proyecto Registrado:**", messages[0].content)
        self.assertIn("✅ **Convocatoria Detectada:**", messages[0].content)
        self.assertNotIn("✨ **Proyecto Generado:**", messages[0].content)

if __name__ == '__main__':
    unittest.main()
