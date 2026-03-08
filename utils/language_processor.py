"""
Language Processing Utilities for RHISA Healthcare Chatbot
Handles multilingual support and translation
"""

import logging
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class LanguageProcessor:
    """Handles language processing and translation"""
    
    def __init__(self):
        self.supported_languages = ['en', 'gu', 'mr']
        self.language_patterns = self._load_language_patterns()
        self.medical_translations = self._load_medical_translations()
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            # Simple language detection based on character patterns
            text_clean = text.lower().strip()
            
            # Check for Gujarati characters
            if re.search(r'[\u0A80-\u0AFF]', text):
                return 'gu'
            
            # Check for Devanagari characters (Marathi/Hindi)
            if re.search(r'[\u0900-\u097F]', text):
                return 'mr'
            
            # Check for common Gujarati words in Latin script
            gujarati_words = ['aankh', 'chamdi', 'davai', 'doctor', 'hospital']
            if any(word in text_clean for word in gujarati_words):
                return 'gu'
            
            # Check for common Marathi words in Latin script
            marathi_words = ['dola', 'tvach', 'aushadh', 'daktar', 'rugnalaya']
            if any(word in text_clean for word in marathi_words):
                return 'mr'
            
            # Default to English
            return 'en'
            
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            return 'en'
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """Translate text to target language"""
        try:
            if source_language == target_language:
                return text
            
            # For demonstration, use simple dictionary-based translation
            # In production, this would use AWS Translate or similar service
            
            if target_language in self.medical_translations:
                translations = self.medical_translations[target_language]
                
                # Replace medical terms
                translated_text = text
                for english_term, translated_term in translations.items():
                    # Case-insensitive replacement
                    pattern = re.compile(re.escape(english_term), re.IGNORECASE)
                    translated_text = pattern.sub(translated_term, translated_text)
                
                return translated_text
            
            return text
            
        except Exception as e:
            logger.error(f"Error translating text: {str(e)}")
            return text
    
    def get_localized_response(self, response_key: str, language: str, **kwargs) -> str:
        """Get localized response template"""
        try:
            templates = self._get_response_templates()
            
            if language in templates and response_key in templates[language]:
                template = templates[language][response_key]
                return template.format(**kwargs)
            
            # Fallback to English
            if response_key in templates['en']:
                return templates['en'][response_key].format(**kwargs)
            
            return f"Response not available for {response_key}"
            
        except Exception as e:
            logger.error(f"Error getting localized response: {str(e)}")
            return "Error generating response"
    
    def format_medical_content(self, content: str, language: str, region: str) -> str:
        """Format medical content for specific language and region"""
        try:
            # Translate medical terms
            formatted_content = self.translate_text(content, language)
            
            # Add region-specific information
            if language == 'gu':
                formatted_content += f"\n\n*ગુજરાત માટે વિશેષ માહિતી*"
            elif language == 'mr':
                formatted_content += f"\n\n*महाराष्ट्रासाठी विशेष माहिती*"
            
            # Add cultural context
            formatted_content = self._add_cultural_context(formatted_content, language, region)
            
            return formatted_content
            
        except Exception as e:
            logger.error(f"Error formatting medical content: {str(e)}")
            return content
    
    def validate_language_input(self, text: str, expected_language: str) -> bool:
        """Validate if input text matches expected language"""
        try:
            detected_language = self.detect_language(text)
            return detected_language == expected_language
            
        except Exception as e:
            logger.error(f"Error validating language input: {str(e)}")
            return True  # Default to valid
    
    def get_language_specific_keywords(self, language: str) -> List[str]:
        """Get language-specific medical keywords"""
        try:
            keywords = {
                'en': [
                    'eye', 'vision', 'sight', 'skin', 'rash', 'doctor', 'medicine',
                    'treatment', 'symptoms', 'diagnosis', 'health', 'hospital'
                ],
                'gu': [
                    'આંખ', 'દૃષ્ટિ', 'ચામડી', 'ડૉક્ટર', 'દવા', 'સારવાર',
                    'લક્ષણો', 'આરોગ્ય', 'હોસ્પિટલ'
                ],
                'mr': [
                    'डोळा', 'दृष्टी', 'त्वचा', 'डॉक्टर', 'औषध', 'उपचार',
                    'लक्षणे', 'आरोग्य', 'रुग्णालय'
                ]
            }
            
            return keywords.get(language, keywords['en'])
            
        except Exception as e:
            logger.error(f"Error getting language keywords: {str(e)}")
            return []
    
    def _load_language_patterns(self) -> Dict[str, Any]:
        """Load language detection patterns"""
        return {
            'gujarati': {
                'unicode_range': r'[\u0A80-\u0AFF]',
                'common_words': ['આંખ', 'ચામડી', 'ડૉક્ટર', 'દવા', 'આરોગ્ય'],
                'transliteration': ['aankh', 'chamdi', 'doctor', 'davai', 'aarogya']
            },
            'marathi': {
                'unicode_range': r'[\u0900-\u097F]',
                'common_words': ['डोळा', 'त्वचा', 'डॉक्टर', 'औषध', 'आरोग्य'],
                'transliteration': ['dola', 'tvach', 'doctor', 'aushadh', 'aarogya']
            }
        }
    
    def _load_medical_translations(self) -> Dict[str, Dict[str, str]]:
        """Load medical term translations"""
        return {
            'gu': {
                'eye': 'આંખ',
                'vision': 'દૃષ્ટિ',
                'skin': 'ચામડી',
                'doctor': 'ડૉક્ટર',
                'medicine': 'દવા',
                'treatment': 'સારવાર',
                'symptoms': 'લક્ષણો',
                'diagnosis': 'નિદાન',
                'health': 'આરોગ્ય',
                'hospital': 'હોસ્પિટલ',
                'patient': 'દર્દી',
                'disease': 'રોગ',
                'infection': 'ચેપ',
                'pain': 'દુખાવો',
                'fever': 'તાવ',
                'cataract': 'મોતિયો',
                'glaucoma': 'કાળાપાણી',
                'diabetes': 'મધુમેહ',
                'hypertension': 'હાઈ બ્લડ પ્રેશર',
                'dermatitis': 'ચામડીની બળતરા',
                'eczema': 'ખરજવું'
            },
            'mr': {
                'eye': 'डोळा',
                'vision': 'दृष्टी',
                'skin': 'त्वचा',
                'doctor': 'डॉक्टर',
                'medicine': 'औषध',
                'treatment': 'उपचार',
                'symptoms': 'लक्षणे',
                'diagnosis': 'निदान',
                'health': 'आरोग्य',
                'hospital': 'रुग्णालय',
                'patient': 'रुग्ण',
                'disease': 'आजार',
                'infection': 'संसर्ग',
                'pain': 'वेदना',
                'fever': 'ताप',
                'cataract': 'मोतीबिंदू',
                'glaucoma': 'काळापाणी',
                'diabetes': 'मधुमेह',
                'hypertension': 'उच्च रक्तदाब',
                'dermatitis': 'त्वचेची जळजळ',
                'eczema': 'खरुज'
            }
        }
    
    def _get_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Get response templates for different languages"""
        return {
            'en': {
                'greeting': "Hello! I'm RHISA, your healthcare assistant for {region}. How can I help you today?",
                'error': "I apologize, but I encountered an error. Please try again.",
                'no_results': "I couldn't find specific information about your query. Could you please rephrase?",
                'compliance_check': "Checking compliance with {region} healthcare guidelines...",
                'trend_analysis': "Analyzing health trends for {condition} in {region}...",
                'patient_education': "Here's important information about {condition}:",
                'emergency': "For medical emergencies, please call 108 or visit your nearest hospital immediately."
            },
            'gu': {
                'greeting': "નમસ્તે! હું RHISA છું, {region} માટે તમારો આરોગ્ય સહાયક. આજે હું તમારી કેવી રીતે મદદ કરી શકું?",
                'error': "માફ કરશો, મને ભૂલ આવી છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.",
                'no_results': "તમારા પ્રશ્ન વિશે મને ચોક્કસ માહિતી મળી નથી. કૃપા કરીને ફરીથી પૂછો?",
                'compliance_check': "{region} આરોગ્ય માર્ગદર્શિકા સાથે અનુપાલન તપાસી રહ્યા છીએ...",
                'trend_analysis': "{region} માં {condition} માટે આરોગ્ય વલણોનું વિશ્લેષણ કરી રહ્યા છીએ...",
                'patient_education': "{condition} વિશે મહત્વપૂર્ણ માહિતી અહીં છે:",
                'emergency': "તબીબી કટોકટી માટે, કૃપા કરીને 108 પર કૉલ કરો અથવા તમારી નજીકની હોસ્પિટલમાં તરત જ જાઓ."
            },
            'mr': {
                'greeting': "नमस्कार! मी RHISA आहे, {region} साठी तुमचा आरोग्य सहाyyक. आज मी तुमची कशी मदत करू शकतो?",
                'error': "मी दिलगीर आहे, मला त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा.",
                'no_results': "मला तुमच्या प्रश्नाबद्दल विशिष्ट माहिती सापडली नाही. कृपया पुन्हा विचारा?",
                'compliance_check': "{region} आरोग्य मार्गदर्शक तत्त्वांसह अनुपालन तपासत आहे...",
                'trend_analysis': "{region} मध्ये {condition} साठी आरोग्य ट्रेंडचे विश्लेषण करत आहे...",
                'patient_education': "{condition} बद्दल महत्त्वाची माहिती येथे आहे:",
                'emergency': "वैद्यकीय आणीबाणीसाठी, कृपया 108 वर कॉल करा किंवा तुमच्या जवळच्या रुग्णालयात ताबडतोब जा."
            }
        }
    
    def _add_cultural_context(self, content: str, language: str, region: str) -> str:
        """Add cultural context to medical content"""
        try:
            cultural_additions = {
                'gu': {
                    'gujarat': "\n\n**સ્થાનિક સંસાધનો:**\n• નજીકના પ્રાથમિક આરોગ્ય કેન્દ્રનો સંપર્ક કરો\n• કટોકટી: 108",
                },
                'mr': {
                    'maharashtra': "\n\n**स्थानिक संसाधने:**\n• जवळच्या प्राथमिक आरोग्य केंद्राशी संपर्क साधा\n• आणीबाणी: 108",
                }
            }
            
            if language in cultural_additions and region in cultural_additions[language]:
                content += cultural_additions[language][region]
            
            return content
            
        except Exception as e:
            logger.error(f"Error adding cultural context: {str(e)}")
            return content