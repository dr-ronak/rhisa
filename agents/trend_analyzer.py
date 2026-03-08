"""
Trend Analyzer Agent for RHISA Healthcare Chatbot
Analyzes regional health trends and patterns
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    """Agent responsible for analyzing health trends and patterns"""
    
    def __init__(self):
        self.synthetic_data = self._load_synthetic_trend_data()
        self.trend_patterns = self._initialize_trend_patterns()
    
    def analyze_trends(self, region: str, condition: str) -> Dict[str, Any]:
        """Analyze health trends for specific region and condition"""
        try:
            # Get synthetic trend data
            trend_data = self._get_trend_data(region, condition)
            
            # Perform trend analysis
            analysis = {
                'region': region,
                'condition': condition,
                'time_period': '2023-2024',
                'trend_direction': trend_data['trend_direction'],
                'percentage_change': trend_data['percentage_change'],
                'current_prevalence': trend_data['current_prevalence'],
                'risk_factors': trend_data['risk_factors'],
                'seasonal_patterns': trend_data['seasonal_patterns'],
                'demographic_insights': trend_data['demographic_insights'],
                'recommendations': trend_data['recommendations']
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {str(e)}")
            return self._get_default_trend_analysis(region, condition)
    
    def analyze_and_explain(self, region: str, condition: str, language: str) -> str:
        """Analyze trends and provide explanation"""
        try:
            analysis = self.analyze_trends(region, condition)
            explanation = self._generate_trend_explanation(analysis, language)
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating trend explanation: {str(e)}")
            return self._get_error_response(language)
    
    def compare_regions(self, condition: str, regions: List[str]) -> Dict[str, Any]:
        """Compare health trends across multiple regions"""
        try:
            comparison = {
                'condition': condition,
                'regions': regions,
                'comparison_data': {}
            }
            
            for region in regions:
                trend_data = self.analyze_trends(region, condition)
                comparison['comparison_data'][region] = trend_data
            
            # Generate comparative insights
            comparison['insights'] = self._generate_comparative_insights(comparison['comparison_data'])
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing regions: {str(e)}")
            return {}
    
    def get_seasonal_analysis(self, region: str, condition: str) -> Dict[str, Any]:
        """Get seasonal analysis for specific condition"""
        try:
            seasonal_data = {
                'region': region,
                'condition': condition,
                'seasonal_patterns': {
                    'monsoon': self._get_seasonal_impact('monsoon', condition, region),
                    'winter': self._get_seasonal_impact('winter', condition, region),
                    'summer': self._get_seasonal_impact('summer', condition, region),
                    'post_monsoon': self._get_seasonal_impact('post_monsoon', condition, region)
                },
                'peak_months': self._get_peak_months(condition, region),
                'prevention_strategies': self._get_seasonal_prevention(condition, region)
            }
            
            return seasonal_data
            
        except Exception as e:
            logger.error(f"Error getting seasonal analysis: {str(e)}")
            return {}
    
    def _load_synthetic_trend_data(self) -> Dict[str, Any]:
        """Load synthetic trend data"""
        return {
            'gujarat': {
                'eye_health': {
                    'cataract': {
                        'trend_direction': 'increasing',
                        'percentage_change': 12.5,
                        'current_prevalence': 8.2,
                        'risk_factors': ['aging population', 'diabetes', 'UV exposure'],
                        'seasonal_patterns': {
                            'summer': 'higher incidence due to UV exposure',
                            'monsoon': 'stable',
                            'winter': 'slight decrease'
                        },
                        'demographic_insights': {
                            'age_group_most_affected': '60+',
                            'gender_distribution': {'male': 45, 'female': 55},
                            'rural_vs_urban': {'rural': 65, 'urban': 35}
                        },
                        'recommendations': [
                            'Increase awareness campaigns in rural areas',
                            'Expand cataract surgery capacity',
                            'Promote UV protection measures'
                        ]
                    },
                    'glaucoma': {
                        'trend_direction': 'stable',
                        'percentage_change': 2.1,
                        'current_prevalence': 3.8,
                        'risk_factors': ['family history', 'high eye pressure', 'age'],
                        'seasonal_patterns': {
                            'summer': 'stable',
                            'monsoon': 'slight increase in acute cases',
                            'winter': 'stable'
                        },
                        'demographic_insights': {
                            'age_group_most_affected': '50+',
                            'gender_distribution': {'male': 52, 'female': 48},
                            'rural_vs_urban': {'rural': 40, 'urban': 60}
                        },
                        'recommendations': [
                            'Regular eye pressure screening',
                            'Early detection programs',
                            'Patient education on compliance'
                        ]
                    }
                },
                'skin_health': {
                    'dermatitis': {
                        'trend_direction': 'increasing',
                        'percentage_change': 18.3,
                        'current_prevalence': 15.6,
                        'risk_factors': ['humidity', 'occupational exposure', 'allergies'],
                        'seasonal_patterns': {
                            'summer': 'peak incidence',
                            'monsoon': 'highest cases due to humidity',
                            'winter': 'lowest incidence'
                        },
                        'demographic_insights': {
                            'age_group_most_affected': '20-40',
                            'gender_distribution': {'male': 48, 'female': 52},
                            'rural_vs_urban': {'rural': 70, 'urban': 30}
                        },
                        'recommendations': [
                            'Improve workplace safety measures',
                            'Promote proper hygiene practices',
                            'Increase access to dermatological care'
                        ]
                    }
                }
            },
            'maharashtra': {
                'eye_health': {
                    'cataract': {
                        'trend_direction': 'stable',
                        'percentage_change': 5.2,
                        'current_prevalence': 7.8,
                        'risk_factors': ['aging population', 'diabetes', 'pollution'],
                        'seasonal_patterns': {
                            'summer': 'moderate increase',
                            'monsoon': 'stable',
                            'winter': 'slight decrease'
                        },
                        'demographic_insights': {
                            'age_group_most_affected': '65+',
                            'gender_distribution': {'male': 42, 'female': 58},
                            'rural_vs_urban': {'rural': 55, 'urban': 45}
                        },
                        'recommendations': [
                            'Strengthen urban eye care services',
                            'Address pollution-related risk factors',
                            'Improve diabetes management'
                        ]
                    }
                },
                'skin_health': {
                    'fungal_infections': {
                        'trend_direction': 'increasing',
                        'percentage_change': 22.7,
                        'current_prevalence': 18.9,
                        'risk_factors': ['humidity', 'poor hygiene', 'overcrowding'],
                        'seasonal_patterns': {
                            'summer': 'high incidence',
                            'monsoon': 'peak cases',
                            'winter': 'significant decrease'
                        },
                        'demographic_insights': {
                            'age_group_most_affected': 'all ages',
                            'gender_distribution': {'male': 55, 'female': 45},
                            'rural_vs_urban': {'rural': 45, 'urban': 55}
                        },
                        'recommendations': [
                            'Improve sanitation facilities',
                            'Public health education campaigns',
                            'Increase antifungal medication availability'
                        ]
                    }
                }
            }
        }
    
    def _initialize_trend_patterns(self) -> Dict[str, Any]:
        """Initialize trend pattern templates"""
        return {
            'increasing': {
                'description': 'showing an upward trend',
                'concern_level': 'moderate to high',
                'action_required': 'immediate attention needed'
            },
            'decreasing': {
                'description': 'showing a downward trend',
                'concern_level': 'low to moderate',
                'action_required': 'continue current interventions'
            },
            'stable': {
                'description': 'remaining relatively stable',
                'concern_level': 'low',
                'action_required': 'maintain current monitoring'
            }
        }
    
    def _get_trend_data(self, region: str, condition: str) -> Dict[str, Any]:
        """Get trend data for specific region and condition"""
        try:
            # Navigate through synthetic data structure
            region_data = self.synthetic_data.get(region.lower(), {})
            
            # Try to find condition in eye_health or skin_health
            for domain in ['eye_health', 'skin_health']:
                domain_data = region_data.get(domain, {})
                if condition.lower() in domain_data:
                    return domain_data[condition.lower()]
            
            # If specific condition not found, return generic data
            return self._generate_generic_trend_data(region, condition)
            
        except Exception as e:
            logger.error(f"Error getting trend data: {str(e)}")
            return self._generate_generic_trend_data(region, condition)
    
    def _generate_generic_trend_data(self, region: str, condition: str) -> Dict[str, Any]:
        """Generate generic trend data for unknown conditions"""
        return {
            'trend_direction': random.choice(['increasing', 'stable', 'decreasing']),
            'percentage_change': round(random.uniform(-5, 20), 1),
            'current_prevalence': round(random.uniform(2, 15), 1),
            'risk_factors': ['genetic factors', 'environmental factors', 'lifestyle factors'],
            'seasonal_patterns': {
                'summer': 'variable',
                'monsoon': 'variable',
                'winter': 'variable'
            },
            'demographic_insights': {
                'age_group_most_affected': 'adults',
                'gender_distribution': {'male': 50, 'female': 50},
                'rural_vs_urban': {'rural': 50, 'urban': 50}
            },
            'recommendations': [
                'Increase awareness and education',
                'Improve access to healthcare services',
                'Conduct further research on risk factors'
            ]
        }
    
    def _generate_trend_explanation(self, analysis: Dict[str, Any], language: str) -> str:
        """Generate human-readable trend explanation"""
        try:
            region = analysis['region'].title()
            condition = analysis['condition'].title()
            trend_direction = analysis['trend_direction']
            percentage_change = analysis['percentage_change']
            prevalence = analysis['current_prevalence']
            
            explanation = f"**Health Trend Analysis for {condition} in {region}**\n\n"
            
            # Trend overview
            if trend_direction == 'increasing':
                explanation += f"📈 The incidence of {condition} is **increasing** by {percentage_change}% compared to the previous year. "
            elif trend_direction == 'decreasing':
                explanation += f"📉 The incidence of {condition} is **decreasing** by {abs(percentage_change)}% compared to the previous year. "
            else:
                explanation += f"📊 The incidence of {condition} remains **stable** with only a {percentage_change}% change. "
            
            explanation += f"Current prevalence is {prevalence}% of the population.\n\n"
            
            # Risk factors
            explanation += "**Key Risk Factors:**\n"
            for factor in analysis['risk_factors']:
                explanation += f"• {factor.title()}\n"
            explanation += "\n"
            
            # Demographic insights
            demo = analysis['demographic_insights']
            explanation += "**Demographic Patterns:**\n"
            explanation += f"• Most affected age group: {demo['age_group_most_affected']}\n"
            explanation += f"• Gender distribution: {demo['gender_distribution']['female']}% female, {demo['gender_distribution']['male']}% male\n"
            explanation += f"• Geographic distribution: {demo['rural_vs_urban']['rural']}% rural, {demo['rural_vs_urban']['urban']}% urban\n\n"
            
            # Seasonal patterns
            explanation += "**Seasonal Patterns:**\n"
            for season, pattern in analysis['seasonal_patterns'].items():
                explanation += f"• {season.title()}: {pattern}\n"
            explanation += "\n"
            
            # Recommendations
            explanation += "**Recommended Actions:**\n"
            for i, rec in enumerate(analysis['recommendations'], 1):
                explanation += f"{i}. {rec}\n"
            
            explanation += "\n*This analysis is based on synthetic data for demonstration purposes.*"
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return self._get_error_response(language)
    
    def _generate_comparative_insights(self, comparison_data: Dict[str, Any]) -> List[str]:
        """Generate insights from regional comparison"""
        insights = []
        
        try:
            regions = list(comparison_data.keys())
            if len(regions) >= 2:
                region1, region2 = regions[0], regions[1]
                data1 = comparison_data[region1]
                data2 = comparison_data[region2]
                
                # Compare prevalence
                if data1['current_prevalence'] > data2['current_prevalence']:
                    insights.append(f"{region1.title()} has higher prevalence ({data1['current_prevalence']}%) compared to {region2.title()} ({data2['current_prevalence']}%)")
                else:
                    insights.append(f"{region2.title()} has higher prevalence ({data2['current_prevalence']}%) compared to {region1.title()} ({data1['current_prevalence']}%)")
                
                # Compare trends
                if data1['trend_direction'] != data2['trend_direction']:
                    insights.append(f"Trend directions differ: {region1.title()} is {data1['trend_direction']} while {region2.title()} is {data2['trend_direction']}")
                
                # Compare rural vs urban distribution
                rural1 = data1['demographic_insights']['rural_vs_urban']['rural']
                rural2 = data2['demographic_insights']['rural_vs_urban']['rural']
                
                if abs(rural1 - rural2) > 10:
                    if rural1 > rural2:
                        insights.append(f"{region1.title()} shows higher rural prevalence ({rural1}%) compared to {region2.title()} ({rural2}%)")
                    else:
                        insights.append(f"{region2.title()} shows higher rural prevalence ({rural2}%) compared to {region1.title()} ({rural1}%)")
        
        except Exception as e:
            logger.error(f"Error generating comparative insights: {str(e)}")
            insights.append("Unable to generate comparative insights due to data limitations")
        
        return insights
    
    def _get_seasonal_impact(self, season: str, condition: str, region: str) -> str:
        """Get seasonal impact description"""
        seasonal_impacts = {
            'monsoon': {
                'skin_health': 'High humidity increases fungal and bacterial infections',
                'eye_health': 'Increased risk of conjunctivitis and eye infections'
            },
            'summer': {
                'skin_health': 'Heat and sun exposure increase dermatitis and sunburn',
                'eye_health': 'UV exposure increases cataract and pterygium risk'
            },
            'winter': {
                'skin_health': 'Dry air causes eczema and skin dryness',
                'eye_health': 'Generally lower incidence of most conditions'
            },
            'post_monsoon': {
                'skin_health': 'Continued humidity effects with vector-borne diseases',
                'eye_health': 'Gradual normalization of infection rates'
            }
        }
        
        # Determine domain based on condition
        domain = 'eye_health' if condition.lower() in ['cataract', 'glaucoma', 'conjunctivitis'] else 'skin_health'
        
        return seasonal_impacts.get(season, {}).get(domain, 'Variable seasonal impact')
    
    def _get_peak_months(self, condition: str, region: str) -> List[str]:
        """Get peak months for specific condition"""
        peak_patterns = {
            'dermatitis': ['June', 'July', 'August'],
            'fungal_infections': ['July', 'August', 'September'],
            'cataract': ['April', 'May', 'June'],
            'conjunctivitis': ['June', 'July', 'August']
        }
        
        return peak_patterns.get(condition.lower(), ['Variable throughout year'])
    
    def _get_seasonal_prevention(self, condition: str, region: str) -> List[str]:
        """Get seasonal prevention strategies"""
        prevention_strategies = {
            'dermatitis': [
                'Use antifungal powders during monsoon',
                'Wear breathable clothing',
                'Maintain proper hygiene'
            ],
            'fungal_infections': [
                'Keep skin dry during humid weather',
                'Use antifungal soaps',
                'Avoid sharing personal items'
            ],
            'cataract': [
                'Wear UV-protective sunglasses',
                'Avoid direct sun exposure during peak hours',
                'Regular eye checkups'
            ]
        }
        
        return prevention_strategies.get(condition.lower(), ['Follow general health guidelines'])
    
    def _get_default_trend_analysis(self, region: str, condition: str) -> Dict[str, Any]:
        """Get default trend analysis when data is unavailable"""
        return {
            'region': region,
            'condition': condition,
            'time_period': '2023-2024',
            'trend_direction': 'stable',
            'percentage_change': 0.0,
            'current_prevalence': 5.0,
            'risk_factors': ['various factors'],
            'seasonal_patterns': {'all_seasons': 'data not available'},
            'demographic_insights': {
                'age_group_most_affected': 'adults',
                'gender_distribution': {'male': 50, 'female': 50},
                'rural_vs_urban': {'rural': 50, 'urban': 50}
            },
            'recommendations': ['Collect more data for accurate analysis']
        }
    
    def _get_error_response(self, language: str) -> str:
        """Get error response in specified language"""
        responses = {
            'en': "I apologize, but I encountered an error while analyzing the health trends. Please try again.",
            'gu': "માફ કરશો, આરોગ્ય વલણોનું વિશ્લેષણ કરતી વખતે મને ભૂલ આવી છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.",
            'mr': "मी दिलगीर आहे, आरोग्य ट्रेंडचे विश्लेषण करताना मला त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा."
        }
        return responses.get(language, responses['en'])