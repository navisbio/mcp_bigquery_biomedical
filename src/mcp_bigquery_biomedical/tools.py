import logging
from typing import Any

from google.cloud import bigquery

import mcp.types as types
from .memo_manager import MemoManager
from .database import BigQueryDatabase  # Import the BigQueryDatabase class

logger = logging.getLogger('mcp_bigquery_biomedical.tools')


class ToolManager:
    def __init__(self, db: BigQueryDatabase, memo_manager: MemoManager):
        self.memo_manager = memo_manager
        self.db = db  # Use the BigQueryDatabase instance
        logger.info("ToolManager initialized with BigQueryDatabase")
    def get_available_tools(self) -> list[types.Tool]:
        """Return list of available tools."""
        logger.debug("Retrieving available tools")
        tools = [
            types.Tool(
                name="list-datasets",
                description=(
                    "List all available BigQuery public datasets that can be queried. "
                    "These datasets contain various biomedical data that can be analyzed."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="read-query",
                description=(
                    "Execute a SELECT query on the specified BigQuery public dataset. "
                    "Use this tool to extract and analyze specific data from tables. "
                    "IMPORTANT: When using this tool, your answer must be based solely on the data retrieved from the query."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dataset": {"type": "string", "description": "Name of the BigQuery dataset to query"},
                        "query": {"type": "string", "description": "SELECT SQL query to execute"},
                    },
                    "required": ["dataset", "query"],
                },
            ),
            types.Tool(
                name="list-tables",
                description=(
                    "Retrieve a list of all available tables in the specified BigQuery public dataset. "
                    "This tool helps you understand the dataset structure and explore available data."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dataset": {"type": "string", "description": "Name of the BigQuery dataset to explore"},
                    },
                    "required": ["dataset"],
                },
            ),
            types.Tool(
                name="describe-table",
                description=(
                    "Get detailed schema information of a specific table in the specified BigQuery public dataset."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "dataset": {"type": "string", "description": "Name of the BigQuery dataset containing the table"},
                        "table_name": {"type": "string", "description": "Name of the table to describe"},
                    },
                    "required": ["dataset", "table_name"],
                },
            ),
            types.Tool(
                name="append-insight",
                description=(
                    "Record key findings and insights discovered during your analysis of the Open Targets datasets. "
                    "Use this tool whenever you uncover meaningful patterns, trends, or notable observations about targets, diseases, associations, or drugs. "
                    "This helps build a comprehensive analytical narrative and ensures important discoveries are documented."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "finding": {"type": "string", "description": "Analysis finding about Open Targets data patterns or trends"},
                    },
                    "required": ["finding"],
                },
            ),
            types.Tool(
                name="get-insights",
                description=(
                    "Retrieve all recorded insights and findings from the current analysis session. "
                    "This tool helps you review all the key observations and patterns that have been documented."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]
        logger.debug(f"Retrieved {len(tools)} available tools")
        return tools
    async def execute_tool(self, name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
        """Execute a tool with given arguments."""
        logger.info(f"Executing tool: {name} with arguments: {arguments}")

        try:
            available_tool_names = {tool.name for tool in self.get_available_tools()}
            if name not in available_tool_names:
                logger.error(f"Unknown tool requested: {name}")
                raise ValueError(f"Unknown tool: {name}")

            if name == "list-datasets":
                datasets = self.db.allowed_datasets
                return [types.TextContent(type="text", text=str(datasets))]

            # For all other tools that require a dataset
            if name in ["list-tables", "describe-table", "read-query"]:
                dataset = arguments.get("dataset")
                if not dataset:
                    raise ValueError(f"Missing dataset argument for {name}")
                # Validate dataset before proceeding
                self.db.validate_dataset(dataset)

            if name == "list-tables":
                query = """
                    SELECT table_name
                    FROM INFORMATION_SCHEMA.TABLES
                    ORDER BY table_name;
                """
                
                rows = self.db.execute_query(query, dataset)
                tables = [row['table_name'] for row in rows]
                return [types.TextContent(type="text", text=str(tables))]

            elif name == "describe-table":
                table_name = arguments.get("table_name")
                if not table_name:
                    raise ValueError("Missing table_name argument")

                query = """
                    SELECT column_name, data_type, is_nullable
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE table_name = @table_name
                    ORDER BY ordinal_position;
                """
                
                rows = self.db.execute_query(query, dataset, {"table_name": table_name})
                columns = [
                    {
                        "column_name": row['column_name'],
                        "data_type": row['data_type'],
                        "is_nullable": row['is_nullable'],
                    }
                    for row in rows
                ]
                return [types.TextContent(type="text", text=str(columns))]

            elif name == "read-query":
                query = arguments.get("query", "").strip()
                if not query:
                    raise ValueError("Missing query argument")

                # Additional validation for the query
                self.db.validate_query_datasets(query)
                rows = self.db.execute_query(query, dataset)
                return [types.TextContent(type="text", text=str(rows))]

            elif name == "append-insight":
                if "finding" not in arguments:
                    logger.error("Missing finding argument for append-insight")
                    raise ValueError("Missing finding argument")

                finding = arguments["finding"]
                logger.debug(f"Adding insight: {finding[:50]}...")
                self.memo_manager.add_insights(finding)
                logger.info("Insight added successfully")
                return [types.TextContent(type="text", text="Insight added")]

            elif name == "get-insights":
                insights = self.memo_manager.get_insights()
                if not insights:
                    return [types.TextContent(type="text", text="No insights have been recorded yet.")]
                formatted_insights = "\n\nRecorded Insights:\n" + "\n".join(f"- {insight}" for insight in insights)
                return [types.TextContent(type="text", text=formatted_insights)]


        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
            raise

