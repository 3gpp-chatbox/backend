const fs = require('fs');

function parseMermaidComments(mermaidCode) {
  const lines = mermaidCode.split("\n");
  const graphData = { nodes: [], edges: [] };

  let currentNode = null;
  let currentEdge = null;

  lines.forEach(line => {
    // Look for node definitions and capture comments
    if (line.includes('["') && line.includes('"]')) {
      const nodeId = line.split('["')[0].trim();
      const description = line.split('["')[1].split('"]')[0].trim();
      currentNode = { id: nodeId, description };
      graphData.nodes.push(currentNode);
    }

    if (line.startsWith("%%")) {
      // Extract type and description from comments for nodes
      const comment = line.split(": ");
      if (comment[0] === "%% Type") {
        if (currentNode) {
          currentNode.type = comment[1].trim();
        }
      } else if (comment[0] === "%% Description") {
        if (currentNode) {
          currentNode.description = comment[1].trim();
        }
      }
    }

    // Extract edges with comments
    if (line.includes("-->")) {
      const [fromNode, toNode] = line.split(" -->|")[0].split(" --> ");
      const label = line.split("|")[1] || "";

      currentEdge = { from: fromNode, to: toNode, description: label.trim() };

      // Look for edge comments for additional info
      lines.forEach(edgeLine => {
        if (edgeLine.includes("%%") && edgeLine.includes(fromNode) && edgeLine.includes(toNode)) {
          if (edgeLine.includes("%% Type")) {
            const edgeType = edgeLine.split(": ")[1].trim();
            currentEdge.type = edgeType;
          }
          if (edgeLine.includes("%% Description")) {
            const edgeDescription = edgeLine.split(": ")[1].trim();
            currentEdge.description = edgeDescription;
          }
        }
      });

      graphData.edges.push(currentEdge);
    }
  });

  return graphData;
}

// Example usage: Parsing saved Mermaid code with comments
const mermaidCode = fs.readFileSync('test_converteroutput_with_comments.md', 'utf-8');
const parsedGraphData = parseMermaidComments(mermaidCode);

// Save the parsed JSON to a file
const outputFile = 'mermaidtojson.json';
fs.writeFileSync(outputFile, JSON.stringify(parsedGraphData, null, 2), 'utf-8');
console.log(`Converted JSON saved to ${outputFile}`);
