from typing import List, Dict, Optional
from dataclasses import dataclass
import re
import logging
from .refined_extractor import State, Action, ExecutionStep, Parameter

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class DataValidator:
    def __init__(self):
        self.known_states = {
            "CM-IDLE", "CM-CONNECTED",
            "RM-REGISTERED", "RM-DEREGISTERED",
            "5GMM-REGISTERED", "5GMM-DEREGISTERED",
            "EMM-REGISTERED", "EMM-DEREGISTERED"
        }
        
        self.known_actors = {"UE", "AMF", "SMF", "AUSF", "UDM", "SEAF"}
        
    def validate_state(self, state: State) -> ValidationResult:
        errors = []
        warnings = []
        
        if not state.name:
            errors.append("State name is required")
        
        if state.name and state.name not in self.known_states:
            warnings.append(f"Unknown state: {state.name}")
            
        if not state.type:
            errors.append("State type is required")
            
        if not state.description:
            warnings.append("State description is missing")
            
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_action(self, action: Action) -> ValidationResult:
        errors = []
        warnings = []
        
        if not action.name:
            errors.append("Action name is required")
            
        if not action.actor:
            errors.append("Actor is required")
        elif action.actor not in self.known_actors:
            warnings.append(f"Unknown actor: {action.actor}")
            
        if not action.outcome:
            warnings.append("Action outcome is missing")
            
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_execution_flow(self, steps: List[ExecutionStep]) -> ValidationResult:
        errors = []
        warnings = []
        
        if not steps:
            errors.append("Execution flow must have at least one step")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        step_numbers = set()
        for step in steps:
            if step.step_number in step_numbers:
                errors.append(f"Duplicate step number: {step.step_number}")
            step_numbers.add(step.step_number)
            
            if not step.action:
                errors.append(f"Step {step.step_number} has no action")
                
            if not step.actor:
                warnings.append(f"Step {step.step_number} has no actor")
                
            # Validate step references
            for next_step in step.next_steps:
                if next_step not in step_numbers and next_step > len(steps):
                    errors.append(f"Step {step.step_number} references invalid step {next_step}")
                    
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        ) 