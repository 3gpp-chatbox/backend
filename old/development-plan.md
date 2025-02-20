# Implementation Plan: 3GPP NAS Procedure Knowledge Graph (Revised - Simplified Status)

**Project Goal:** To extract NAS procedures and their state flows from 3GPP specifications (.docx format, focusing on 24.501 and 23.502 initially) and represent them as a property graph in Neo4j for querying and visualization, **starting with basic procedure and state name extraction in Phase 1 and progressing to flow extraction in Phase 2.**

**Status Legend:**

- **[ ]** - To Do
- **[x]** - Done
- **[~]** - In Progress

---

## Phase 1: Proof of Concept - Basic Extraction and KG Building (Procedure & State _Names_ only)

**Goal:** Successfully extract _names_ of procedures and states from a single .docx specification (24.501), create a basic Neo4j Knowledge Graph with `Procedure` and `State` nodes and `HAS_STATE` relationships, and perform simple queries. **Focus is on name recognition, not flow or transitions in this phase.**

### Tasks:

- **[~] 1. Environment Setup:**

  - [x] 1.1. Install Python and set up a virtual environment (`venv` or `conda`).
  - [x] 1.2. Install required Python libraries: `python-docx`, `neo4j-driver`, and LangChain packages.
  - [x] 1.3. Install and configure Neo4j Community Edition.
  - [x] 1.4. Create a `requirements.txt` file and add initial dependencies.
  - [x] 1.5. Configure environment variables and API keys for LangChain integration.

- **[~] 2. Data Ingestion & .docx Text Extraction:**

  - [x] 2.1. Acquire specification files (24.501 and 23.502).
  - [x] 2.2. Write a Python script using `python-docx` to open and read the .docx files.
  - [x] 2.3. Extract and print the text content of the documents paragraph by paragraph.
  - [ ] 2.4. Review the printed text output to identify sections related to procedures and states.

- **[ ] 3. Procedure and State Name Identification (Hybrid Approach - Names only):**

  - [ ] 3.1. Analyze specifications to identify patterns for procedure and state _names_.
  - [ ] 3.2. Implement a hybrid extraction approach:
    - [ ] 3.2.1. Use regex patterns for clear structural matches
    - [ ] 3.2.2. Use LangChain for complex text analysis and name extraction
    - [ ] 3.2.3. Combine and deduplicate results from both approaches
  - [ ] 3.3. Validate extracted names against manual review
  - [ ] 3.4. Fine-tune extraction process based on validation results

- **[ ] 4. Knowledge Graph Creation (Basic KG - Names only):**

  - [ ] 4.1. Define a _basic_ Neo4j KG schema for Phase 1:
    - Nodes: `Procedure` (properties: `name`, `specification`), `State` (properties: `name`).
    - Relationships: `HAS_STATE` (Procedure -> State).
  - [ ] 4.2. Write Python code to connect to Neo4j using `neo4j-driver`.
  - [ ] 4.3. Create `Procedure` nodes in Neo4j for each extracted procedure name.
  - [ ] 4.4. Create `State` nodes in Neo4j for each extracted state name.
  - [ ] 4.5. For each procedure, create `HAS_STATE` relationships to its identified states (no flow yet).

- **[ ] 5. Basic Querying & Visualization (Names only):**
  - [ ] 5.1. Use Neo4j Browser to connect to your Neo4j database.
  - [ ] 5.2. Write simple Cypher queries to retrieve `Procedure` and `State` nodes and `HAS_STATE` relationships.
  - [ ] 5.3. Visualize the created basic graph in Neo4j Browser, checking for `Procedure` and `State` nodes and `HAS_STATE` relationships (focus on verifying names are extracted and linked, not flow).

---

## Phase 2: Enhancing Extraction - Procedure Flow and State Transitions

**Goal:** Improve procedure and state extraction to capture not just names, but also state transitions and procedure flow. Expand processing to include 23.502 and refine the KG schema to represent flows.

### Tasks:

- **[ ] 1. Refine Parsing and Extraction Logic (for Flow):**

  - [ ] 1.1. Analyze the structure of procedure descriptions in specifications
  - [ ] 1.2. Implement enhanced extraction using LangChain:
    - [ ] 1.2.1. Create custom prompts for flow extraction
    - [ ] 1.2.2. Use LLM to identify state transitions and relationships
    - [ ] 1.2.3. Validate and clean LLM outputs
  - [ ] 1.3. Combine rule-based and LLM-based approaches for robust extraction
  - [ ] 1.4. Implement validation and error checking

- **[ ] 2. State Transition Relationship Extraction:**

  - [ ] 2.1. Identify keywords and sentence structures indicating state transitions (e.g., "transitions to," "then," "next state is," "from state A to state B").
  - [ ] 2.2. Develop logic to extract `TRANSITIONS_TO` relationships between `State` nodes based on these patterns and the order of states in procedure descriptions.
  - [ ] 2.3. Test and refine state transition extraction on procedure descriptions in 24.501 and 23.502.

- **[ ] 3. Expand Specification Coverage (Process 23.502 for Flow):**

  - [ ] 3.1. Adapt your Python scripts to process the 23.502 .docx specification for procedure flows.
  - [ ] 3.2. Run your enhanced extraction and KG creation pipeline on 23.502, adding procedure flows from this document to the KG.
  - [ ] 3.3. Review the combined KG (from 24.501 and 23.502) for flow representation, consistency, and accuracy.

- **[ ] 4. Enhance KG Schema for Flow Representation:**

  - [ ] 4.1. Refine the KG schema to include `TRANSITIONS_TO` relationships between `State` nodes.
  - [ ] 4.2. Consider adding properties to `State` nodes to describe their role in the flow (e.g., `is_initial_state`, `is_final_state`).
  - [ ] 4.3. Think about representing triggers for transitions (messages, events) in the KG in later sub-phases (e.g., Phase 2.x or Phase 3).

- **[ ] 5. Advanced Querying and Visualization (State Flows):**
  - [ ] 5.1. Write Cypher queries to explore state flows within procedures using `TRANSITIONS_TO` relationships.
  - [ ] 5.2. Experiment with visualizing state flow paths in Neo4j Browser.
  - [ ] 5.3. Potentially develop more interactive visualizations of procedure flows (e.g., using a web UI and graph visualization library in later sub-phases/Phase 3).

---

## Phase 3: Application Logic and Presentation (Optional - Depending on Goals)

### Tasks (Example - Web UI):

- **[ ] 1. Develop Data Access Layer:**

  - [ ] 1.1. Create Python functions to encapsulate KG queries (e.g., `get_procedures()`, `get_states_for_procedure(procedure_name)`, `get_state_flow(procedure_name)`).

- **[ ] 2. Build Application Logic Layer (using Flask or FastAPI - Example with Flask):**

  - [ ] 2.1. Set up a Flask web application.
  - [ ] 2.2. Create API endpoints (e.g., `/procedures`, `/procedure/{procedure_name}/states`, `/procedure/{procedure_name}/flow`) that use the Data Access Layer functions.

- **[ ] 3. Develop Presentation Layer (Web UI - Example with HTML/JS):**
  - [ ] 3.1. Create HTML templates to display lists of procedures, state information, and potentially interactive graph visualizations.
  - [ ] 3.2. Use JavaScript and a graph visualization library (e.g., `vis.js`, `cytoscape.js`) to visualize procedure state flows fetched from the API.

---

## Resources and Notes:

- **3GPP Specifications:** Located in `data/` directory
- **Python Libraries:**
  - `python-docx`: [https://python-docx.readthedocs.io/en/master/](https://python-docx.readthedocs.io/en/master/)
  - `neo4j-driver`: [https://neo4j.com/docs/python-driver/current/](https://neo4j.com/docs/python-driver/current/)
  - LangChain: [https://python.langchain.com/docs/get_started/introduction](https://python.langchain.com/docs/get_started/introduction)
- **Neo4j documentation:** [https://neo4j.com/docs/](https://neo4j.com/docs/)
- **Notes and Learnings:**
  - Project structure established with virtual environment and key dependencies
  - Added LangChain integration for improved text analysis capabilities
  - Environment variables need to be configured for LLM access
