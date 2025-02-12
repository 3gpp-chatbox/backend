# Implementation Plan: 3GPP NAS Procedure Knowledge Graph

**Project Goal:** To extract NAS procedures and their state flows from 3GPP specifications (.docx format, focusing on 24.501 and 23.502 initially) and represent them as a property graph in Neo4j for querying and visualization.


## Phase 1: Proof of Concept - Core Extraction and KG Building (Focus on a single .docx - e.g., 24.501)

**Goal:**  Successfully extract procedure names and states from a single .docx specification (24.501), create a basic Neo4j Knowledge Graph, and perform simple queries.



### Tasks:

* [x] **1. Environment Setup:**
    * [x] 1.1.  Install Python and set up a virtual environment (`venv` or `conda`).
    * [x] 1.2.  Install required Python libraries: `python-docx`, `neo4j-driver`.
    * [x] 1.3.  Install and configure Neo4j Community Edition.

* [ ] **2. Data Ingestion & .docx Text Extraction (24.501):**
    * [x] 2.1.  Choose the 24.501 .docx specification file.
    * [x] 2.2.  Write a Python script using `python-docx` to open and read the .docx file.
    * [x] 2.3.  Extract and print the text content of the document paragraph by paragraph.
    * [x] 2.4.  Review the printed text output to identify sections related to procedures and states.

* [ ] **3. Procedure and State Identification (Rule-based, Regex):**
    * [ ] 3.1.  Define regex patterns to identify procedure names (e.g., based on headings, bold text, keywords like "Procedure:").
    * [ ] 3.2.  Define regex patterns to identify state names (e.g., keywords like "State:", "UE state is," "enters state").
    * [ ] 3.3.  Write Python code to apply these regex patterns to the extracted text and extract procedure names and state names.
    * [ ] 3.4.  Manually review the extracted procedure and state names to validate accuracy.

* [ ] **4. Knowledge Graph Creation (Basic Procedure & State Graph in Neo4j):**
    * [ ] 4.1.  Define a basic Neo4j KG schema (Nodes: `Procedure`, `State`; Relationships: `HAS_STATE`, `TRANSITIONS_TO`).
    * [ ] 4.2.  Write Python code to connect to Neo4j using `neo4j-driver`.
    * [ ] 4.3.  Create `Procedure` nodes in Neo4j for each extracted procedure name.
    * [ ] 4.4.  Create `State` nodes in Neo4j for each extracted state name.
    * [ ] 4.5.  (Initial - simple connection)  For each procedure, create `HAS_STATE` relationships to its identified states (even if transition order is not yet determined).

* [ ] **5. Basic Querying & Visualization:**
    * [ ] 5.1.  Use Neo4j Browser to connect to your Neo4j database.
    * [ ] 5.2.  Write simple Cypher queries to retrieve `Procedure` and `State` nodes.
    * [ ] 5.3.  Visualize the created graph in Neo4j Browser, checking for `Procedure` and `State` nodes and `HAS_STATE` relationships.

---

## Phase 2: Enhancing Extraction and Adding State Flow (Expanding to 23.502, Deeper Parsing)

**Goal:** Improve procedure and state extraction accuracy, begin to capture state transition flows, and expand processing to include 23.502.

### Tasks:

* [ ] **1. Refine Parsing and Extraction Logic:**
    * [ ] 1.1.  Analyze the structure of procedure descriptions in 24.501 and 23.502 more deeply.
    * [ ] 1.2.  Improve regex patterns to be more robust and accurate in identifying procedures and states.
    * [ ] 1.3.  Implement logic to extract procedure descriptions and state descriptions (if available).
    * [ ] 1.4.  Consider using `python-docx` features to identify headings, lists, and formatting to improve parsing.

* [ ] **2. State Transition Extraction:**
    * [ ] 2.1.  Identify keywords and patterns in the text that indicate state transitions (e.g., "transitions to," "then," "next state is").
    * [ ] 2.2.  Develop logic to extract `TRANSITIONS_TO` relationships between `State` nodes based on these patterns and the order of states mentioned in procedure descriptions.
    * [ ] 2.3.  Test and refine state transition extraction on procedure descriptions in 24.501 and 23.502.

* [ ] **3. Expand Specification Coverage (Process 23.502):**
    * [ ] 3.1.  Adapt your Python scripts to process the 23.502 .docx specification.
    * [ ] 3.2.  Run your extraction and KG creation pipeline on 23.502, adding procedures and states from this document to the KG.
    * [ ] 3.3.  Review the combined KG (from 24.501 and 23.502) for consistency and accuracy.

* [ ] **4. Enhance KG Schema and Relationships:**
    * [ ] 4.1.  Refine the KG schema based on insights gained. Consider adding properties to `Procedure` and `State` nodes (e.g., `specification_section`, `procedure_id`).
    * [ ] 4.2.  Explore other potential relationships.  Are there relationships between procedures? (e.g., "Procedure A triggers Procedure B").  Start thinking about identifying these.

* [ ] **5. Advanced Querying and Visualization (State Flows):**
    * [ ] 5.1.  Write Cypher queries to explore state flows within procedures using `TRANSITIONS_TO` relationships.
    * [ ] 5.2.  Experiment with visualizing state flow paths in Neo4j Browser.

---

## Phase 3: Application Logic and Presentation (Optional - Depending on Goals)

**Goal:**  Develop an application to interact with the KG.  This phase is optional and depends on whether you want to build a user interface or API.

### Tasks (Example - Web UI):

* [ ] **1. Develop Data Access Layer:**
    * [ ] 1.1.  Create Python functions to encapsulate KG queries (e.g., `get_procedures()`, `get_states_for_procedure(procedure_name)`, `get_state_flow(procedure_name)`).

* [ ] **2. Build Application Logic Layer (using Flask or FastAPI - Example with Flask):**
    * [ ] 2.1.  Set up a Flask web application.
    * [ ] 2.2.  Create API endpoints (e.g., `/procedures`, `/procedure/{procedure_name}/states`, `/procedure/{procedure_name}/flow`) that use the Data Access Layer functions.

* [ ] **3. Develop Presentation Layer (Web UI - Example with HTML/JS):**
    * [ ] 3.1.  Create HTML templates to display lists of procedures, state information, and potentially interactive graph visualizations.
    * [ ] 3.2.  Use JavaScript and a graph visualization library (e.g., `vis.js`, `cytoscape.js`) to visualize procedure state flows fetched from the API.

---

## Resources and Notes:

*   **3GPP Specifications (24.501, 23.502 .docx files):**  [Location of your .docx files]
*   **Python `python-docx` library documentation:** [Link to python-docx documentation]
*   **Neo4j documentation:** [Link to Neo4j documentation]
*   **Neo4j Python Driver documentation (`neo4j-driver`):** [Link to neo4j-driver documentation]
*   **Regex Tutorial/Cheatsheet:** [Link to a good regex resource - e.g., regex101.com]
*   **Notes and Learnings:**
    *   [Space to add notes, challenges, and learnings as you progress]
    *   ...

---
**Last Updated:** 12/02/2024
