"""
Synthetic Data Generator for RHISA Healthcare Chatbot
Generates realistic synthetic patient data for testing and demonstration
"""

import json
import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid

logger = logging.getLogger(__name__)

@dataclass
class SyntheticPatient:
    """Synthetic patient data structure"""
    patient_id: str
    demographics: Dict[str, Any]
    medical_history: Dict[str, Any]
    visit_records: List[Dict[str, Any]]
    synthetic_flag: bool = True
    generation_date: str = None

class SyntheticDataGenerator:
    """Generator for synthetic healthcare data"""
    
    def __init__(self):
        self.demographic_data = self._load_demographic_templates()
        self.medical_conditions = self._load_medical_conditions()
        self.medications = self._load_medications()
        self.symptoms = self._load_symptoms()
        
    def generate_patient(self, region: str, condition: Optional[str] = None) -> SyntheticPatient:
        """Generate a single synthetic patient"""
        try:
            patient_id = f"SYN_{uuid.uuid4().hex[:8].upper()}"
            
            # Generate demographics
            demographics = self._generate_demographics(region)
            
            # Generate medical history
            medical_history = self._generate_medical_history(region, condition)
            
            # Generate visit records
            visit_records = self._generate_visit_records(demographics, medical_history)
            
            patient = SyntheticPatient(
                patient_id=patient_id,
                demographics=demographics,
                medical_history=medical_history,
                visit_records=visit_records,
                generation_date=datetime.utcnow().isoformat()
            )
            
            return patient
            
        except Exception as e:
            logger.error(f"Error generating synthetic patient: {str(e)}")
            return self._generate_default_patient(region)
    
    def generate_patient_batch(self, count: int, region: str, conditions: Optional[List[str]] = None) -> List[SyntheticPatient]:
        """Generate multiple synthetic patients"""
        try:
            patients = []
            
            for i in range(count):
                condition = None
                if conditions:
                    condition = random.choice(conditions)
                
                patient = self.generate_patient(region, condition)
                patients.append(patient)
            
            return patients
            
        except Exception as e:
            logger.error(f"Error generating patient batch: {str(e)}")
            return []
    
    def generate_health_trends_data(self, region: str, condition: str, months: int = 12) -> Dict[str, Any]:
        """Generate synthetic health trends data"""
        try:
            base_prevalence = self._get_base_prevalence(condition, region)
            seasonal_factors = self._get_seasonal_factors(condition, region)
            
            trends_data = {
                'region': region,
                'condition': condition,
                'time_period': f"{months} months",
                'monthly_data': [],
                'demographics': self._generate_demographic_trends(region, condition),
                'risk_factors': self._get_risk_factors(condition),
                'generated_at': datetime.utcnow().isoformat()
            }
            
            # Generate monthly data points
            current_date = datetime.now() - timedelta(days=30 * months)
            
            for month in range(months):
                month_date = current_date + timedelta(days=30 * month)
                seasonal_multiplier = seasonal_factors.get(month_date.strftime('%B').lower(), 1.0)
                
                # Add some randomness
                random_factor = random.uniform(0.8, 1.2)
                prevalence = base_prevalence * seasonal_multiplier * random_factor
                
                monthly_record = {
                    'month': month_date.strftime('%Y-%m'),
                    'month_name': month_date.strftime('%B %Y'),
                    'prevalence_rate': round(prevalence, 2),
                    'cases_reported': random.randint(50, 500),
                    'population_screened': random.randint(1000, 5000)
                }
                
                trends_data['monthly_data'].append(monthly_record)
            
            return trends_data
            
        except Exception as e:
            logger.error(f"Error generating trends data: {str(e)}")
            return {}
    
    def generate_clinical_case(self, region: str, condition: str, complexity: str = 'moderate') -> Dict[str, Any]:
        """Generate synthetic clinical case"""
        try:
            patient = self.generate_patient(region, condition)
            
            case_data = {
                'case_id': f"CASE_{uuid.uuid4().hex[:8].upper()}",
                'patient_id': patient.patient_id,
                'region': region,
                'primary_condition': condition,
                'complexity_level': complexity,
                'presentation': self._generate_case_presentation(condition, complexity),
                'examination_findings': self._generate_examination_findings(condition),
                'diagnostic_tests': self._generate_diagnostic_tests(condition),
                'treatment_plan': self._generate_treatment_plan(condition, region),
                'follow_up_plan': self._generate_follow_up_plan(condition),
                'patient_demographics': patient.demographics,
                'synthetic_flag': True,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return case_data
            
        except Exception as e:
            logger.error(f"Error generating clinical case: {str(e)}")
            return {}
    
    def _load_demographic_templates(self) -> Dict[str, Any]:
        """Load demographic data templates"""
        return {
            'gujarat': {
                'age_distribution': {
                    '0-18': 0.35,
                    '19-35': 0.30,
                    '36-60': 0.25,
                    '60+': 0.10
                },
                'gender_distribution': {'male': 0.52, 'female': 0.48},
                'urban_rural': {'urban': 0.43, 'rural': 0.57},
                'languages': ['gujarati', 'hindi', 'english'],
                'districts': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Gandhinagar'],
                'occupations': ['farmer', 'laborer', 'shopkeeper', 'teacher', 'government_employee', 'student']
            },
            'maharashtra': {
                'age_distribution': {
                    '0-18': 0.32,
                    '19-35': 0.33,
                    '36-60': 0.27,
                    '60+': 0.08
                },
                'gender_distribution': {'male': 0.51, 'female': 0.49},
                'urban_rural': {'urban': 0.45, 'rural': 0.55},
                'languages': ['marathi', 'hindi', 'english'],
                'districts': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur'],
                'occupations': ['office_worker', 'factory_worker', 'farmer', 'teacher', 'driver', 'student']
            }
        }
    
    def _load_medical_conditions(self) -> Dict[str, Any]:
        """Load medical conditions data"""
        return {
            'eye_health': {
                'cataract': {
                    'prevalence': {'gujarat': 8.2, 'maharashtra': 7.8},
                    'age_groups': ['50+', '60+', '70+'],
                    'symptoms': ['blurred_vision', 'glare_sensitivity', 'night_vision_problems'],
                    'risk_factors': ['age', 'diabetes', 'uv_exposure', 'smoking']
                },
                'glaucoma': {
                    'prevalence': {'gujarat': 3.8, 'maharashtra': 4.1},
                    'age_groups': ['40+', '50+', '60+'],
                    'symptoms': ['peripheral_vision_loss', 'eye_pain', 'headache'],
                    'risk_factors': ['family_history', 'high_eye_pressure', 'age', 'ethnicity']
                },
                'diabetic_retinopathy': {
                    'prevalence': {'gujarat': 5.2, 'maharashtra': 4.8},
                    'age_groups': ['30+', '40+', '50+'],
                    'symptoms': ['floaters', 'blurred_vision', 'dark_spots'],
                    'risk_factors': ['diabetes_duration', 'poor_glucose_control', 'hypertension']
                }
            },
            'skin_health': {
                'dermatitis': {
                    'prevalence': {'gujarat': 15.6, 'maharashtra': 12.3},
                    'age_groups': ['20-40', '30-50', 'all_ages'],
                    'symptoms': ['itching', 'redness', 'scaling', 'inflammation'],
                    'risk_factors': ['humidity', 'occupational_exposure', 'allergies', 'stress']
                },
                'fungal_infections': {
                    'prevalence': {'gujarat': 12.1, 'maharashtra': 18.9},
                    'age_groups': ['all_ages'],
                    'symptoms': ['itching', 'scaling', 'discoloration', 'odor'],
                    'risk_factors': ['humidity', 'poor_hygiene', 'overcrowding', 'diabetes']
                },
                'eczema': {
                    'prevalence': {'gujarat': 8.7, 'maharashtra': 9.2},
                    'age_groups': ['children', 'adults'],
                    'symptoms': ['dry_skin', 'itching', 'redness', 'cracking'],
                    'risk_factors': ['genetics', 'allergens', 'stress', 'climate']
                }
            }
        }
    
    def _load_medications(self) -> Dict[str, List[str]]:
        """Load medications data"""
        return {
            'eye_health': [
                'Timolol eye drops', 'Latanoprost', 'Brimonidine', 'Dorzolamide',
                'Prednisolone eye drops', 'Ciprofloxacin eye drops', 'Artificial tears'
            ],
            'skin_health': [
                'Hydrocortisone cream', 'Clotrimazole cream', 'Ketoconazole shampoo',
                'Calamine lotion', 'Antihistamines', 'Moisturizing cream', 'Antifungal powder'
            ],
            'general': [
                'Paracetamol', 'Ibuprofen', 'Metformin', 'Amlodipine',
                'Atorvastatin', 'Omeprazole', 'Multivitamins'
            ]
        }
    
    def _load_symptoms(self) -> Dict[str, List[str]]:
        """Load symptoms data"""
        return {
            'eye_health': [
                'blurred vision', 'eye pain', 'redness', 'discharge', 'light sensitivity',
                'floaters', 'flashing lights', 'night blindness', 'double vision'
            ],
            'skin_health': [
                'itching', 'rash', 'redness', 'scaling', 'burning sensation',
                'swelling', 'blisters', 'dry skin', 'discoloration'
            ],
            'general': [
                'fever', 'headache', 'fatigue', 'nausea', 'dizziness',
                'chest pain', 'shortness of breath', 'abdominal pain'
            ]
        }
    
    def _generate_demographics(self, region: str) -> Dict[str, Any]:
        """Generate demographic data for a patient"""
        region_data = self.demographic_data.get(region.lower(), self.demographic_data['gujarat'])
        
        # Generate age
        age_ranges = region_data['age_distribution']
        age_range = random.choices(list(age_ranges.keys()), weights=list(age_ranges.values()))[0]
        
        if age_range == '0-18':
            age = random.randint(0, 18)
        elif age_range == '19-35':
            age = random.randint(19, 35)
        elif age_range == '36-60':
            age = random.randint(36, 60)
        else:
            age = random.randint(60, 85)
        
        # Generate gender
        gender_dist = region_data['gender_distribution']
        gender = random.choices(['male', 'female'], weights=[gender_dist['male'], gender_dist['female']])[0]
        
        # Generate location
        urban_rural_dist = region_data['urban_rural']
        location_type = random.choices(['urban', 'rural'], weights=[urban_rural_dist['urban'], urban_rural_dist['rural']])[0]
        district = random.choice(region_data['districts'])
        
        # Generate other demographics
        language_preference = random.choice(region_data['languages'])
        occupation = random.choice(region_data['occupations'])
        
        return {
            'age': age,
            'gender': gender,
            'region': region,
            'district': district,
            'location_type': location_type,
            'language_preference': language_preference,
            'occupation': occupation,
            'education_level': random.choice(['primary', 'secondary', 'higher_secondary', 'graduate'])
        }
    
    def _generate_medical_history(self, region: str, target_condition: Optional[str] = None) -> Dict[str, Any]:
        """Generate medical history for a patient"""
        conditions = []
        medications = []
        allergies = []
        
        # Add target condition if specified
        if target_condition:
            conditions.append(target_condition)
            # Add related medications
            domain = self._get_condition_domain(target_condition)
            if domain in self.medications:
                medications.extend(random.sample(self.medications[domain], random.randint(1, 3)))
        
        # Add random additional conditions (10% chance each)
        all_conditions = []
        for domain in self.medical_conditions.values():
            all_conditions.extend(domain.keys())
        
        for condition in all_conditions:
            if condition != target_condition and random.random() < 0.1:
                conditions.append(condition)
        
        # Add general medications
        if random.random() < 0.3:
            medications.extend(random.sample(self.medications['general'], random.randint(1, 2)))
        
        # Add allergies (20% chance)
        if random.random() < 0.2:
            allergies = random.sample(['penicillin', 'sulfa', 'latex', 'peanuts', 'shellfish'], random.randint(1, 2))
        
        return {
            'conditions': list(set(conditions)),
            'medications': list(set(medications)),
            'allergies': allergies,
            'family_history': random.sample(['diabetes', 'hypertension', 'heart_disease', 'cancer'], random.randint(0, 2)),
            'smoking_status': random.choice(['never', 'former', 'current']),
            'alcohol_use': random.choice(['none', 'occasional', 'regular'])
        }
    
    def _generate_visit_records(self, demographics: Dict[str, Any], medical_history: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate visit records for a patient"""
        visits = []
        num_visits = random.randint(1, 5)
        
        for i in range(num_visits):
            visit_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            # Select primary condition for this visit
            conditions = medical_history.get('conditions', ['general_checkup'])
            primary_condition = random.choice(conditions) if conditions else 'general_checkup'
            
            # Generate symptoms based on condition
            domain = self._get_condition_domain(primary_condition)
            available_symptoms = self.symptoms.get(domain, self.symptoms['general'])
            visit_symptoms = random.sample(available_symptoms, random.randint(1, 3))
            
            visit = {
                'visit_id': f"VISIT_{uuid.uuid4().hex[:6].upper()}",
                'visit_date': visit_date.isoformat(),
                'primary_condition': primary_condition,
                'symptoms': visit_symptoms,
                'vital_signs': self._generate_vital_signs(demographics['age']),
                'diagnosis': primary_condition if primary_condition != 'general_checkup' else 'routine_examination',
                'treatment': self._generate_treatment(primary_condition),
                'follow_up_required': random.choice([True, False]),
                'provider': f"Dr. {random.choice(['Patel', 'Shah', 'Sharma', 'Desai', 'Joshi'])}"
            }
            
            visits.append(visit)
        
        return sorted(visits, key=lambda x: x['visit_date'], reverse=True)
    
    def _generate_vital_signs(self, age: int) -> Dict[str, Any]:
        """Generate realistic vital signs based on age"""
        # Age-adjusted normal ranges
        if age < 18:
            systolic_base = random.randint(90, 110)
            diastolic_base = random.randint(50, 70)
        elif age < 60:
            systolic_base = random.randint(110, 130)
            diastolic_base = random.randint(70, 85)
        else:
            systolic_base = random.randint(120, 140)
            diastolic_base = random.randint(75, 90)
        
        return {
            'blood_pressure': f"{systolic_base}/{diastolic_base}",
            'heart_rate': random.randint(60, 100),
            'temperature': round(random.uniform(98.0, 99.5), 1),
            'weight': random.randint(45, 90),
            'height': random.randint(150, 180)
        }
    
    def _get_condition_domain(self, condition: str) -> str:
        """Get the domain (eye_health/skin_health) for a condition"""
        for domain, conditions in self.medical_conditions.items():
            if condition in conditions:
                return domain
        return 'general'
    
    def _get_base_prevalence(self, condition: str, region: str) -> float:
        """Get base prevalence for a condition in a region"""
        for domain in self.medical_conditions.values():
            if condition in domain:
                return domain[condition]['prevalence'].get(region, 5.0)
        return 5.0
    
    def _get_seasonal_factors(self, condition: str, region: str) -> Dict[str, float]:
        """Get seasonal factors for a condition"""
        seasonal_patterns = {
            'dermatitis': {
                'june': 1.3, 'july': 1.5, 'august': 1.4, 'september': 1.2,
                'december': 0.7, 'january': 0.6, 'february': 0.8
            },
            'fungal_infections': {
                'june': 1.2, 'july': 1.6, 'august': 1.7, 'september': 1.4,
                'october': 1.1, 'november': 0.9, 'december': 0.7
            },
            'cataract': {
                'april': 1.1, 'may': 1.2, 'june': 1.3,
                'december': 0.9, 'january': 0.8, 'february': 0.9
            }
        }
        
        return seasonal_patterns.get(condition, {})
    
    def _get_risk_factors(self, condition: str) -> List[str]:
        """Get risk factors for a condition"""
        for domain in self.medical_conditions.values():
            if condition in domain:
                return domain[condition]['risk_factors']
        return ['unknown_factors']
    
    def _generate_demographic_trends(self, region: str, condition: str) -> Dict[str, Any]:
        """Generate demographic trend data"""
        return {
            'age_distribution': {
                '0-18': random.randint(5, 15),
                '19-35': random.randint(20, 35),
                '36-60': random.randint(30, 45),
                '60+': random.randint(25, 40)
            },
            'gender_distribution': {
                'male': random.randint(45, 55),
                'female': random.randint(45, 55)
            },
            'urban_rural_distribution': {
                'urban': random.randint(35, 65),
                'rural': random.randint(35, 65)
            }
        }
    
    def _generate_case_presentation(self, condition: str, complexity: str) -> Dict[str, Any]:
        """Generate case presentation details"""
        domain = self._get_condition_domain(condition)
        symptoms = self.symptoms.get(domain, self.symptoms['general'])
        
        if complexity == 'simple':
            num_symptoms = random.randint(1, 2)
        elif complexity == 'moderate':
            num_symptoms = random.randint(2, 4)
        else:  # complex
            num_symptoms = random.randint(3, 6)
        
        return {
            'chief_complaint': random.choice(symptoms),
            'symptoms': random.sample(symptoms, min(num_symptoms, len(symptoms))),
            'duration': f"{random.randint(1, 30)} days",
            'severity': random.choice(['mild', 'moderate', 'severe']),
            'associated_factors': random.sample(['stress', 'weather', 'diet', 'medication'], random.randint(0, 2))
        }
    
    def _generate_examination_findings(self, condition: str) -> Dict[str, Any]:
        """Generate examination findings"""
        domain = self._get_condition_domain(condition)
        
        if domain == 'eye_health':
            return {
                'visual_acuity': f"6/{random.choice([6, 9, 12, 18, 24, 36])}",
                'pupil_reaction': random.choice(['normal', 'sluggish', 'non-reactive']),
                'eye_pressure': f"{random.randint(10, 25)} mmHg",
                'fundus_examination': random.choice(['normal', 'abnormal', 'requires_dilation'])
            }
        elif domain == 'skin_health':
            return {
                'skin_appearance': random.choice(['normal', 'erythematous', 'scaly', 'vesicular']),
                'distribution': random.choice(['localized', 'generalized', 'bilateral']),
                'texture': random.choice(['smooth', 'rough', 'thickened']),
                'color_changes': random.choice(['none', 'hyperpigmentation', 'hypopigmentation'])
            }
        else:
            return {'general_examination': 'within_normal_limits'}
    
    def _generate_diagnostic_tests(self, condition: str) -> List[str]:
        """Generate appropriate diagnostic tests"""
        domain = self._get_condition_domain(condition)
        
        if domain == 'eye_health':
            tests = ['visual_field_test', 'OCT', 'fundus_photography', 'tonometry']
        elif domain == 'skin_health':
            tests = ['KOH_test', 'skin_biopsy', 'patch_test', 'bacterial_culture']
        else:
            tests = ['blood_test', 'urine_test', 'x_ray']
        
        return random.sample(tests, random.randint(1, 3))
    
    def _generate_treatment_plan(self, condition: str, region: str) -> Dict[str, Any]:
        """Generate treatment plan"""
        domain = self._get_condition_domain(condition)
        medications = self.medications.get(domain, self.medications['general'])
        
        return {
            'medications': random.sample(medications, random.randint(1, 3)),
            'non_pharmacological': random.sample([
                'lifestyle_modification', 'dietary_changes', 'exercise',
                'stress_management', 'hygiene_education'
            ], random.randint(1, 2)),
            'duration': f"{random.randint(1, 12)} weeks",
            'special_instructions': f"Follow regional guidelines for {region}"
        }
    
    def _generate_follow_up_plan(self, condition: str) -> Dict[str, Any]:
        """Generate follow-up plan"""
        return {
            'next_visit': f"{random.randint(1, 12)} weeks",
            'monitoring_parameters': random.sample([
                'symptom_improvement', 'medication_compliance', 'side_effects',
                'disease_progression', 'quality_of_life'
            ], random.randint(2, 4)),
            'red_flag_symptoms': random.sample([
                'worsening_symptoms', 'new_symptoms', 'medication_reactions',
                'vision_changes', 'severe_pain'
            ], random.randint(1, 3))
        }
    
    def _generate_treatment(self, condition: str) -> str:
        """Generate simple treatment description"""
        domain = self._get_condition_domain(condition)
        treatments = {
            'eye_health': ['eye drops prescribed', 'referral to specialist', 'surgery recommended'],
            'skin_health': ['topical medication', 'oral medication', 'lifestyle advice'],
            'general': ['medication prescribed', 'follow-up advised', 'lifestyle counseling']
        }
        
        return random.choice(treatments.get(domain, treatments['general']))
    
    def _generate_default_patient(self, region: str) -> SyntheticPatient:
        """Generate a default patient when generation fails"""
        return SyntheticPatient(
            patient_id="SYN_DEFAULT",
            demographics={
                'age': 35,
                'gender': 'male',
                'region': region,
                'district': 'Unknown',
                'location_type': 'urban',
                'language_preference': 'english',
                'occupation': 'unknown'
            },
            medical_history={
                'conditions': [],
                'medications': [],
                'allergies': [],
                'family_history': [],
                'smoking_status': 'never',
                'alcohol_use': 'none'
            },
            visit_records=[],
            generation_date=datetime.utcnow().isoformat()
        )