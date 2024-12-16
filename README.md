# MCP BigQuery Biomedical Server

## Overview

A Model Context Protocol (MCP) server implementation that provides access to Google BigQuery biomedical datasets, starting with **OpenTargets**. While other bigquery MCP servers exist, we decided to build a dedicated MCP server for specific datasets to help the MCP client find the right information faster and provide the right context for biopharma specific questions. 

## Components

### Resources

The server exposes the following resources:

- `memo://insights`: **Insights on Target Assessment**  
  *A memo for the LLM to store information on the analysis.*

- `schema://database`: **OpenTargets Database Schema**  
  *Detailed structural information about the OpenTargets database, including column names and a short table description. This helps the network to plan queries without the need of exploring the database itself.*

### Tools

The server offers several core tools:

#### Query Tools

- `read-query`
  - Execute `SELECT` queries on the BigQuery biomedical datasets
  - **Input:**
    - `query` (string): The `SELECT` SQL query to execute
  - **Returns:** Query results as JSON array of objects

#### Schema Tools

- `list-tables`
  - Get a list of all tables in the BigQuery dataset
  - **Input:** None required
  - **Returns:** List of table names

- `describe-table`
  - View schema information for a specific table
  - **Input:**
    - `table_name` (string): Name of table to describe
  - **Returns:** Column definitions with names, types, and nullability

#### Analysis Tools

- `append-analysis`
  - Add new findings to the analysis memo
  - **Input:**
    - `finding` (string): Analysis finding about patterns or trends
  - **Returns:** Confirmation of finding addition

### Prompt Template

We provide a prompt template defined in `prompts.py` to guide bioinformatics analyses using the OpenTargets dataset. This can be helpful in guiding the LLM in its exploration. If you have suggestions for predefined workflows, let us know!


## Environment Variables

The server requires the following environment variables:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account key file
- `PROJECT_ID`: Your Google Cloud project ID

## Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json:claude_desktop_config.json
"mcpServers": {
    "BIGQUERY-BIOMEDICAL-MCP": {
      "command": "python",
      "args": [
        "-m",
        "mcp_bigquery_biomedical"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "PATH_TO_YOUR_SERVICE_ACCOUNT_KEY.json",
        "PROJECT_ID": "YOUR_GOOGLE_CLOUD_PROJECT_ID"
      }
    }
}

## Roadmap & Contribution

We start with support for **OpenTargets** datasets and plan to include additional BigQuery biomedical datasets in the future. Over the coming weeks and months, we will expand support to include:

- **Additional BigQuery biomedical datasets**
- ChEMBL: Bioactive molecules and drug-like compounds
- TCGA: Cancer genomics data
- And more to come!

We warmly welcome contributions of all kinds! Happy to hear from you if you:

- Have specific use cases you'd like to explore
- Need customizations for your research
- Want to suggest additional datasets
- Are interested in contributing code, documentation, or ideas
- Want to improve existing features

Please reach out by:

- Opening an issue on GitHub
- Starting a discussion in our repository
- Emailing us at [jonas.walheim@navis-bio.com](mailto:jonas.walheim@navis-bio.com)
- Submitting pull requests

Your feedback helps shape our development priorities.


## License

This MCP server is licensed under the GNU General Public License v3.0 (GPL-3.0). This means you have the freedom to run, study, share, and modify the software. Any modifications or derivative works must also be distributed under the same GPL-3.0 terms. For more details, please see the LICENSE file in the project repository.
