import logging

logger = logging.getLogger('mcp_bigquery_server.memo_manager')

class MemoManager:
    def __init__(self):
        self.insights = []
        logger.info("MemoManager initialized")

    def add_insights(self, finding: str) -> None:
        """Add a new insight or finding to the memo."""
        logger.debug(f"Adding insight: {finding[:50]}...")
        self.insights.append(finding)
        logger.info("Insight added successfully")

    def get_insights(self) -> list[str]:
        """Retrieve all recorded insights."""
        logger.debug(f"Retrieving {len(self.insights)} insights")
        return self.insights

