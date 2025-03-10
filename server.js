require('dotenv').config();
const express = require('express');
const neo4j = require('neo4j-driver');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Neo4j Connection
const driver = neo4j.driver(
    process.env.NEO4J_URI || 'bolt://localhost:7687',
    neo4j.auth.basic(
        process.env.NEO4J_USERNAME || 'neo4j', 
        process.env.NEO4J_PASSWORD || 'password'
    ),
    {
        encrypted: process.env.NEO4J_ENCRYPTED === 'true' || false,
        trust: 'TRUST_ALL_CERTIFICATES'
    }
);

// Test Neo4j connection
async function testConnection() {
    const session = driver.session();
    try {
        const result = await session.run('MATCH (n) RETURN count(n) as count');
        console.log('Successfully connected to Neo4j');
        console.log(`Database contains ${result.records[0].get('count')} nodes`);
    } catch (error) {
        console.error('Failed to connect to Neo4j:', error);
    } finally {
        await session.close();
    }
}

testConnection();

app.use(cors());
app.use(express.json());

// API to fetch procedure data (Initial Registration or Periodic Registration)
app.get('/fetch-jsondata/:procedureType', async (req, res) => {
    const session = driver.session();
    const { procedureType } = req.params;
    
    // Validate procedure type
    const validProcedures = ['Initial_Registration', 'Periodic_Registration'];
    if (!validProcedures.includes(procedureType)) {
        return res.status(400).json({
            error: `Invalid procedure type. Must be one of: ${validProcedures.join(', ')}`
        });
    }
    
    console.log(`Fetching ${procedureType} procedure...`);
    
    try {
        console.log('Executing Neo4j query...');
        const result = await session.run(`
            MATCH (source)-[r]->(dest)
            WHERE r.procedure = $procedureType
            WITH source, dest, r
            ORDER BY r.sequence_number
            WITH COLLECT(DISTINCT source) + COLLECT(DISTINCT dest) AS nodes,
                 COLLECT(DISTINCT r) AS edges
            RETURN { nodes: nodes, edges: edges } AS jsonData;
        `, { procedureType });  // Pass procedureType as parameter

        const rawData = result.records[0]?.get('jsonData');

        if (!rawData) {
            console.log(`No ${procedureType} flow data found`);
            return res.status(404).json({ 
                error: `No ${procedureType} flow data found` 
            });
        }

        // Transform the data into the expected format
        const transformedData = {
            nodes: rawData.nodes.map(node => ({
                id: node.identity.toString(),
                label: node.properties.name || node.labels[0],
                type: node.labels[0],
                description: node.properties.description || ''
            })),
            edges: rawData.edges.map(edge => ({
                source: edge.start.toString(),
                target: edge.end.toString(),
                label: edge.properties.message || edge.properties.step_name || edge.type,
                type: edge.type,
                properties: edge.properties
            }))
        };

        console.log(`Successfully transformed ${procedureType} data:`);
        console.log('Total nodes:', transformedData.nodes.length);
        console.log('Total edges:', transformedData.edges.length);

        res.json(transformedData);
    } catch (error) {
        console.error(`Error fetching ${procedureType} data:`, error);
        res.status(500).json({ 
            error: 'Internal Server Error',
            message: error.message,
            stack: error.stack
        });
    } finally {
        await session.close();
    }
});

// Add a test endpoint to verify Neo4j connection
app.get('/test-connection', async (req, res) => {
    const session = driver.session();
    try {
        const result = await session.run('MATCH (n) RETURN count(n) as count');
        res.json({
            status: 'success',
            nodeCount: result.records[0].get('count').toNumber()
        });
    } catch (error) {
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    } finally {
        await session.close();
    }
});

// API to fetch complete Initial Registration procedure flow
app.get('/registration-procedure', async (req, res) => {
    const session = driver.session();
    
    console.log('Fetching Initial Registration procedure...');
    
    try {
        const result = await session.run(`
            MATCH (source)-[r:SENDS_MESSAGE]->(target)
            WHERE r.procedure = 'Initial_Registration'
            WITH source, r, target
            ORDER BY r.sequence_number
            RETURN {
                step: r.sequence_number,
                source: source.name,
                target: target.name,
                message: r.message,
                description: r.description,
                sourceState: r.source_state,
                targetState: r.target_state,
                trigger: r.trigger,
                conditions: r.conditions,
                timing: r.timing
            } as step
            ORDER BY step.step
        `);

        const procedureFlow = result.records.map(record => record.get('step'));

        res.json({
            status: 'success',
            data: {
                procedure: 'Initial_Registration',
                total_steps: procedureFlow.length,
                procedure_flow: procedureFlow
            }
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: error.message
        });
    } finally {
        await session.close();
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

process.on('exit', () => {
    driver.close();
});
