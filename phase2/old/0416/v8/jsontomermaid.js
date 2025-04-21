const fs = require('fs');
const path = require('path');

function convertJsonToMermaid(inputFile, outputFile) {
    try {
        console.log(`Starting conversion...`);
        
        // Verify file paths
        const inputPath = path.resolve(inputFile);
        const outputPath = path.resolve(outputFile);
        console.log(`Input file: ${inputPath}`);
        console.log(`Output file: ${outputPath}`);

        // Check if input file exists
        if (!fs.existsSync(inputPath)) {
            throw new Error(`Input file not found at: ${inputPath}`);
        }

        // Read and parse JSON
        console.log(`Reading input file...`);
        const rawData = fs.readFileSync(inputPath, 'utf-8');
        const graphData = JSON.parse(rawData);

        // Validate structure
        if (!Array.isArray(graphData.nodes) || !Array.isArray(graphData.edges)) {
            throw new Error('Invalid JSON structure: nodes and edges must be arrays');
        }

        console.log(`Found ${graphData.nodes.length} nodes and ${graphData.edges.length} edges`);

        // Initialize Mermaid diagram with LR (Left-to-Right) orientation
        let mermaidCode = "graph LR\n";
        mermaidCode += "    classDef state fill:#f9f,stroke:#333,stroke-width:2px;\n";
        mermaidCode += "    classDef event fill:#bbf,stroke:#333,stroke-width:2px;\n\n";

        // Process nodes - using name as primary identifier
        const nodeMap = {};
        graphData.nodes.forEach(node => {
            if (!node.id || !node.name) {
                console.warn(`Skipping malformed node: ${JSON.stringify(node)}`);
                return;
            }
            nodeMap[node.name] = node.id;
            mermaidCode += `    ${node.id}("${node.name}")\n`;
            // You can add class assignment here if you have types
            // mermaidCode += `    class ${node.id} state\n`;
        });

        // Process edges
        graphData.edges.forEach(edge => {
            if (!edge.from || !edge.to) {
                console.warn(`Skipping malformed edge: ${JSON.stringify(edge)}`);
                return;
            }

            // Find node IDs for the edge
            const fromNode = Object.keys(nodeMap).find(name => name === edge.from);
            const toNode = Object.keys(nodeMap).find(name => name === edge.to);

            if (!fromNode || !toNode) {
                console.warn(`Skipping edge with missing nodes: ${edge.from} -> ${edge.to}`);
                return;
            }

            const fromId = nodeMap[fromNode];
            const toId = nodeMap[toNode];
            const label = edge.label || '';
            const sectionRef = edge.section_reference ? ` (${edge.section_reference})` : '';

            mermaidCode += `    ${fromId} --> ${toId}\n`;
        });

        // Wrap in markdown
        const outputContent = "```mermaid\n" + mermaidCode + "```";

        // Write output
        console.log(`Writing output file...`);
        fs.writeFileSync(outputPath, outputContent, 'utf-8');
        console.log(`Successfully generated Mermaid diagram at ${outputPath}`);

    } catch (error) {
        console.error('Conversion failed:');
        console.error(error.message);
        process.exit(1);
    }
}

// Example usage with error handling
try {
    const inputFile = process.argv[2] || "step1.json";
    const outputFile = process.argv[3] || "converted-mermaid.md";
    convertJsonToMermaid(inputFile, outputFile);
} catch (err) {
    console.error("Fatal error in script execution:");
    console.error(err);
    process.exit(1);
}