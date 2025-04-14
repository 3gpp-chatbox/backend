const fs = require("fs");


function escapeNodeText(text) {
  return text.replace(/\(/g, "\\(").replace(/\)/g, "\\)").replace(/"/g, "&quot;");
}

function escapeEdgeText(text) {
  return text.replace(/\(/g, "&#40;").replace(/\)/g, "&#41;").replace(/"/g, "&quot;");
}

function convertJsonToMermaid(inputFile, outputFile) {
  // Load JSON data
  const rawData = fs.readFileSync(inputFile, "utf-8");
  const graphData = JSON.parse(rawData);

  let mermaidCode = "```mermaid\ngraph TD;\n";

  // Add procedure name as a comment
  if (graphData.procedure_name) {
    mermaidCode += `  %% Procedure: ${graphData.procedure_name}\n`;
  }

  // Add nodes with comments for extra metadata
  graphData.graph.nodes.forEach(node => {
    const nodeId = node.id;
    const description = escapeNodeText(node.description);
    mermaidCode += `  ${nodeId};\n`;
    // Add comments for 'type' and 'description'
    mermaidCode += `  %% Type: ${node.type}\n`;
    mermaidCode += `  %% Description: ${node.description}\n`;
  });

  // Add edges with comments for extra metadata
  graphData.graph.edges.forEach(edge => {
    const fromNode = edge.from;
    const toNode = edge.to;
    const edgeLabel = escapeEdgeText(edge.description);
    mermaidCode += `  ${fromNode} -->${toNode};\n`;
    // Add comments for edge type and description
    mermaidCode += `  %% Type: ${edge.type}\n`;
    mermaidCode += `  %% Description: ${edge.description}\n`;
  });

  mermaidCode += "```\n";

  // Write output to file
  fs.writeFileSync(outputFile, mermaidCode, "utf-8");
  console.log(`Mermaid diagram saved to ${outputFile}`);
}

// Example usage
const inputFile = "v1-step4-enrich.json";
const outputFile = "test_converteroutput_with_comments.md";
convertJsonToMermaid(inputFile, outputFile);
