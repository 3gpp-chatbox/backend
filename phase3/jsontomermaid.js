const fs = require("fs");

function convertJsonToMermaid(inputFile, outputFile) {
  if (!fs.existsSync(inputFile)) {
    console.error(`Input file ${inputFile} not found!`);
    return;
  }

  const rawData = fs.readFileSync(inputFile, "utf-8");
  const procedureData = JSON.parse(rawData);
  const graphData = procedureData.graph;

  let mermaidCode = "graph LR\n";
  // Add all class definitions first
  mermaidCode += "    classDef state fill:#e6f3ff,stroke:#333,stroke-width:2px,color:#000;\n";
  mermaidCode += "    classDef action fill:#ffebee,stroke:#333,stroke-width:1px,color:#000;\n";
  mermaidCode += "    classDef condition fill:#fff9e6,stroke:#333,stroke-width:1px,color:#000;\n";
  mermaidCode += "    classDef decision fill:#e6ffe6,stroke:#333,stroke-width:1px,color:#000;\n\n";

  // Process nodes with proper formatting
  graphData.nodes.forEach(node => {
    // Handle different node shapes based on type
    let nodeShape = "";
    if (node.type === "condition" || node.type === "decision") {
      nodeShape = `{"${node.name}"}`; // Rhombus shape for conditions/decisions
    } else {
      nodeShape = `["${node.name}"]`; // Rectangle for others
    }
    
    mermaidCode += `    ${node.id}${nodeShape}\n`;
    mermaidCode += `    class ${node.id} ${node.type}\n`;
  });

  // Process edges with proper formatting
  graphData.edges.forEach(edge => {
    // Clean up label formatting
    let label = edge.label ? edge.label.replace(/"/g, '') : '';
    mermaidCode += `    ${edge.from}-->|"${label}"| ${edge.to}\n`;
  });

  // Generate the final output
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
const inputFile = "step1.json";
const outputFile = "step1.md";
convertJsonToMermaid(inputFile, outputFile);