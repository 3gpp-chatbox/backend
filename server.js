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

// API to fetch jsonData from Neo4j based on procedure type
app.get('/fetch-jsondata/:procedureType', async (req, res) => {
    const session = driver.session();
    const { procedureType } = req.params;
    
    console.log(`Fetching data for step: ${procedureType}`);
    
    try {
        console.log('Executing Neo4j query...');
        const result = await session.run(`
            MATCH (source)-[r]->(dest)
            WHERE r.procedure = 'Initial_Registration'
            WITH source, dest, r
            ORDER BY r.step
            WITH COLLECT(DISTINCT source) + COLLECT(DISTINCT dest) AS nodes,
                 COLLECT(DISTINCT r) AS edges
            RETURN { nodes: nodes, edges: edges } AS jsonData;
        `);

        // Get the raw data
        const rawData = result.records[0]?.get('jsonData');

        if (!rawData) {
            console.log('No message flow data found');
            return res.status(404).json({ 
                error: `No message flow data found` 
            });
        }

        console.log('Raw data from Neo4j:');
        console.log('Nodes:', rawData.nodes.length);
        console.log('Edges:', rawData.edges.length);
        console.log('Sample node:', rawData.nodes[0]?.properties);
        console.log('Sample edge:', rawData.edges[0]?.properties);

        // Transform the data into the expected format
        const transformedData = {
            nodes: rawData.nodes.map(node => ({
                id: node.identity.toString(),
                label: node.properties.name || node.labels[0],
                type: node.labels[0],
                description: node.properties.description || ''
            })),
            edges: rawData.edges.map(edge => {
                const edgeData = {
                    source: edge.start.toString(),
                    target: edge.end.toString(),
                    label: edge.properties.message || edge.properties.step_name || edge.type,
                    type: edge.type,
                    properties: edge.properties
                };
                console.log('Transformed edge:', edgeData);
                return edgeData;
            })
        };

        console.log('Successfully transformed data:');
        console.log('Total nodes:', transformedData.nodes.length);
        console.log('Total edges:', transformedData.edges.length);

        res.json(transformedData);
    } catch (error) {
        console.error('Error fetching data from Neo4j:', error);
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
