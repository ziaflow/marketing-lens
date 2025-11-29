import logging
import json
from .tools import GoogleAnalyticsTools

class GoogleAnalyticsMCPServer:
    def __init__(self, credentials_json: str = None):
        self.tools = GoogleAnalyticsTools(credentials_json)

    def execute_tool(self, tool_name: str, arguments: dict):
        """
        Executes a tool by name with provided arguments.
        """
        logging.info(f"Executing GA MCP Tool: {tool_name}")

        try:
            if tool_name == "get_account_summaries":
                return self.tools.list_account_summaries()

            elif tool_name == "run_report":
                return self.tools.run_report(
                    property_id=arguments.get("property_id"),
                    start_date=arguments.get("start_date", "7daysAgo"),
                    end_date=arguments.get("end_date", "yesterday"),
                    dimensions=arguments.get("dimensions"),
                    metrics=arguments.get("metrics")
                )

            elif tool_name == "run_realtime_report":
                return self.tools.run_realtime_report(
                    property_id=arguments.get("property_id"),
                    dimensions=arguments.get("dimensions"),
                    metrics=arguments.get("metrics")
                )

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

        except Exception as e:
            logging.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"error": str(e)}
