const fs = require("fs");

function convertMermaidToJson(inputFile, outputFile) {
  const mermaidData = fs.readFileSync(inputFile, "utf-8");
  const lines = mermaidData.split("\n");

  const jsonOutput = {
    procedure_name: "",
    graph: {
      nodes: [],
      edges: []
    }
  };

  const labelToIdMap = {};
  let lastElementType = null; // "node" or "edge"
  let lastElementRef = null;

  const procedureLine = lines.find(line => line.includes("%% Procedure:"));
  if (procedureLine) {
    jsonOutput.procedure_name = procedureLine.split("%% Procedure:")[1].trim();
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Match node: A(UE_Deregistered);
    const nodeMatch = line.match(/^([A-Z]+)\(([^()]+)\);/);
    if (nodeMatch) {
      const [_, label, id] = nodeMatch;
      labelToIdMap[label] = id;
      const node = { id, type: "", description: "" };
      jsonOutput.graph.nodes.push(node);
      lastElementType = "node";
      lastElementRef = node;
      continue;
    }

    // Match edge: A --> B;
    const edgeMatch = line.match(/^([A-Z]+) --> ([A-Z]+);/);
    if (edgeMatch) {
      const [_, fromLabel, toLabel] = edgeMatch;
      const from = labelToIdMap[fromLabel] || fromLabel;
      const to = labelToIdMap[toLabel] || toLabel;
      const edge = { from, to, type: "", description: "" };
      jsonOutput.graph.edges.push(edge);
      lastElementType = "edge";
      lastElementRef = edge;
      continue;
    }

    // Match Type
    const typeMatch = line.match(/^%% Type:\s*(.+)$/);
    if (typeMatch && lastElementRef) {
      lastElementRef.type = typeMatch[1].trim();
      continue;
    }

    // Match Description
    const descMatch = line.match(/^%% Description:\s*(.+)$/);
    if (descMatch && lastElementRef) {
      lastElementRef.description = descMatch[1].trim();
      continue;
    }
  }

  fs.writeFileSync(outputFile, JSON.stringify(jsonOutput, null, 2), "utf-8");
  console.log(`✅ JSON output saved to ${outputFile}`);
}

// Example usage
const inputFile = "converted-mermaid.md";
const outputFile = "reversed-json.json";
convertMermaidToJson(inputFile, outputFile);
