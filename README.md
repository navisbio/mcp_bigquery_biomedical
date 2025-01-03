# MCP BigQuery Biomedical Server

## Overview

A Model Context Protocol (MCP) server implementation that provides access to Google BigQuery biomedical datasets, starting with **OpenTargets**. While other bigquery MCP servers exist, we decided to build a dedicated MCP server for specific datasets to help the MCP client find the right information faster and provide the right context for biopharma specific questions. 

Note that this is work in progress and that the MCP itself is still in its very early days, so you can expect changes over the next weeks. 

You will need a Google Cloud account and set up a service account with access to the BigQuery datasets. 

## Components

### Resources

The server exposes the following resources:

- `memo://insights`: **Insights on Target Assessment**  
  *A memo for the LLM to store information on the analysis. Of note, Claude does not seem to use this at the moment unless we explicitly define tools for it (which can make it overuse this capacity and therefore we removed explicit tools for resource access). We assume that future MCP clients will have better tool use (and are also working on our own client) but it does not have much impact for the moment.*

- `schema://database`: **OpenTargets Database Schema**  
  *Detailed structural information about the OpenTargets database, including column names and a short table description. This helps the network to plan queries without the need of exploring the database itself.*

### Tools

The server offers several core tools:

#### Query Tools

- `list-datasets`
  - List all available BigQuery public datasets that can be queried
  - **Input:** None required
  - **Returns:** List of available datasets

- `read-query`
  - Execute `SELECT` queries on the specified BigQuery public dataset
  - **Input:**
    - `dataset` (string): Name of the BigQuery dataset to query
    - `query` (string): The `SELECT` SQL query to execute
  - **Returns:** Query results as JSON array of objects

#### Schema Tools

- `list-tables`
  - Get a list of all tables in the specified BigQuery dataset
  - **Input:**
    - `dataset` (string): Name of the BigQuery dataset to explore
  - **Returns:** List of table names

- `describe-table`
  - View schema information for a specific table
  - **Input:**
    - `dataset` (string): Name of the BigQuery dataset containing the table
    - `table_name` (string): Name of table to describe
  - **Returns:** Column definitions with names, types, and nullability

#### Analysis Tools

- `append-insight`
  - Add new findings to the analysis memo
  - **Input:**
    - `finding` (string): Analysis finding about patterns or trends
  - **Returns:** Confirmation of finding addition

- `get-insights`
  - Retrieve all recorded insights from the current session
  - **Input:** None required
  - **Returns:** List of all recorded insights

## Environment Variables

The server requires the following environment variables:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account key file
- `ALLOWED_DATASETS`: Comma-separated list of allowed BigQuery datasets, e.g.:
  ```
  ALLOWED_DATASETS=open_targets_platform,open_targets_genetics,human_genome_variants,gnomad
  ```

Example `.env` file:
```env
GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/service-account-key.json'
ALLOWED_DATASETS=open_targets_platform,open_targets_genetics,human_genome_variants,gnomad
```

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
        "BIGQUERY_CREDENTIALS": "PATH_TO_YOUR_SERVICE_ACCOUNT_KEY.json",
        "ALLOWED_DATASETS": "open_targets_platform,open_targets_genetics,human_genome_variants,gnomad" # or any other dataset name you want to work with 
      }
    }
}
```
You can check the public datasets in open targets for a comprehensive list, but some of the biomedical datasets are:

- open_targets_platform
- open_targets_genetics 
- ebi_chembl
- ebi_surechembl
- fda_drug
- deepmind_alphafold
- human_genome_variants
- human_variant_annotation
- immune_epitope_db
- cms_medicare
- patents
- patents_view
- patents_cpc
- google_patents_research
- uspto_oce_cancer
- patents_dsep
- ebi_mgnify
- human_genome_variants
- gnomad

Note, that many of these have not been updated for a year or two in the public bigquery database. We are building our own databases for AI supported translational research, so if you need more up to data information, please reach out to us at [jonas.walheim@navis-bio.com](mailto:jonas.walheim@navis-bio.com)

## Currently Supported Datasets

The server supports access to all BigQuery public datasets. The database resource has only been created for the **OpenTargets** datasets, but Claude also works well if no database description is provided. You can easily add one for another dataset and create a pull request.

## Contact

Happy to hear from you if you have suggestions, questions, or feedback [jonas.walheim@navis-bio.com](mailto:jonas.walheim@navis-bio.com)

## License

This MCP server is licensed under the GNU General Public License v3.0 (GPL-3.0). This means you have the freedom to run, study, share, and modify the software. Any modifications or derivative works must also be distributed under the same GPL-3.0 terms. For more details, please see the LICENSE file in the project repository.
