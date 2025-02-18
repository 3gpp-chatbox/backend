import json
from dataclasses import dataclass
from typing import List, Dict, Optional
import re

@dataclass
class Section:  
    level: int
    heading: str
    content: List[Dict[str, str]]
    subsections: List['Section']
    parent: Optional['Section'] = None

    def __str__(self): 
        return f"Level: {self.level}, Heading: {self.heading}"

    @classmethod
    def from_dict(cls, data): 
        section = cls(
            level=data['level'],
            heading=data['heading'],
            content=data['content'],
            subsections=[cls.from_dict(subsection) for subsection in data.get('subsections', [])],
            parent=None 
        )
        for subsection in section.subsections:
            subsection.parent = section
        return section

def extract_nas_nr_data(sections: List[Section], target_procedure: str) -> Dict[str, any]:
    """Extract nodes and edges related to a specific NAS NR procedure."""
    nodes = {}
    edges = []

    for section in sections:
        for item in section.content:
            text = item.strip()
            if text:
                if target_procedure.lower() in text.lower():
                    # Entity extraction
                    for entity_match in re.finditer(r"\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b", text):
                        entity_name = entity_match.group(0).strip()
                        if entity_name not in nodes:
                            nodes[entity_name] = {"label": "Entity", "properties": {}}

                            property_matches = re.finditer(r"(\w+)\s*:\s*([^.,;]+)", text)
                            for prop_match in property_matches:
                                key = prop_match.group(1).strip()
                                value = prop_match.group(2).strip()
                                nodes[entity_name]["properties"][key] = value

                    # Relationship extraction
                    for rel_match in re.finditer(r"(\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b)\s+(?:is related to|depends on|requires|connected to|sends|receives|uses|supports)\s+(\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b)", text):
                        source = rel_match.group(1).strip()
                        target = rel_match.group(2).strip()
                        relation_type = rel_match.group(0).strip().split()[1]

                        if source in nodes and target in nodes:
                            edges.append({
                                "source": source,
                                "target": target,
                                "type": relation_type,
                                "properties": {}
                            })

    return {"nodes": nodes, "edges": edges}


# Load the structured data from the JSON file:
with open("document_sections.json", "r", encoding="utf-8") as f:
    sections_data = json.load(f)

# Recreate the Section objects from the loaded dictionaries:
sections = [Section.from_dict(section_data) for section_data in sections_data]

target_procedure = "Your Specific Procedure Name"  # Replace with the actual procedure name
graph_data = extract_nas_nr_data(sections, target_procedure)

# Convert nodes dictionary to a list of nodes for JSON serialization:
nodes_list = [{"id": identifier, "label": data["label"], "properties": data["properties"]} for identifier, data in graph_data["nodes"].items()]

# Combine nodes and edges into a single dictionary:
graph_data_for_json = {"nodes": nodes_list, "edges": graph_data["edges"]}

# Save to JSON:
with open("nas_nr_graph.json", "w", encoding="utf-8") as f:
    json.dump(graph_data_for_json, f, indent=4)

print("NAS NR graph data saved to nas_nr_graph.json")