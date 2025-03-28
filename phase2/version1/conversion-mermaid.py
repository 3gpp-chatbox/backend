prompt:you're referring to a flow property graph rather than a standard flowchart, which should include more specific details about the relationships between nodes. A flow property graph often highlights the state transitions between entities, events, and properties involved in a procedure, and it includes more metadata (like conditions, actions, timers, etc.) in the transitions (edges).

Let’s clarify the specific structure you need for a flow property graph:

Nodes will represent entities (such as states, processes, timers, or decisions).

Edges will represent transitions between those nodes, and each edge will have properties that describe the conditions, actions, or events triggering the transitions.

For a flow property graph, you need to represent:

Entities/States (Nodes): Representing states, processes, and timers (such as UE, AMF, timers like T3510, etc.).

Transitions (Edges): The relationships between these entities, including event triggers, conditions, and actions on the edges.

Flow Properties: Include metadata like the state change, conditions, or timers in the edge itself.

Simplify the Nodes: Each node should ideally contain the name of the process, not all its details. The detailed description can be shown on the edges or with tooltips if necessary.

Clarify the Edges: The edges should contain information such as the condition, whether it’s a sequential or conditional transition, or any associated timers.



