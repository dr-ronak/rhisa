"""
Entity Extractor for RHISA Healthcare Chatbot
Extracts medical entities from text using rule-based and pattern matching
"""

import re
import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class EntityExtractor:
    """Extracts medical entities from text"""
    
    def __init__(self):
        self.medical_entities = self._load_medical_entities()
        self.patterns = self._load_extraction_patterns()
        self.confidence_threshold = 0.7
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract medical entities from text"""
        try:
            entities = []
            text_lower = text.lower()
            
            # Extract different types of entities
            entities.extend(self._extract_conditions(text_lower))
            entities.extend(self._extract_medications(text_lower))
            entities.extend(self._extract_symptoms(text_lower))
            entities.extend(self._extract_anatomy(text_lower))
            entities.extend(self._extract_procedures(text_lower))
            entities.extend(self._extract_demographics(text_lower))
            entities.extend(self._extract_temporal(text))
            entities.extend(self._extract_numeric(text))
            
            # Remove duplicates and sort by confidence
            entities = self._deduplicate_entities(entities)
            entities.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return []
    
    def extract_medical_context(self, text: str) -> Dict[str, Any]:
        """Extract medical context from text"""
        try:
            entities = self.extract_entities(text)
            
            context = {
                'conditions': [],
                'medications': [],
                'symptoms': [],
                'anatomy': [],
                'procedures': [],
                'demographics': {},
                'temporal': [],
                'severity': None,
                'urgency': None
            }
            
            for entity in entities:
                entity_type = entity.get('type', '').lower()
                entity_text = entity.get('text', '')
                
                if entity_type == 'condition':
                    context['conditions'].append(entity_text)
                elif entity_type == 'medication':
                    context['medications'].append(entity_text)
                elif entity_type == 'symptom':
                    context['symptoms'].append(entity_text)
                elif entity_type == 'anatomy':
                    context['anatomy'].append(entity_text)
                elif entity_type == 'procedure':
                    context['procedures'].append(entity_text)
                elif entity_type == 'demographic':
                    context['demographics'][entity.get('subtype', 'general')] = entity_text
                elif entity_type == 'temporal':
                    context['temporal'].append(entity_text)
            
            # Determine severity and urgency
            context['severity'] = self._determine_severity(text, entities)
            context['urgency'] = self._determine_urgency(text, entities)
            
            return context
            
        except Exception as e:
            logger.error(f"Error extracting medical context: {str(e)}")
            return {}
    
    def validate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate extracted entities"""
        try:
            validated_entities = []
            
            for entity in entities:
                if self._is_valid_entity(entity):
                    validated_entities.append(entity)
            
            return validated_entities
            
        except Exception as e:
            logger.error(f"Error validating entities: {str(e)}")
            return entities
    
    def _load_medical_entities(self) -> Dict[str, List[str]]:
        """Load medical entity dictionaries"""
        return {
            'conditions': [
                'cataract', 'glaucoma', 'diabetic retinopathy', 'conjunctivitis',
                'dry eyes', 'macular degeneration', 'retinal detachment',
                'dermatitis', 'eczema', 'psoriasis', 'fungal infection',
                'bacterial infection', 'acne', 'rosacea', 'skin cancer',
                'diabetes', 'hypertension', 'heart disease', 'asthma',
                'arthritis', 'migraine', 'depression', 'anxiety'
            ],
            'medications': [
                'timolol', 'latanoprost', 'brimonidine', 'dorzolamide',
                'prednisolone', 'ciprofloxacin', 'artificial tears',
                'hydrocortisone', 'clotrimazole', 'ketoconazole',
                'calamine', 'antihistamine', 'moisturizer', 'sunscreen',
                'paracetamol', 'ibuprofen', 'aspirin', 'metformin',
                'amlodipine', 'atorvastatin', 'omeprazole'
            ],
            'symptoms': [
                'blurred vision', 'eye pain', 'redness', 'discharge',
                'light sensitivity', 'floaters', 'flashing lights',
                'night blindness', 'double vision', 'itching', 'rash',
                'burning sensation', 'swelling', 'blisters', 'dry skin',
                'scaling', 'discoloration', 'fever', 'headache',
                'fatigue', 'nausea', 'dizziness', 'chest pain'
            ],
            'anatomy': [
                'eye', 'eyelid', 'cornea', 'iris', 'pupil', 'lens',
                'retina', 'optic nerve', 'skin', 'epidermis', 'dermis',
                'hair follicle', 'sebaceous gland', 'nail', 'scalp',
                'face', 'neck', 'arm', 'leg', 'chest', 'back'
            ],
            'procedures': [
                'cataract surgery', 'laser therapy', 'injection',
                'eye examination', 'visual field test', 'tonometry',
                'skin biopsy', 'patch test', 'culture test',
                'blood test', 'urine test', 'x-ray', 'ultrasound',
                'mri', 'ct scan', 'ecg', 'endoscopy'
            ]
        }
    
    def _load_extraction_patterns(self) -> Dict[str, List[str]]:
        """Load regex patterns for entity extraction"""
        return {
            'age': [
                r'\b(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|y\.?o\.?)\b',
                r'\bage\s*:?\s*(\d{1,3})\b',
                r'\b(\d{1,3})\s*year\s*old\b'
            ],
            'duration': [
                r'\b(\d+)\s*(?:days?|weeks?|months?|years?)\b',
                r'\bfor\s*(\d+)\s*(?:days?|weeks?|months?|years?)\b',
                r'\bsince\s*(\d+)\s*(?:days?|weeks?|months?|years?)\b'
            ],
            'dosage': [
                r'\b(\d+(?:\.\d+)?)\s*(?:mg|ml|drops?|tablets?|capsules?)\b',
                r'\b(\d+)\s*times?\s*(?:a\s*)?day\b',
                r'\bevery\s*(\d+)\s*hours?\b'
            ],
            'severity': [
                r'\b(mild|moderate|severe|acute|chronic|slight|intense)\b',
                r'\b(very|extremely|quite|somewhat)\s*(painful|itchy|red|swollen)\b'
            ],
            'frequency': [
                r'\b(daily|weekly|monthly|occasionally|frequently|rarely)\b',
                r'\b(\d+)\s*times?\s*(?:per|a)\s*(?:day|week|month)\b'
            ]
        }
    
    def _extract_conditions(self, text: str) -> List[Dict[str, Any]]:
        """Extract medical conditions"""
        entities = []
        conditions = self.medical_entities['conditions']
        
        for condition in conditions:
            if condition.lower() in text:
                start_pos = text.find(condition.lower())
                entities.append({
                    'text': condition,
                    'type': 'CONDITION',
                    'start': start_pos,
                    'end': start_pos + len(condition),
                    'confidence': 0.9
                })
        
        return entities
    
    def _extract_medications(self, text: str) -> List[Dict[str, Any]]:
        """Extract medications"""
        entities = []
        medications = self.medical_entities['medications']
        
        for medication in medications:
            if medication.lower() in text:
                start_pos = text.find(medication.lower())
                entities.append({
                    'text': medication,
                    'type': 'MEDICATION',
                    'start': start_pos,
                    'end': start_pos + len(medication),
                    'confidence': 0.85
                })
        
        return entities
    
    def _extract_symptoms(self, text: str) -> List[Dict[str, Any]]:
        """Extract symptoms"""
        entities = []
        symptoms = self.medical_entities['symptoms']
        
        for symptom in symptoms:
            if symptom.lower() in text:
                start_pos = text.find(symptom.lower())
                entities.append({
                    'text': symptom,
                    'type': 'SYMPTOM',
                    'start': start_pos,
                    'end': start_pos + len(symptom),
                    'confidence': 0.8
                })
        
        return entities
    
    def _extract_anatomy(self, text: str) -> List[Dict[str, Any]]:
        """Extract anatomical references"""
        entities = []
        anatomy_terms = self.medical_entities['anatomy']
        
        for term in anatomy_terms:
            if term.lower() in text:
                start_pos = text.find(term.lower())
                entities.append({
                    'text': term,
                    'type': 'ANATOMY',
                    'start': start_pos,
                    'end': start_pos + len(term),
                    'confidence': 0.75
                })
        
        return entities
    
    def _extract_procedures(self, text: str) -> List[Dict[str, Any]]:
        """Extract medical procedures"""
        entities = []
        procedures = self.medical_entities['procedures']
        
        for procedure in procedures:
            if procedure.lower() in text:
                start_pos = text.find(procedure.lower())
                entities.append({
                    'text': procedure,
                    'type': 'PROCEDURE',
                    'start': start_pos,
                    'end': start_pos + len(procedure),
                    'confidence': 0.85
                })
        
        return entities
    
    def _extract_demographics(self, text: str) -> List[Dict[str, Any]]:
        """Extract demographic information"""
        entities = []
        
        # Extract age
        age_patterns = self.patterns['age']
        for pattern in age_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(1),
                    'type': 'DEMOGRAPHIC',
                    'subtype': 'age',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.9
                })
        
        # Extract gender
        gender_pattern = r'\b(male|female|man|woman|boy|girl)\b'
        matches = re.finditer(gender_pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({
                'text': match.group(1),
                'type': 'DEMOGRAPHIC',
                'subtype': 'gender',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.8
            })
        
        return entities
    
    def _extract_temporal(self, text: str) -> List[Dict[str, Any]]:
        """Extract temporal information"""
        entities = []
        
        # Extract duration
        duration_patterns = self.patterns['duration']
        for pattern in duration_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(0),
                    'type': 'TEMPORAL',
                    'subtype': 'duration',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.85
                })
        
        # Extract frequency
        frequency_patterns = self.patterns['frequency']
        for pattern in frequency_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(0),
                    'type': 'TEMPORAL',
                    'subtype': 'frequency',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.8
                })
        
        return entities
    
    def _extract_numeric(self, text: str) -> List[Dict[str, Any]]:
        """Extract numeric information"""
        entities = []
        
        # Extract dosage
        dosage_patterns = self.patterns['dosage']
        for pattern in dosage_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(0),
                    'type': 'NUMERIC',
                    'subtype': 'dosage',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.9
                })
        
        return entities
    
    def _determine_severity(self, text: str, entities: List[Dict[str, Any]]) -> Optional[str]:
        """Determine severity from text and entities"""
        severity_keywords = {
            'mild': ['mild', 'slight', 'minor', 'little'],
            'moderate': ['moderate', 'medium', 'some', 'noticeable'],
            'severe': ['severe', 'intense', 'extreme', 'very', 'acute', 'chronic']
        }
        
        text_lower = text.lower()
        
        for severity, keywords in severity_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return severity
        
        return None
    
    def _determine_urgency(self, text: str, entities: List[Dict[str, Any]]) -> Optional[str]:
        """Determine urgency from text and entities"""
        urgent_keywords = [
            'emergency', 'urgent', 'immediate', 'severe pain',
            'can\'t see', 'sudden', 'acute', 'bleeding'
        ]
        
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            return 'high'
        
        # Check for symptoms that might indicate urgency
        urgent_symptoms = ['severe pain', 'sudden vision loss', 'severe bleeding']
        for symptom in urgent_symptoms:
            if symptom in text_lower:
                return 'high'
        
        return 'normal'
    
    def _deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entities"""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            # Create a unique key based on text and type
            key = (entity.get('text', '').lower(), entity.get('type', ''))
            
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _is_valid_entity(self, entity: Dict[str, Any]) -> bool:
        """Validate if entity meets quality criteria"""
        try:
            # Check required fields
            if not all(key in entity for key in ['text', 'type']):
                return False
            
            # Check confidence threshold
            confidence = entity.get('confidence', 0)
            if confidence < self.confidence_threshold:
                return False
            
            # Check text length
            text = entity.get('text', '')
            if len(text) < 2 or len(text) > 100:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating entity: {str(e)}")
            return False