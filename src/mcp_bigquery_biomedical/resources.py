from typing import TypedDict
from pydantic import AnyUrl
import mcp.types as types

class ResourceDefinition(TypedDict):
    uri: str
    name: str
    description: str
    mimeType: str

OPENTARGETS_RESOURCES: list[ResourceDefinition] = [
    {
        "uri": "memo://insights",
        "name": "Insights on Target Assessment",
        "description": "Comprehensive analysis repository capturing key findings about drug targets, disease associations, genetic evidence, and therapeutic potential. This living document grows with each discovered insight to build a complete target validation overview.",
        "mimeType": "text/plain",
    },
    {
        "uri": "schema://database",
        "name": "OpenTargets Database Schema",
        "description": "Detailed structural information about the OpenTargets database, including table relationships, column definitions, and data types. Essential reference for understanding genomic data organization and planning effective queries.",
        "mimeType": "application/json",
    }
]
def get_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=AnyUrl(resource["uri"]),
            name=resource["name"],
            description=resource["description"],
            mimeType=resource["mimeType"],
        )
        for resource in OPENTARGETS_RESOURCES
    ] 