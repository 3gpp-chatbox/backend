const fs = require("fs");

function convertJsonToMermaid(inputFile, outputFile) {
  if (!fs.existsSync(inputFile)) {
    console.error(`Input file ${inputFile} not found!`);
    return;
  }

  const rawData = fs.readFileSync(inputFile, "utf-8");
  const procedureData = JSON.parse(rawData);
  const graphData = procedureData.graph; // Access the graph object from your new structure

  let mermaidCode = "graph LR\n";  // Left-to-right flow for better readability
  mermaidCode += "    classDef state fill:#e6f3ff,stroke:#333,stroke-width:2px,color:#000;\n";
  mermaidCode += "    classDef event fill:#ffebee,stroke:#333,stroke-width:1px,color:#000;\n\n";

  // Process nodes
  graphData.nodes.forEach(node => {
    const nodeId = node.id;
    const nodeName = node.name;
    const nodeType = node.type || 'state'; // Default to state if type not specified
    
    // Add nodes with styling based on type
    mermaidCode += `    ${nodeId}["${nodeName}"]\n`;
    mermaidCode += `    class ${nodeId} ${nodeType}\n`;
  });

  // Process edges with better label formatting
  graphData.edges.forEach(edge => {
    const fromNode = graphData.nodes.find(n => n.id === edge.from)?.name || edge.from;
    const toNode = graphData.nodes.find(n => n.id === edge.to)?.name || edge.to;
    let label = edge.label || '';
    
    // Clean up label formatting
    if (label.startsWith("Condition: ")) {
      label = label.substring("Condition: ".length);
    }
    
    // Add section reference if available
    if (edge.section_reference) {
      label += ` (${edge.section_reference})`;
    }

    // Add the edge with proper quoting
    mermaidCode += `    ${fromNode} -->|"${label}"| ${toNode}\n`;
  });

  // Add title if procedure_name exists
  let outputContent = "";
  if (procedureData.procedure_name) {
    outputContent += `# ${procedureData.procedure_name}\n\n`;
  }
  outputContent += "```mermaid\n" + mermaidCode + "```";

  // Write the output file
  fs.writeFileSync(outputFile, outputContent, "utf-8");
  console.log(`Mermaid diagram saved to ${outputFile}`);
}

// Example usage
const inputFile = "step2.json";
const outputFile = "step2-converted-mermaid.md";
convertJsonToMermaid(inputFile, outputFile);