const fs = require("fs");

function convertJsonToMermaid(inputFile, outputFile) {
  if (!fs.existsSync(inputFile)) {
    console.error(`Input file ${inputFile} not found!`);
    return;
  }

  const rawData = fs.readFileSync(inputFile, "utf-8");
  const graphData = JSON.parse(rawData);

  let mermaidCode = "graph TD\n";  // Initialize Mermaid code for flowchart

  // Process nodes (both states and events)
  graphData.nodes.forEach(node => {
    let nodeId = node.id;
    let description = node.properties.description || '';

    // Add nodes to the Mermaid diagram
    if (node.type === 'state' || node.type === 'event') {
      mermaidCode += `    ${nodeId}\n`;

    }
  });

// Process edges
graphData.edges.forEach(edge => {
  let fromState = edge.from;
  let toState = edge.to;

  let action = edge.action || '';
  let condition = edge.condition || '';

  // Use action as label, if action is missing use condition
  let label = action || condition;

  // Add the edge (transition) between nodes to the Mermaid diagram
  mermaidCode += `    ${fromState} -->|"${label}"| ${toState}\n`;
});

  // Wrap the Mermaid code in markdown syntax for Mermaid rendering
  mermaidCode = "```mermaid\n" + mermaidCode + "```";

  // Write the Mermaid code to the output file
  fs.writeFileSync(outputFile, mermaidCode, "utf-8");
  console.log(`Mermaid diagram saved to ${outputFile}`);
}

// Example usage
const inputFile = "step1-v2.json"; // Absolute path
const outputFile = "converted-mermaid-v2.md";  // Output file path
convertJsonToMermaid(inputFile, outputFile);

