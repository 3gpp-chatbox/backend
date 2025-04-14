const fs = require("fs");
const path = require("path");

// Escape text for Mermaid nodes
function escapeNodeText(text) {
  return text.replace(/\(/g, "\\(").replace(/\)/g, "\\)").replace(/"/g, "&quot;");
}

// Escape text for Mermaid edge labels
function escapeEdgeText(text) {
  return text.replace(/\(/g, "&#40;").replace(/\)/g, "&#41;").replace(/"/g, "&quot;");
}

function convertJsonToMermaid(inputFile, outputFile) {
  // Load JSON data
  const rawData = fs.readFileSync(inputFile, "utf-8");
  const graphData = JSON.parse(rawData);

  let mermaidCode = "```mermaid\ngraph TD;\n";

  // Add nodes
  const nodeMap = {};
  graphData.graph.nodes.forEach(node => {
    const nodeId = node.id;
    const description = escapeNodeText(node.description);
    nodeMap[nodeId] = description;
    mermaidCode += `  ${nodeId}["${description}"];\n`;
  });

  // Add edges
  graphData.graph.edges.forEach(edge => {
    const fromNode = edge.from;
    const toNode = edge.to;
    const edgeLabel = escapeEdgeText(edge.description);
    mermaidCode += `  ${fromNode} -->|${edgeLabel}| ${toNode};\n`;
  });

  mermaidCode += "```\n";

  // Write output to file
  fs.writeFileSync(outputFile, mermaidCode, "utf-8");
  console.log(`Mermaid diagram saved to ${outputFile}`);
}

// Default run if script is executed directly
if (require.main === module) {
  const inputFile = "v1-step4-enrich.json";
  const outputFile = "test_converteroutput-lea.md";
  convertJsonToMermaid(inputFile, outputFile);
}
