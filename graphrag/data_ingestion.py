"""
Data ingestion pipeline for GraphRAG
"""

import logging
from typing import List, Dict, Any
import json

from .graphrag_engine import GraphRAGEngine
from .bedrock_client import BedrockClient

logger = logging.getLogger(__name__)

class DataIngestionPipeline:
    """Pipeline for ingesting healthcare data into GraphRAG system"""
    
    def __init__(self, engine: GraphRAGEngine):
        self.engine = engine
        self.bedrock_client = engine.bedrock_client
    
    def ingest_healthcare_knowledge(self):
        """Ingest synthetic healthcare knowledge"""
        logger.info("Starting healthcare knowledge ingestion...")
        
        # Ingest conditions
        self._ingest_conditions()
        
        # Ingest symptoms
        self._ingest_symptoms()
        
        # Ingest treatments
        self._ingest_treatments()
        
        # Ingest medications
        self._ingest_medications()
        
        # Ingest guidelines
        self._ingest_guidelines()
        
        # Create relationships
        self._create_relationships()
        
        logger.info("Healthcare knowledge ingestion complete")
    
    def _ingest_conditions(self):
        """Ingest medical conditions"""
        conditions = [
            {
                'id': 'cond_cataract_gj',
                'type': 'condition',
                'name': 'cataract',
                'display_name': 'Cataract',
                'region': 'gujarat',
                'domain': 'eye_health',
                'description': 'Clouding of the eye lens causing vision impairment',
                'prevalence': 'high',
                'content': 'Cataract is a common age-related eye condition where the lens becomes cloudy. In Gujarat, it affects approximately 8% of the population over 60. Symptoms include blurred vision, glare sensitivity, and difficulty seeing at night. Treatment typically involves surgical lens replacement.'
            },
            {
                'id': 'cond_glaucoma_gj',
                'type': 'condition',
                'name': 'glaucoma',
                'display_name': 'Glaucoma',
                'region': 'gujarat',
                'domain': 'eye_health',
                'description': 'Eye condition causing optic nerve damage',
                'prevalence': 'medium',
                'content': 'Glaucoma is a group of eye conditions that damage the optic nerve. Early detection through regular eye exams is crucial. Gujarat health centers offer free glaucoma screening for high-risk individuals.'
            },
            {
                'id': 'cond_diabetic_retinopathy_gj',
                'type': 'condition',
                'name': 'diabetic_retinopathy',
                'display_name': 'Diabetic Retinopathy',
                'region': 'gujarat',
                'domain': 'eye_health',
                'description': 'Diabetes complication affecting retina',
                'prevalence': 'high',
                'content': 'Diabetic retinopathy is a leading cause of blindness in Gujarat. All diabetic patients should have annual dilated eye exams. Early treatment can prevent vision loss.'
            }
        ]
        
        for condition in conditions:
            # Add to graph
            props = {k: v for k, v in condition.items() if k not in ['id', 'type', 'content']}
            self.engine.add_graph_entity('condition', condition['id'], props)
            
            # Index in vector store
            metadata = {
                'region': condition['region'],
                'domain': condition['domain'],
                'entity_type': 'condition',
                'title': condition['display_name']
            }
            self.engine.index_document(condition['id'], condition['content'], metadata)
        
        logger.info(f"Ingested {len(conditions)} conditions")
    
    def _ingest_symptoms(self):
        """Ingest symptoms"""
        symptoms = [
            {
                'id': 'symp_blurred_vision',
                'type': 'symptom',
                'name': 'blurred_vision',
                'display_name': 'Blurred Vision',
                'severity': 'moderate',
                'description': 'Unclear or fuzzy vision'
            },
            {
                'id': 'symp_eye_pain',
                'type': 'symptom',
                'name': 'eye_pain',
                'display_name': 'Eye Pain',
                'severity': 'high',
                'description': 'Pain or discomfort in the eye'
            },
            {
                'id': 'symp_light_sensitivity',
                'type': 'symptom',
                'name': 'light_sensitivity',
                'display_name': 'Light Sensitivity',
                'severity': 'moderate',
                'description': 'Increased sensitivity to light'
            }
        ]
        
        for symptom in symptoms:
            props = {k: v for k, v in symptom.items() if k not in ['id', 'type']}
            self.engine.add_graph_entity('symptom', symptom['id'], props)
        
        logger.info(f"Ingested {len(symptoms)} symptoms")
    
    def _ingest_treatments(self):
        """Ingest treatments"""
        treatments = [
            {
                'id': 'treat_cataract_surgery',
                'type': 'treatment',
                'name': 'cataract_surgery',
                'display_name': 'Cataract Surgery',
                'procedure_type': 'surgical',
                'success_rate': 0.95,
                'recovery_time': '4-6 weeks',
                'description': 'Surgical removal of cloudy lens and replacement with artificial lens'
            },
            {
                'id': 'treat_laser_therapy',
                'type': 'treatment',
                'name': 'laser_therapy',
                'display_name': 'Laser Therapy',
                'procedure_type': 'minimally_invasive',
                'success_rate': 0.85,
                'recovery_time': '1-2 weeks',
                'description': 'Laser treatment for various eye conditions'
            }
        ]
        
        for treatment in treatments:
            props = {k: v for k, v in treatment.items() if k not in ['id', 'type']}
            self.engine.add_graph_entity('treatment', treatment['id'], props)
        
        logger.info(f"Ingested {len(treatments)} treatments")
    
    def _ingest_medications(self):
        """Ingest medications"""
        medications = [
            {
                'id': 'med_eye_drops_antibiotic',
                'type': 'medication',
                'name': 'antibiotic_eye_drops',
                'display_name': 'Antibiotic Eye Drops',
                'category': 'antibiotic',
                'form': 'drops',
                'description': 'Topical antibiotic for eye infections'
            },
            {
                'id': 'med_glaucoma_drops',
                'type': 'medication',
                'name': 'glaucoma_drops',
                'display_name': 'Glaucoma Eye Drops',
                'category': 'pressure_reducing',
                'form': 'drops',
                'description': 'Medication to reduce intraocular pressure'
            }
        ]
        
        for medication in medications:
            props = {k: v for k, v in medication.items() if k not in ['id', 'type']}
            self.engine.add_graph_entity('medication', medication['id'], props)
        
        logger.info(f"Ingested {len(medications)} medications")
    
    def _ingest_guidelines(self):
        """Ingest regional guidelines"""
        guidelines = [
            {
                'id': 'guide_eye_screening_gj',
                'type': 'guideline',
                'name': 'eye_screening_protocol',
                'display_name': 'Eye Screening Protocol - Gujarat',
                'region': 'gujarat',
                'domain': 'eye_health',
                'authority': 'Gujarat Health Department',
                'content': 'Annual eye screening recommended for all individuals over 40. Diabetic patients should have screening every 6 months. Free screening available at all Primary Health Centers.'
            }
        ]
        
        for guideline in guidelines:
            props = {k: v for k, v in guideline.items() if k not in ['id', 'type', 'content']}
            self.engine.add_graph_entity('guideline', guideline['id'], props)
            
            # Index in vector store
            metadata = {
                'region': guideline['region'],
                'domain': guideline['domain'],
                'entity_type': 'guideline',
                'title': guideline['display_name']
            }
            self.engine.index_document(guideline['id'], guideline['content'], metadata)
        
        logger.info(f"Ingested {len(guidelines)} guidelines")
    
    def _create_relationships(self):
        """Create relationships between entities"""
        relationships = [
            # Condition -> Symptom
            ('cond_cataract_gj', 'symp_blurred_vision', 'has_symptom', {'frequency': 'common'}),
            ('cond_cataract_gj', 'symp_light_sensitivity', 'has_symptom', {'frequency': 'common'}),
            ('cond_glaucoma_gj', 'symp_eye_pain', 'has_symptom', {'frequency': 'occasional'}),
            
            # Condition -> Treatment
            ('cond_cataract_gj', 'treat_cataract_surgery', 'treated_by', {'effectiveness': 'high'}),
            ('cond_glaucoma_gj', 'treat_laser_therapy', 'treated_by', {'effectiveness': 'moderate'}),
            
            # Condition -> Medication
            ('cond_glaucoma_gj', 'med_glaucoma_drops', 'requires_medication', {'duration': 'long_term'}),
            
            # Treatment -> Medication
            ('treat_cataract_surgery', 'med_eye_drops_antibiotic', 'requires_medication', {'phase': 'post_operative'})
        ]
        
        for from_id, to_id, rel_type, props in relationships:
            self.engine.add_graph_relationship(from_id, to_id, rel_type, props)
        
        logger.info(f"Created {len(relationships)} relationships")
