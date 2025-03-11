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

// API to fetch Change in RAT procedure path
app.get('/periodic-registration/change-in-rat-path', async (req, res) => {
    const session = driver.session();
    
    console.log('Fetching Change in RAT procedure path...');
    
    try {
        // First verify if we can find any matching relationships
        const verifyResult = await session.run(`
            MATCH (source:NetworkElement)-[r:SENDS_MESSAGE]->(target:NetworkElement)
            WHERE r.procedure = 'Periodic_Registration'
            AND r.trigger = 'Change in RAT'
            RETURN COUNT(r) as count
        `);
        
        const count = verifyResult.records[0].get('count').toNumber();
        console.log(`Found ${count} matching relationships`);

        if (count === 0) {
            return res.status(404).json({
                status: 'error',
                error: 'No procedure steps found for Change in RAT trigger'
            });
        }

        console.log('Executing main query...');
        const result = await session.run(`
            MATCH (source:NetworkElement)-[r:SENDS_MESSAGE]->(target:NetworkElement)
            WHERE r.procedure = 'Periodic_Registration'
            AND r.trigger = 'Change in RAT'
            RETURN {
                step: r.sequence_number,
                source: {
                    name: source.name,
                    type: source.type,
                    description: source.description
                },
                target: {
                    name: target.name,
                    type: target.type,
                    description: target.description
                },
                message: r.message,
                description: r.description,
                messageType: r.message_type,
                conditions: CASE 
                    WHEN r.conditions IS NULL THEN []
                    ELSE r.conditions 
                END,
                parameters: CASE 
                    WHEN r.parameters IS NULL THEN []
                    ELSE r.parameters 
                END,
                outcome: r.outcome,
                trigger: r.trigger
            } as step
            ORDER BY r.sequence_number
        `);

        console.log('Query executed, processing results...');
        const procedureSteps = result.records.map(record => record.get('step'));
        console.log(`Found ${procedureSteps.length} steps in the procedure`);
        console.log('First step:', JSON.stringify(procedureSteps[0], null, 2));

        console.log('Sending response...');
        res.json({
            status: 'success',
            data: {
                procedure: 'Periodic Registration',
                trigger: 'Change in RAT',
                description: 'Periodic registration procedure triggered by Radio Access Technology change',
                total_steps: procedureSteps.length,
                procedure_flow: procedureSteps,
                timestamp: new Date().toISOString()
            }
        });
        console.log('Response sent successfully');

    } catch (error) {
        console.error('Error in Change in RAT endpoint:', error);
        res.status(500).json({
            status: 'error',
            error: 'Internal Server Error',
            message: error.message,
            stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
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