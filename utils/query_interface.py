from typing import List, Dict, Optional
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

class GraphQueryInterface:
    def __init__(self, neo4j_connection):
        self.neo4j = neo4j_connection

    def get_procedure_flow(self, procedure_name: str) -> List[Dict]:
        """Get complete procedure flow including all steps"""
        with self.neo4j.connect().session() as session:
            result = session.run("""
                MATCH (p:Procedure {name: $name})-[:HAS_STEP]->(s:Step)
                OPTIONAL MATCH (s)-[:USES]->(param:Parameter)
                OPTIONAL MATCH (s)-[:HAS_CONDITION]->(c:Condition)
                OPTIONAL MATCH (s)-[:NEXT]->(next:Step)
                OPTIONAL MATCH (s)-[:ALTERNATIVE]->(alt:Step)
                RETURN s, collect(distinct param) as parameters,
                       collect(distinct c) as conditions,
                       collect(distinct next) as next_steps,
                       collect(distinct alt) as alternative_steps
                ORDER BY s.number
            """, name=procedure_name)
            
            return [record.data() for record in result]

    def get_state_transitions(self, state_name: str) -> List[Dict]:
        """Get all transitions from/to a specific state"""
        with self.neo4j.connect().session() as session:
            result = session.run("""
                MATCH (s1:State {name: $name})-[r:TRANSITIONS_TO]->(s2:State)
                RETURN s1.name as from_state, s2.name as to_state,
                       r.condition as condition, r.trigger as trigger
                UNION
                MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State {name: $name})
                RETURN s1.name as from_state, s2.name as to_state,
                       r.condition as condition, r.trigger as trigger
            """, name=state_name)
            
            return [record.data() for record in result]

    def get_action_details(self, action_name: str) -> Dict:
        """Get complete details of an action including parameters and prerequisites"""
        with self.neo4j.connect().session() as session:
            result = session.run("""
                MATCH (a:Action {name: $name})
                OPTIONAL MATCH (a)-[:REQUIRES]->(p:Parameter)
                OPTIONAL MATCH (a)-[:HAS_PREREQUISITE]->(pre:Prerequisite)
                OPTIONAL MATCH (a)-[:TARGETS]->(t:Entity)
                RETURN a,
                       collect(distinct p) as parameters,
                       collect(distinct pre) as prerequisites,
                       collect(distinct t) as targets
            """, name=action_name)
            
            return result.single().data()

    def find_related_procedures(self, entity_name: str) -> List[Dict]:
        """Find all procedures involving a specific entity"""
        with self.neo4j.connect().session() as session:
            result = session.run("""
                MATCH (e:Entity {name: $name})<-[:INVOLVES]-(p:Procedure)
                OPTIONAL MATCH (p)-[:HAS_STEP]->(s:Step)
                RETURN p.name as procedure,
                       count(s) as step_count,
                       collect(s.action) as actions
            """, name=entity_name)
            
            return [record.data() for record in result]

    def get_conditional_flows(self, procedure_name: str) -> List[Dict]:
        """Get all conditional branches in a procedure"""
        with self.neo4j.connect().session() as session:
            result = session.run("""
                MATCH (p:Procedure {name: $name})-[:HAS_STEP]->(s:Step)
                MATCH (s)-[r:ALTERNATIVE]->(alt:Step)
                RETURN s.number as step_number,
                       s.action as action,
                       r.condition as condition,
                       alt.number as alternative_step,
                       alt.action as alternative_action
                ORDER BY s.number
            """, name=procedure_name)
            
            return [record.data() for record in result] 