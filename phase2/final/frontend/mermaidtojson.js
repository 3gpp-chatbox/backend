const fs = require("fs");

function unescapeText(text) {
  return text
    .replace(/\\\(/g, "(")
    .replace(/\\\)/g, ")")
    .replace(/&quot;/g, '"')
    .replace(/&#40;/g, "(")
    .replace(/&#41;/g, ")");
}

function convertMermaidToJson(inputFile, outputFile) {
  // Load Mermaid data
  const mermaidData = fs.readFileSync(inputFile, "utf-8");
  
  // Initialize JSON structure
  const jsonData = {
    procedure_name: "",
    graph: {
      nodes: [],
      edges: []
    }
  };

  // Split into lines and process each line
  const lines = mermaidData.split('\n');
  let currentEdge = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    
    // Skip empty lines and mermaid markers
    if (!line || line === '```mermaid' || line === '```') {
      continue;
    }

    // Extract procedure name if available
    if (line.startsWith('%% Procedure:')) {
      jsonData.procedure_name = line.replace('%% Procedure:', '').trim();
      continue;
    }

    // Process node definitions
    if (/^\w+;/.test(line)) {
      const nodeId = line.split(';')[0].trim();
      jsonData.graph.nodes.push({
        id: nodeId,
        type: '',
        description: ''
      });
      
      // Look ahead for node metadata comments
      let j = i + 1;
      while (j < lines.length && lines[j].trim().startsWith('%%')) {
        const comment = lines[j].trim();
        const node = jsonData.graph.nodes.find(n => n.id === nodeId);
        
        if (comment.startsWith('%% Type:')) {
          node.type = unescapeText(comment.replace('%% Type:', '').trim());
        } else if (comment.startsWith('%% Description:')) {
          node.description = unescapeText(comment.replace('%% Description:', '').trim());
        }
        j++;
      }
      continue;
    }

    // Process edge definitions
    const edgeMatch = line.match(/^(\w+)\s*(-+>)\s*(\w+);/);
    if (edgeMatch) {
      const fromNode = edgeMatch[1];
      const toNode = edgeMatch[3];
      currentEdge = {
        from: fromNode,
        to: toNode,
        type: '',
        description: ''
      };
      jsonData.graph.edges.push(currentEdge);
      
      // Look ahead for edge metadata comments
      let j = i + 1;
      while (j < lines.length && lines[j].trim().startsWith('%%')) {
        const comment = lines[j].trim();
        
        if (comment.startsWith('%% Type:')) {
          currentEdge.type = unescapeText(comment.replace('%% Type:', '').trim());
        } else if (comment.startsWith('%% Description:')) {
          currentEdge.description = unescapeText(comment.replace('%% Description:', '').trim());
        }
        j++;
      }
      continue;
    }

    // Handle graph declaration (ignore)
    if (line.startsWith('graph')) {
      continue;
    }
  }

  // Write output to file
  fs.writeFileSync(outputFile, JSON.stringify(jsonData, null, 2), "utf-8");
  console.log(`JSON data saved to ${outputFile}`);
}

// Example usage
const inputFile = "test_converteroutput_with_comments.md";
const outputFile = "converted_back.json";
convertMermaidToJson(inputFile, outputFile);