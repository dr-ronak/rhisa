"""
Compliance Checker Agent for RHISA Healthcare Chatbot
Validates healthcare practices against regional guidelines
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ComplianceChecker:
    """Agent responsible for checking compliance with healthcare guidelines"""
    
    def __init__(self):
        self.guidelines = self._load_regional_guidelines()
        self.compliance_rules = self._initialize_compliance_rules()
    
    def check_compliance(self, case_data: Dict[str, Any], region: str) -> Dict[str, Any]:
        """Check compliance of case data against regional guidelines"""
        try:
            compliance_result = {
                'region': region,
                'overall_compliance': 'compliant',
                'compliance_score': 0,
                'checks_performed': [],
                'violations': [],
                'recommendations': [],
                'guidelines_referenced': []
            }
            
            # Get regional guidelines
            regional_guidelines = self.guidelines.get(region.lower(), {})
            
            # Perform various compliance checks
            checks = [
                self._check_medication_compliance(case_data, regional_guidelines),
                self._check_treatment_protocol_compliance(case_data, regional_guidelines),
                self._check_documentation_compliance(case_data, regional_guidelines),
                self._check_referral_compliance(case_data, regional_guidelines),
                self._check_follow_up_compliance(case_data, regional_guidelines)
            ]
            
            # Aggregate results
            total_score = 0
            total_checks = 0
            
            for check in checks:
                if check:
                    compliance_result['checks_performed'].append(check['check_name'])
                    total_score += check['score']
                    total_checks += 1
                    
                    if not check['compliant']:
                        compliance_result['violations'].extend(check['violations'])
                    
                    compliance_result['recommendations'].extend(check['recommendations'])
                    compliance_result['guidelines_referenced'].extend(check['guidelines_used'])
            
            # Calculate overall compliance
            if total_checks > 0:
                compliance_result['compliance_score'] = round(total_score / total_checks, 2)
                
                if compliance_result['compliance_score'] < 0.7:
                    compliance_result['overall_compliance'] = 'non_compliant'
                elif compliance_result['compliance_score'] < 0.9:
                    compliance_result['overall_compliance'] = 'partially_compliant'
            
            # Remove duplicates
            compliance_result['recommendations'] = list(set(compliance_result['recommendations']))
            compliance_result['guidelines_referenced'] = list(set(compliance_result['guidelines_referenced']))
            
            return compliance_result
            
        except Exception as e:
            logger.error(f"Error checking compliance: {str(e)}")
            return self._get_default_compliance_result(region)
    
    def check_and_explain(self, case_data: Dict[str, Any], region: str, language: str) -> str:
        """Check compliance and provide detailed explanation"""
        try:
            compliance_result = self.check_compliance(case_data, region)
            explanation = self._generate_compliance_explanation(compliance_result, language)
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating compliance explanation: {str(e)}")
            return self._get_error_response(language)
    
    def get_guidelines_summary(self, region: str, domain: str) -> Dict[str, Any]:
        """Get summary of guidelines for specific region and domain"""
        try:
            regional_guidelines = self.guidelines.get(region.lower(), {})
            domain_guidelines = regional_guidelines.get(domain.lower(), {})
            
            summary = {
                'region': region,
                'domain': domain,
                'key_guidelines': domain_guidelines.get('key_points', []),
                'mandatory_requirements': domain_guidelines.get('mandatory', []),
                'recommended_practices': domain_guidelines.get('recommended', []),
                'prohibited_practices': domain_guidelines.get('prohibited', []),
                'documentation_requirements': domain_guidelines.get('documentation', [])
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting guidelines summary: {str(e)}")
            return {}
    
    def validate_treatment_protocol(self, condition: str, treatment: str, region: str) -> Dict[str, Any]:
        """Validate specific treatment protocol"""
        try:
            validation_result = {
                'condition': condition,
                'treatment': treatment,
                'region': region,
                'is_valid': True,
                'confidence': 0.8,
                'alternative_treatments': [],
                'contraindications': [],
                'special_considerations': []
            }
            
            # Get condition-specific guidelines
            regional_guidelines = self.guidelines.get(region.lower(), {})
            condition_guidelines = self._get_condition_guidelines(condition, regional_guidelines)
            
            if condition_guidelines:
                # Check if treatment is in approved list
                approved_treatments = condition_guidelines.get('approved_treatments', [])
                if treatment.lower() not in [t.lower() for t in approved_treatments]:
                    validation_result['is_valid'] = False
                    validation_result['confidence'] = 0.3
                
                validation_result['alternative_treatments'] = approved_treatments
                validation_result['contraindications'] = condition_guidelines.get('contraindications', [])
                validation_result['special_considerations'] = condition_guidelines.get('special_considerations', [])
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating treatment protocol: {str(e)}")
            return {'is_valid': False, 'error': str(e)}
    
    def _load_regional_guidelines(self) -> Dict[str, Any]:
        """Load regional healthcare guidelines"""
        return {
            'gujarat': {
                'eye_health': {
                    'key_points': [
                        'Annual eye screening for diabetic patients',
                        'Cataract surgery within 6 weeks of diagnosis',
                        'Glaucoma monitoring every 3 months',
                        'UV protection education mandatory'
                    ],
                    'mandatory': [
                        'Pre-operative assessment for cataract surgery',
                        'Post-operative follow-up at 1 day, 1 week, 1 month',
                        'Diabetic retinopathy screening annually',
                        'Documentation of visual acuity measurements'
                    ],
                    'recommended': [
                        'Community eye health programs',
                        'School eye screening programs',
                        'Telemedicine for remote consultations',
                        'Patient education in local language'
                    ],
                    'prohibited': [
                        'Cataract surgery without proper pre-operative evaluation',
                        'Use of expired medications',
                        'Inadequate sterilization procedures'
                    ],
                    'documentation': [
                        'Patient consent forms in Gujarati/English',
                        'Detailed surgical notes',
                        'Post-operative care instructions',
                        'Complication reporting'
                    ],
                    'conditions': {
                        'cataract': {
                            'approved_treatments': ['Phacoemulsification', 'ECCE', 'SICS'],
                            'contraindications': ['Active eye infection', 'Uncontrolled diabetes'],
                            'special_considerations': ['Age-related factors', 'Diabetic status']
                        },
                        'glaucoma': {
                            'approved_treatments': ['Timolol', 'Latanoprost', 'Trabeculectomy'],
                            'contraindications': ['Asthma for beta-blockers', 'Pregnancy'],
                            'special_considerations': ['IOP monitoring', 'Visual field testing']
                        }
                    }
                },
                'skin_health': {
                    'key_points': [
                        'Antifungal treatment for monsoon-related infections',
                        'Occupational dermatitis prevention programs',
                        'Sun protection awareness campaigns',
                        'Hygiene education in rural areas'
                    ],
                    'mandatory': [
                        'Patch testing for contact dermatitis',
                        'Fungal culture for persistent infections',
                        'Biopsy for suspicious lesions',
                        'Follow-up for chronic conditions'
                    ],
                    'recommended': [
                        'Seasonal skin care guidance',
                        'Workplace safety measures',
                        'Community health worker training',
                        'Telemedicine for dermatology'
                    ],
                    'prohibited': [
                        'Use of steroids without proper indication',
                        'Self-medication with antibiotics',
                        'Inadequate wound care'
                    ],
                    'documentation': [
                        'Detailed skin examination notes',
                        'Photographic documentation',
                        'Treatment response monitoring',
                        'Adverse reaction reporting'
                    ],
                    'conditions': {
                        'dermatitis': {
                            'approved_treatments': ['Topical steroids', 'Antihistamines', 'Moisturizers'],
                            'contraindications': ['Viral skin infections', 'Bacterial infections'],
                            'special_considerations': ['Occupational exposure', 'Seasonal factors']
                        },
                        'fungal_infections': {
                            'approved_treatments': ['Antifungal creams', 'Oral antifungals', 'Antifungal powders'],
                            'contraindications': ['Liver disease for oral antifungals'],
                            'special_considerations': ['Humidity factors', 'Hygiene practices']
                        }
                    }
                }
            },
            'maharashtra': {
                'eye_health': {
                    'key_points': [
                        'Comprehensive eye examination for all patients',
                        'Diabetic retinopathy screening program',
                        'Cataract surgery quality assurance',
                        'Glaucoma awareness campaigns'
                    ],
                    'mandatory': [
                        'Pre-operative fitness clearance',
                        'Informed consent in patient\'s language',
                        'Post-operative care protocol adherence',
                        'Complication reporting to state authority'
                    ],
                    'recommended': [
                        'Mobile eye care units for rural areas',
                        'Integration with diabetes care programs',
                        'Continuing medical education for practitioners',
                        'Patient support groups'
                    ],
                    'prohibited': [
                        'Surgery without proper equipment calibration',
                        'Inadequate post-operative monitoring',
                        'Use of non-standard surgical techniques'
                    ],
                    'documentation': [
                        'Standardized surgical forms',
                        'Quality metrics reporting',
                        'Patient satisfaction surveys',
                        'Outcome tracking'
                    ],
                    'conditions': {
                        'cataract': {
                            'approved_treatments': ['Phacoemulsification', 'MSICS', 'Femtosecond laser'],
                            'contraindications': ['Severe corneal disease', 'Uncontrolled glaucoma'],
                            'special_considerations': ['Urban pollution effects', 'Diabetes management']
                        }
                    }
                },
                'skin_health': {
                    'key_points': [
                        'Monsoon-related skin infection management',
                        'Urban pollution and skin health',
                        'Occupational skin disease prevention',
                        'Skin cancer awareness programs'
                    ],
                    'mandatory': [
                        'Histopathological examination for suspicious lesions',
                        'Culture sensitivity for bacterial infections',
                        'Contact tracing for infectious conditions',
                        'Occupational health assessments'
                    ],
                    'recommended': [
                        'Seasonal dermatology clinics',
                        'Industrial hygiene programs',
                        'Public health education campaigns',
                        'Dermatology telemedicine services'
                    ],
                    'prohibited': [
                        'Inappropriate antibiotic use',
                        'Delay in malignancy evaluation',
                        'Inadequate infection control measures'
                    ],
                    'documentation': [
                        'Comprehensive dermatological assessment',
                        'Treatment outcome documentation',
                        'Occupational exposure history',
                        'Follow-up compliance tracking'
                    ]
                }
            }
        }
    
    def _initialize_compliance_rules(self) -> Dict[str, Any]:
        """Initialize compliance checking rules"""
        return {
            'medication_rules': {
                'prescription_required': ['antibiotics', 'steroids', 'controlled_substances'],
                'contraindication_check': True,
                'dosage_verification': True,
                'interaction_check': True
            },
            'documentation_rules': {
                'consent_required': True,
                'examination_notes': True,
                'treatment_plan': True,
                'follow_up_schedule': True
            },
            'treatment_rules': {
                'evidence_based': True,
                'guideline_adherence': True,
                'safety_protocols': True,
                'quality_standards': True
            }
        }
    
    def _check_medication_compliance(self, case_data: Dict[str, Any], guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check medication compliance"""
        try:
            medications = case_data.get('medications', [])
            if not medications:
                return None
            
            check_result = {
                'check_name': 'Medication Compliance',
                'compliant': True,
                'score': 1.0,
                'violations': [],
                'recommendations': [],
                'guidelines_used': ['Regional Medication Guidelines']
            }
            
            for medication in medications:
                # Check if medication requires prescription
                if any(controlled in medication.lower() for controlled in ['antibiotic', 'steroid', 'controlled']):
                    if 'prescription' not in case_data or not case_data['prescription']:
                        check_result['compliant'] = False
                        check_result['score'] = 0.5
                        check_result['violations'].append(f"Prescription required for {medication}")
                        check_result['recommendations'].append("Ensure proper prescription documentation")
            
            return check_result
            
        except Exception as e:
            logger.error(f"Error checking medication compliance: {str(e)}")
            return None
    
    def _check_treatment_protocol_compliance(self, case_data: Dict[str, Any], guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check treatment protocol compliance"""
        try:
            conditions = case_data.get('conditions', [])
            if not conditions:
                return None
            
            check_result = {
                'check_name': 'Treatment Protocol Compliance',
                'compliant': True,
                'score': 1.0,
                'violations': [],
                'recommendations': [],
                'guidelines_used': ['Regional Treatment Protocols']
            }
            
            for condition in conditions:
                # Check if treatment follows guidelines
                condition_guidelines = self._get_condition_guidelines(condition, guidelines)
                if condition_guidelines:
                    treatments = case_data.get('treatments', [])
                    approved_treatments = condition_guidelines.get('approved_treatments', [])
                    
                    if treatments and approved_treatments:
                        for treatment in treatments:
                            if treatment.lower() not in [t.lower() for t in approved_treatments]:
                                check_result['compliant'] = False
                                check_result['score'] = 0.7
                                check_result['violations'].append(f"Non-standard treatment {treatment} for {condition}")
                                check_result['recommendations'].append(f"Consider approved treatments: {', '.join(approved_treatments)}")
            
            return check_result
            
        except Exception as e:
            logger.error(f"Error checking treatment protocol compliance: {str(e)}")
            return None
    
    def _check_documentation_compliance(self, case_data: Dict[str, Any], guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check documentation compliance"""
        try:
            check_result = {
                'check_name': 'Documentation Compliance',
                'compliant': True,
                'score': 1.0,
                'violations': [],
                'recommendations': [],
                'guidelines_used': ['Documentation Standards']
            }
            
            required_fields = ['patient_id', 'examination_date', 'symptoms', 'diagnosis']
            missing_fields = []
            
            for field in required_fields:
                if field not in case_data or not case_data[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                check_result['compliant'] = False
                check_result['score'] = max(0.3, 1.0 - (len(missing_fields) * 0.2))
                check_result['violations'].append(f"Missing required documentation: {', '.join(missing_fields)}")
                check_result['recommendations'].append("Complete all required documentation fields")
            
            return check_result
            
        except Exception as e:
            logger.error(f"Error checking documentation compliance: {str(e)}")
            return None
    
    def _check_referral_compliance(self, case_data: Dict[str, Any], guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check referral compliance"""
        try:
            check_result = {
                'check_name': 'Referral Compliance',
                'compliant': True,
                'score': 1.0,
                'violations': [],
                'recommendations': [],
                'guidelines_used': ['Referral Guidelines']
            }
            
            # Check if complex cases have appropriate referrals
            conditions = case_data.get('conditions', [])
            complex_conditions = ['glaucoma', 'diabetic_retinopathy', 'skin_cancer']
            
            for condition in conditions:
                if condition.lower() in complex_conditions:
                    if 'referral' not in case_data or not case_data['referral']:
                        check_result['recommendations'].append(f"Consider specialist referral for {condition}")
            
            return check_result
            
        except Exception as e:
            logger.error(f"Error checking referral compliance: {str(e)}")
            return None
    
    def _check_follow_up_compliance(self, case_data: Dict[str, Any], guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check follow-up compliance"""
        try:
            check_result = {
                'check_name': 'Follow-up Compliance',
                'compliant': True,
                'score': 1.0,
                'violations': [],
                'recommendations': [],
                'guidelines_used': ['Follow-up Protocols']
            }
            
            # Check if follow-up is scheduled for chronic conditions
            conditions = case_data.get('conditions', [])
            chronic_conditions = ['diabetes', 'hypertension', 'glaucoma', 'chronic_dermatitis']
            
            for condition in conditions:
                if condition.lower() in chronic_conditions:
                    if 'follow_up_date' not in case_data or not case_data['follow_up_date']:
                        check_result['recommendations'].append(f"Schedule follow-up for {condition}")
            
            return check_result
            
        except Exception as e:
            logger.error(f"Error checking follow-up compliance: {str(e)}")
            return None
    
    def _get_condition_guidelines(self, condition: str, guidelines: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get guidelines for specific condition"""
        try:
            # Search in both eye_health and skin_health domains
            for domain in ['eye_health', 'skin_health']:
                domain_guidelines = guidelines.get(domain, {})
                conditions = domain_guidelines.get('conditions', {})
                
                if condition.lower() in conditions:
                    return conditions[condition.lower()]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting condition guidelines: {str(e)}")
            return None
    
    def _generate_compliance_explanation(self, compliance_result: Dict[str, Any], language: str) -> str:
        """Generate human-readable compliance explanation"""
        try:
            region = compliance_result['region'].title()
            overall_compliance = compliance_result['overall_compliance']
            score = compliance_result['compliance_score']
            
            explanation = f"**Compliance Check Results for {region}**\n\n"
            
            # Overall status
            if overall_compliance == 'compliant':
                explanation += f"✅ **Status**: Compliant (Score: {score}/1.0)\n"
                explanation += "The case meets regional healthcare guidelines.\n\n"
            elif overall_compliance == 'partially_compliant':
                explanation += f"⚠️ **Status**: Partially Compliant (Score: {score}/1.0)\n"
                explanation += "Some aspects need attention to meet full compliance.\n\n"
            else:
                explanation += f"❌ **Status**: Non-Compliant (Score: {score}/1.0)\n"
                explanation += "Significant compliance issues identified.\n\n"
            
            # Checks performed
            if compliance_result['checks_performed']:
                explanation += "**Checks Performed:**\n"
                for check in compliance_result['checks_performed']:
                    explanation += f"• {check}\n"
                explanation += "\n"
            
            # Violations
            if compliance_result['violations']:
                explanation += "**Compliance Issues:**\n"
                for violation in compliance_result['violations']:
                    explanation += f"• {violation}\n"
                explanation += "\n"
            
            # Recommendations
            if compliance_result['recommendations']:
                explanation += "**Recommendations:**\n"
                for i, rec in enumerate(compliance_result['recommendations'], 1):
                    explanation += f"{i}. {rec}\n"
                explanation += "\n"
            
            # Guidelines referenced
            if compliance_result['guidelines_referenced']:
                explanation += "**Guidelines Referenced:**\n"
                for guideline in compliance_result['guidelines_referenced']:
                    explanation += f"• {guideline}\n"
            
            explanation += "\n*This compliance check is based on regional healthcare guidelines and best practices.*"
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating compliance explanation: {str(e)}")
            return self._get_error_response(language)
    
    def _get_default_compliance_result(self, region: str) -> Dict[str, Any]:
        """Get default compliance result when check fails"""
        return {
            'region': region,
            'overall_compliance': 'unknown',
            'compliance_score': 0.0,
            'checks_performed': [],
            'violations': ['Unable to perform compliance check'],
            'recommendations': ['Ensure all required data is provided'],
            'guidelines_referenced': []
        }
    
    def _get_error_response(self, language: str) -> str:
        """Get error response in specified language"""
        responses = {
            'en': "I apologize, but I encountered an error while checking compliance. Please try again.",
            'gu': "માફ કરશો, અનુપાલન તપાસતી વખતે મને ભૂલ આવી છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.",
            'mr': "मी दिलगीर आहे, अनुपालन तपासताना मला त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा."
        }
        return responses.get(language, responses['en'])