const fs = require("fs");

function escapeNodeText(text) {
  return text.replace(/\(/g, "\\(").replace(/\)/g, "\\)").replace(/"/g, "&quot;");
}

function escapeEdgeText(text) {
  return text.replace(/\(/g, "&#40;").replace(/\)/g, "&#41;").replace(/"/g, "&quot;");
}

function convertJsonToMermaid(inputFile, outputFile) {
  const rawData = fs.readFileSync(inputFile, "utf-8");
  const graphData = JSON.parse(rawData);

  let mermaidCode = "```mermaid\ngraph TD;\n";

  if (graphData.procedure_name) {
    mermaidCode += `  %% Procedure: ${graphData.procedure_name}\n`;
  }

  const nodeIdMap = {};
  const allNodes = graphData.graph.nodes.map(node => node.id);
  const labelLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let labelIndex = 0;

  // Extend label system to AA, AB, etc., if we run out of single letters
  function getNextLabel() {
    let label = "";
    let index = labelIndex;
    do {
      label = labelLetters[index % 26] + label;
      index = Math.floor(index / 26) - 1;
    } while (index >= 0);
    labelIndex++;
    return label;
  }

  // Assign labels and print node definitions
  graphData.graph.nodes.forEach(node => {
    const label = getNextLabel();
    nodeIdMap[node.id] = label;
    const labelText = escapeNodeText(node.id);
    mermaidCode += `  ${label}(${labelText});\n`;
  });

  // Add edges using mapped labels
  graphData.graph.edges.forEach(edge => {
    const from = nodeIdMap[edge.from] || edge.from;
    const to = nodeIdMap[edge.to] || edge.to;
    mermaidCode += `  ${from} --> ${to};\n`;
  });

  mermaidCode += "```";

  fs.writeFileSync(outputFile, mermaidCode, "utf-8");
  console.log(`Mermaid diagram saved to ${outputFile}`);
}

// Example usage
const inputFile = "v1-step4-enrich.json";
const outputFile = "converted-mermaid.md";
convertJsonToMermaid(inputFile, outputFile);
