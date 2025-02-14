from typing import Dict, List, Optional
import re
import logging
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StateType(Enum):
    UE_STATE = "UE_STATE"
    NETWORK_STATE = "NETWORK_STATE"
    CONNECTION_STATE = "CONNECTION_STATE"
    REGISTRATION_STATE = "REGISTRATION_STATE"
    SECURITY_STATE = "SECURITY_STATE"

@dataclass
class State:
    name: str
    type: StateType
    description: str
    conditions: List[str]
    source_section: str

@dataclass
class Action:
    name: str
    actor: str  # UE or Network Element
    target: Optional[str]
    parameters: List[str]
    prerequisites: List[str]
    outcome: str

@dataclass
class Event:
    name: str
    trigger: str
    source_state: str
    target_state: str
    conditions: List[str]
    parameters: List[str]

@dataclass
class Parameter:
    name: str
    type: str
    mandatory: bool
    value_range: Optional[str]
    description: str
    used_in: List[str]  # procedures/messages where this parameter is used

@dataclass
class ExecutionStep:
    step_number: int
    actor: str
    action: str
    parameters: List[str]
    conditions: List[str]
    next_steps: List[int]
    alternative_steps: Dict[str, int]  # condition -> step_number

@dataclass
class Conditional:
    condition: str
    evaluation_point: str
    true_path: List[int]  # step numbers
    false_path: List[int]  # step numbers
    parameters_involved: List[str]

class RefinedExtractor:
    def __init__(self):
        self._init_patterns()

    def _init_patterns(self):
        """Initialize regex patterns for extraction"""
        self.patterns = {
            "states": {
                "ue_state": r"(?:UE|user equipment)\s+(?:enters?|transitions?\s+to|in)\s+([A-Z][A-Z0-9-]+(?:\s+STATE)?)",
                "network_state": r"(?:network|AMF|SMF)\s+(?:enters?|transitions?\s+to|in)\s+([A-Z][A-Z0-9-]+(?:\s+STATE)?)",
                "connection_state": r"(?:connection|RRC)\s+(?:state|in)\s+([A-Z][A-Z0-9-]+(?:\s+STATE)?)",
                "registration_state": r"(?:registration|EMM|5GMM)\s+(?:state|in)\s+([A-Z][A-Z0-9-]+(?:\s+STATE)?)",
                "security_state": r"(?:security\s+context|security\s+mode)\s+(?:is|in)\s+([A-Z][A-Z0-9-]+(?:\s+STATE)?)"
            },
            "actions": {
                "ue_action": r"(?:UE|user equipment)\s+(?:shall|must|may)\s+([a-z]+(?:\s+[a-z]+)*)",
                "network_action": r"(?:network|AMF|SMF)\s+(?:shall|must|may)\s+([a-z]+(?:\s+[a-z]+)*)",
                "security_action": r"(?:authentication|security)\s+(?:shall|must|may)\s+([a-z]+(?:\s+[a-z]+)*)"
            },
            "events": {
                "trigger": r"(?:upon|when|after|if)\s+([^,\.]+)",
                "state_change": r"(?:causes?|triggers?|results? in)\s+([^,\.]+)",
                "timer": r"(?:timer|T3[0-9]+)\s+(?:expires?|starts?)"
            },
            "parameters": {
                "mandatory": r"(?:mandatory|required)\s+parameter\s+([A-Za-z0-9_]+)",
                "optional": r"optional\s+parameter\s+([A-Za-z0-9_]+)",
                "value_range": r"parameter\s+([A-Za-z0-9_]+)\s+range\s+(?:is|:)\s+([^,\.]+)",
                "type": r"(?:IE|parameter)\s+type\s+([A-Za-z0-9_]+)\s+(?:is|:)\s+([^,\.]+)"
            },
            "flow": {
                "step": r"(?:\d+\.|[a-z]\)|\-)\s+([^,\.]+)",
                "sequence": r"(?:then|after that|subsequently)\s+([^,\.]+)",
                "parallel": r"(?:meanwhile|simultaneously|in parallel)\s+([^,\.]+)"
            },
            "conditionals": {
                "if_then": r"if\s+([^,\.]+)\s+then\s+([^,\.]+)",
                "else": r"otherwise\s+([^,\.]+)",
                "case": r"in\s+case\s+(?:of|when)\s+([^,\.]+)"
            }
        }

    def extract_states(self, text: str) -> List[State]:
        """Extract different types of states and their properties"""
        states = []
        for state_type, pattern in self.patterns["states"].items():
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Get context around the state
                context = self._get_context(text, match.start(), 200)
                conditions = self._extract_conditions(context)
                
                state = State(
                    name=match.group(1).strip(),
                    type=StateType[state_type.upper()],
                    description=self._extract_description(context),
                    conditions=conditions,
                    source_section=self._extract_section_reference(context)
                )
                states.append(state)
        return states

    def extract_actions(self, text: str) -> List[Action]:
        """Extract actions performed by different entities"""
        actions = []
        for actor_type, pattern in self.patterns["actions"].items():
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                context = self._get_context(text, match.start(), 200)
                action = Action(
                    name=match.group(1).strip(),
                    actor=actor_type.split('_')[0].upper(),
                    target=self._extract_target(context),
                    parameters=self._extract_parameters(context),
                    prerequisites=self._extract_prerequisites(context),
                    outcome=self._extract_outcome(context)
                )
                actions.append(action)
        return actions

    def extract_execution_flow(self, text: str) -> List[ExecutionStep]:
        """Extract the sequence of steps in a procedure"""
        steps = []
        step_matches = re.finditer(self.patterns["flow"]["step"], text, re.MULTILINE)
        
        current_step = 0
        for match in step_matches:
            current_step += 1
            context = self._get_context(text, match.start(), 300)
            
            step = ExecutionStep(
                step_number=current_step,
                actor=self._extract_actor(context),
                action=match.group(1).strip(),
                parameters=self._extract_parameters(context),
                conditions=self._extract_conditions(context),
                next_steps=[current_step + 1],  # Default to next step
                alternative_steps=self._extract_alternative_steps(context)
            )
            steps.append(step)
            
        return self._link_steps(steps)

    def _extract_description(self, context: str) -> str:
        """Extract description from context"""
        # Look for descriptive text after state declaration
        desc_match = re.search(r'(?::|is|means|indicates)\s+([^,\.]+)', context)
        return desc_match.group(1).strip() if desc_match else ""

    def _extract_section_reference(self, context: str) -> str:
        """Extract section reference from context"""
        section_match = re.search(r'(?:section|clause)\s+(\d+\.\d+\.\d+(?:\.\d+)?)', context)
        return section_match.group(1) if section_match else ""

    def _extract_conditions(self, context: str) -> List[str]:
        """Extract conditions from context"""
        conditions = []
        for pattern in self.patterns["conditionals"].values():
            matches = re.finditer(pattern, context, re.IGNORECASE)
            conditions.extend(match.group(1).strip() for match in matches)
        return conditions

    def _extract_parameters(self, context: str) -> List[str]:
        """Extract parameters from context"""
        parameters = []
        for pattern in self.patterns["parameters"].values():
            matches = re.finditer(pattern, context, re.IGNORECASE)
            parameters.extend(match.group(1).strip() for match in matches)
        return parameters

    def _get_context(self, text: str, position: int, window: int) -> str:
        """Get surrounding context for a match"""
        start = max(0, position - window)
        end = min(len(text), position + window)
        return text[start:end].strip()

    def _link_steps(self, steps: List[ExecutionStep]) -> List[ExecutionStep]:
        """Link steps based on conditions and alternatives"""
        for i, step in enumerate(steps[:-1]):
            next_step = steps[i + 1]
            # Check for conditional branches
            if step.conditions:
                alt_steps = {}
                for condition in step.conditions:
                    # Find alternative step based on condition
                    alt_step = self._find_alternative_step(steps, i, condition)
                    if alt_step:
                        alt_steps[condition] = alt_step.step_number
                step.alternative_steps = alt_steps
        return steps

    def _find_alternative_step(self, steps: List[ExecutionStep], current_idx: int, 
                             condition: str) -> Optional[ExecutionStep]:
        """Find alternative step based on condition"""
        for step in steps[current_idx + 1:]:
            if any(cond in condition.lower() for cond in step.conditions):
                return step
        return None

    def _extract_target(self, context: str) -> Optional[str]:
        """Extract target entity from action context"""
        target_patterns = [
            r'(?:to|with|from)\s+(?:the\s+)?([A-Z][A-Za-z0-9-]+)',
            r'(?:sends?|receives?)\s+(?:to|from)\s+(?:the\s+)?([A-Z][A-Za-z0-9-]+)'
        ]
        
        for pattern in target_patterns:
            match = re.search(pattern, context)
            if match:
                return match.group(1).strip()
        return None

    def _extract_prerequisites(self, context: str) -> List[str]:
        """Extract prerequisites for an action"""
        prereq_patterns = [
            r'(?:requires?|needs?|must have)\s+([^,\.]+)',
            r'(?:after|following|upon)\s+([^,\.]+)',
            r'(?:only if|when)\s+([^,\.]+)'
        ]
        
        prerequisites = []
        for pattern in prereq_patterns:
            matches = re.finditer(pattern, context, re.IGNORECASE)
            prerequisites.extend(match.group(1).strip() for match in matches)
        return prerequisites

    def _extract_outcome(self, context: str) -> str:
        """Extract outcome of an action"""
        outcome_patterns = [
            r'(?:results? in|leads? to|causes?)\s+([^,\.]+)',
            r'(?:to|will|shall)\s+([^,\.]+)'
        ]
        
        for pattern in outcome_patterns:
            match = re.search(pattern, context)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_actor(self, context: str) -> str:
        """Extract actor from step context"""
        actor_patterns = {
            'UE': r'(?:UE|user equipment)\s+(?:shall|must|may|will)',
            'AMF': r'(?:AMF|network)\s+(?:shall|must|may|will)',
            'SMF': r'SMF\s+(?:shall|must|may|will)',
            'AUSF': r'AUSF\s+(?:shall|must|may|will)'
        }
        
        for actor, pattern in actor_patterns.items():
            if re.search(pattern, context, re.IGNORECASE):
                return actor
        return "UNKNOWN"

    def _extract_alternative_steps(self, context: str) -> Dict[str, int]:
        """Extract alternative steps based on conditions"""
        alt_steps = {}
        alt_patterns = [
            r'if\s+([^,\.]+)\s+then\s+(?:step\s+)?(\d+)',
            r'otherwise\s+(?:go to\s+)?(?:step\s+)?(\d+)',
            r'in\s+case\s+of\s+([^,\.]+)\s+(?:go to\s+)?(?:step\s+)?(\d+)'
        ]
        
        for pattern in alt_patterns:
            matches = re.finditer(pattern, context, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    condition, step = match.groups()
                    alt_steps[condition.strip()] = int(step)
                elif len(match.groups()) == 1:
                    alt_steps["otherwise"] = int(match.group(1))
        
        return alt_steps 