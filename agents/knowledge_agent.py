"""
Knowledge Agent for RHISA Healthcare Chatbot
Handles knowledge base queries and patient education generation
"""

import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class KnowledgeAgent:
    """Agent responsible for knowledge retrieval and patient education"""
    
    def __init__(self):
        self.knowledge_base = self._load_synthetic_knowledge()
        self.patient_education_templates = self._load_education_templates()
    
    def search(self, query: str, region: str, language: str) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant information"""
        try:
            # Simulate vector search with synthetic data
            results = []
            query_lower = query.lower()
            
            for doc in self.knowledge_base:
                # Simple keyword matching for demonstration
                if (any(keyword in doc['content'].lower() for keyword in query_lower.split()) and
                    doc['region'] == region):
                    
                    # Calculate synthetic relevance score
                    relevance = self._calculate_relevance(query, doc['content'])
                    
                    results.append({
                        'document_id': doc['id'],
                        'title': doc['title'],
                        'content': doc['content'][:500] + '...' if len(doc['content']) > 500 else doc['content'],
                        'relevance_score': relevance,
                        'source': doc['source'],
                        'region': doc['region'],
                        'domain': doc['domain']
                    })
            
            # Sort by relevance and return top 5
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return results[:5]
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []
    
    def search_and_respond(self, query: str, region: str, language: str) -> str:
        """Search knowledge base and generate response"""
        try:
            results = self.search(query, region, language)
            
            if not results:
                return self._get_no_results_response(language)
            
            # Generate response based on search results
            response = self._generate_search_response(results, query, region, language)
            return response
            
        except Exception as e:
            logger.error(f"Error generating search response: {str(e)}")
            return self._get_error_response(language)
    
    def generate_patient_education(self, condition: str, language: str, region: str) -> str:
        """Generate patient education content"""
        try:
            template = self.patient_education_templates.get(condition.lower(), 
                                                          self.patient_education_templates['general'])
            
            # Customize content based on region and language
            content = self._customize_education_content(template, region, language)
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating patient education: {str(e)}")
            return self._get_error_response(language)
    
    def general_response(self, message: str, region: str, language: str) -> str:
        """Generate general response for unclassified queries"""
        try:
            # Analyze message for health-related keywords
            health_keywords = ['health', 'medical', 'doctor', 'treatment', 'symptom', 'disease']
            message_lower = message.lower()
            
            if any(keyword in message_lower for keyword in health_keywords):
                return self._get_health_general_response(region, language)
            else:
                return self._get_general_greeting_response(language)
                
        except Exception as e:
            logger.error(f"Error generating general response: {str(e)}")
            return self._get_error_response(language)
    
    def _load_synthetic_knowledge(self) -> List[Dict[str, Any]]:
        """Load synthetic knowledge base data"""
        return [
            {
                'id': 'doc_001',
                'title': 'Eye Health Guidelines for Gujarat',
                'content': 'Regular eye examinations are crucial for early detection of conditions like cataracts and glaucoma. In Gujarat, the NPCB&VI program provides free eye screenings at Primary Health Centers. Common symptoms to watch for include blurred vision, eye pain, and difficulty seeing at night.',
                'region': 'gujarat',
                'domain': 'eye_health',
                'source': 'NPCB&VI Gujarat',
                'language': 'en'
            },
            {
                'id': 'doc_002',
                'title': 'Skin Care in Maharashtra Climate',
                'content': 'Maharashtra\'s humid climate can exacerbate skin conditions like eczema and fungal infections. Proper hygiene, use of antifungal powders, and wearing breathable clothing are recommended. Monsoon season requires extra care to prevent skin infections.',
                'region': 'maharashtra',
                'domain': 'skin_health',
                'source': 'Maharashtra Health Department',
                'language': 'en'
            },
            {
                'id': 'doc_003',
                'title': 'Diabetes and Eye Health',
                'content': 'Diabetic patients are at higher risk for diabetic retinopathy, a leading cause of blindness. Annual dilated eye exams are essential. Early symptoms include floaters, blurred vision, and dark spots in vision. Treatment options include laser therapy and injections.',
                'region': 'gujarat',
                'domain': 'eye_health',
                'source': 'Gujarat Diabetes Association',
                'language': 'en'
            },
            {
                'id': 'doc_004',
                'title': 'Cataract Surgery Guidelines',
                'content': 'Cataract surgery is one of the most successful procedures with 95% success rate. Post-operative care includes using prescribed eye drops, avoiding heavy lifting, and protecting eyes from bright light. Recovery typically takes 4-6 weeks.',
                'region': 'maharashtra',
                'domain': 'eye_health',
                'source': 'Maharashtra Ophthalmology Society',
                'language': 'en'
            },
            {
                'id': 'doc_005',
                'title': 'Skin Cancer Prevention',
                'content': 'Skin cancer prevention involves limiting sun exposure, using sunscreen with SPF 30+, wearing protective clothing, and regular skin self-examinations. Look for changes in moles, new growths, or sores that don\'t heal.',
                'region': 'gujarat',
                'domain': 'skin_health',
                'source': 'Gujarat Cancer Society',
                'language': 'en'
            }
        ]
    
    def _load_education_templates(self) -> Dict[str, str]:
        """Load patient education templates"""
        return {
            'diabetes': """
            **Understanding Diabetes and Your Health**
            
            Diabetes is a condition where your blood sugar levels are too high. Here's what you need to know:
            
            **Symptoms to Watch:**
            - Increased thirst and urination
            - Unexplained weight loss
            - Fatigue and blurred vision
            
            **Management Tips:**
            - Take medications as prescribed
            - Monitor blood sugar regularly
            - Follow a healthy diet
            - Exercise regularly
            - Get regular eye and foot checkups
            
            **When to Seek Help:**
            Contact your healthcare provider if you experience severe symptoms or blood sugar levels outside your target range.
            """,
            
            'hypertension': """
            **Managing High Blood Pressure**
            
            High blood pressure often has no symptoms but can lead to serious health problems.
            
            **Lifestyle Changes:**
            - Reduce salt intake
            - Maintain healthy weight
            - Exercise regularly
            - Limit alcohol consumption
            - Manage stress
            
            **Monitoring:**
            - Check blood pressure regularly
            - Take medications as prescribed
            - Keep a blood pressure log
            
            **Warning Signs:**
            Seek immediate medical attention for severe headaches, chest pain, or difficulty breathing.
            """,
            
            'cataract': """
            **Understanding Cataracts**
            
            Cataracts cause clouding of the eye's lens, leading to vision problems.
            
            **Symptoms:**
            - Blurry or cloudy vision
            - Difficulty seeing at night
            - Sensitivity to light
            - Seeing halos around lights
            
            **Treatment:**
            - Early stages: Updated glasses prescription
            - Advanced stages: Cataract surgery
            
            **Prevention:**
            - Wear sunglasses
            - Don't smoke
            - Eat foods rich in antioxidants
            - Get regular eye exams
            """,
            
            'general': """
            **General Health Information**
            
            Maintaining good health requires attention to both prevention and early detection of health issues.
            
            **Key Health Practices:**
            - Regular health checkups
            - Balanced diet and exercise
            - Adequate sleep and stress management
            - Avoiding tobacco and limiting alcohol
            
            **When to Consult a Healthcare Provider:**
            - Persistent symptoms
            - Changes in your health
            - Questions about medications
            - Preventive care needs
            
            For specific health concerns, please consult with a qualified healthcare professional.
            """
        }
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate relevance score between query and content"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        # Simple Jaccard similarity
        intersection = len(query_words.intersection(content_words))
        union = len(query_words.union(content_words))
        
        if union == 0:
            return 0.0
        
        base_score = intersection / union
        
        # Add some randomness for demonstration
        return min(1.0, base_score + random.uniform(0.1, 0.3))
    
    def _customize_education_content(self, template: str, region: str, language: str) -> str:
        """Customize education content for region and language"""
        content = template
        
        # Add region-specific information
        if region == 'gujarat':
            content += "\n\n**Local Resources in Gujarat:**\n"
            content += "- Contact your nearest Primary Health Center\n"
            content += "- Gujarat State Health Department: 079-23250646\n"
            content += "- Emergency services: 108\n"
        elif region == 'maharashtra':
            content += "\n\n**Local Resources in Maharashtra:**\n"
            content += "- Contact your nearest Primary Health Center\n"
            content += "- Maharashtra Health Department: 022-22010306\n"
            content += "- Emergency services: 108\n"
        
        # Language customization (simplified for demonstration)
        if language == 'gu':
            content += "\n\n*આ માહિતી ગુજરાતીમાં પણ ઉપલબ્ધ છે.*"
        elif language == 'mr':
            content += "\n\n*ही माहिती मराठीमध्ये देखील उपलब्ध आहे.*"
        
        return content
    
    def _generate_search_response(self, results: List[Dict], query: str, region: str, language: str) -> str:
        """Generate response based on search results"""
        response = f"Based on your query about '{query}', here's what I found:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            response += f"**{i}. {result['title']}**\n"
            response += f"{result['content']}\n"
            response += f"*Source: {result['source']}*\n\n"
        
        response += "Would you like more specific information about any of these topics?"
        
        return response
    
    def _get_no_results_response(self, language: str) -> str:
        """Get response when no search results found"""
        responses = {
            'en': "I couldn't find specific information about your query. Could you please rephrase your question or ask about a specific health condition?",
            'gu': "તમારા પ્રશ્ન વિશે મને ચોક્કસ માહિતી મળી નથી. કૃપા કરીને તમારો પ્રશ્ન ફરીથી પૂછો અથવા કોઈ ચોક્કસ સ્વાસ્થ્ય સ્થિતિ વિશે પૂછો?",
            'mr': "मला तुमच्या प्रश्नाबद्दल विशिष्ट माहिती सापडली नाही. कृपया तुमचा प्रश्न पुन्हा विचारा किंवा एखाद्या विशिष्ट आरोग्य स्थितीबद्दल विचारा?"
        }
        return responses.get(language, responses['en'])
    
    def _get_error_response(self, language: str) -> str:
        """Get error response"""
        responses = {
            'en': "I apologize, but I encountered an error processing your request. Please try again.",
            'gu': "માફ કરશો, તમારી વિનંતી પર કામ કરતી વખતે મને ભૂલ આવી છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.",
            'mr': "मी दिलगीर आहे, तुमची विनंती प्रक्रिया करताना मला त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा."
        }
        return responses.get(language, responses['en'])
    
    def _get_health_general_response(self, region: str, language: str) -> str:
        """Get general health response"""
        responses = {
            'en': f"I'm RHISA, your healthcare assistant for {region.title()}. I can help you with information about eye health, skin conditions, treatment guidelines, and patient education. What specific health topic would you like to know about?",
            'gu': f"હું RHISA છું, {region.title()} માટે તમારો આરોગ્ય સહાયક. હું તમને આંખના સ્વાસ્થ્ય, ચામડીની સમસ્યાઓ, સારવારની માર્ગદર્શિકા અને દર્દીઓની શિક્ષા વિશે માહિતી આપી શકું છું. તમે કયા ચોક્કસ આરોગ્ય વિષય વિશે જાણવા માંગો છો?",
            'mr': f"मी RHISA आहे, {region.title()} साठी तुमचा आरोग्य सहाyyक. मी तुम्हाला डोळ्यांच्या आरोग्याबद्दल, त्वचेच्या समस्यांबद्दल, उपचार मार्गदर्शकतत्त्वांबद्दल आणि रुग्ण शिक्षणाबद्दल माहिती देऊ शकतो. तुम्हाला कोणत्या विशिष्ट आरोग्य विषयाबद्दल जाणून घ्यायचे आहे?"
        }
        return responses.get(language, responses['en'])
    
    def _get_general_greeting_response(self, language: str) -> str:
        """Get general greeting response"""
        responses = {
            'en': "Hello! I'm RHISA, your Regional Health Insight & Support Agent. I'm here to help you with healthcare information for Gujarat and Maharashtra, including eye health, skin conditions, and general medical guidance. How can I assist you today?",
            'gu': "નમસ્તે! હું RHISA છું, તમારો પ્રાદેશિક આરોગ્ય અંતર્દૃષ્ટિ અને સહાયતા એજન્ટ. હું ગુજરાત અને મહારાષ્ટ્ર માટે આરોગ્ય માહિતી સાથે તમારી મદદ કરવા અહીં છું, જેમાં આંખના સ્વાસ્થ્ય, ચામડીની સ્થિતિ અને સામાન્ય તબીબી માર્ગદર્શન શામેલ છે. આજે હું તમારી કેવી રીતે મદદ કરી શકું?",
            'mr': "नमस्कार! मी RHISA आहे, तुमचा प्रादेशिक आरोग्य अंतर्दृष्टी आणि सहाय्य एजंट. मी गुजरात आणि महाराष्ट्रासाठी आरोग्य माहितीसह तुमची मदत करण्यासाठी येथे आहे, ज्यामध्ये डोळ्यांचे आरोग्य, त्वचेच्या स्थिती आणि सामान्य वैद्यकीय मार्गदर्शन समाविष्ट आहे. आज मी तुमची कशी मदत करू शकतो?"
        }
        return responses.get(language, responses['en'])