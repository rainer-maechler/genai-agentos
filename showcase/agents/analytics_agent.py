#!/usr/bin/env python3
"""
Analytics Agent for GenAI AgentOS Showcase

This agent performs deep content analysis on structured text.
Capabilities:
- Key topic identification
- Statistical analysis
- Risk factor detection
- Compliance checking
- Business metrics extraction
- Trend analysis
"""

import asyncio
import json
import re
from typing import Dict, Any, List
from datetime import datetime
from collections import Counter
from loguru import logger

# Text processing imports
from textblob import TextBlob

# GenAI Protocol
from genai_protocol import GenAISession


class AnalyticsAgent:
    """Agent that performs comprehensive content analysis."""
    
    def __init__(self):
        self.name = "analytics_agent"
        self.description = "Performs deep content analysis, risk assessment, and business intelligence"
        self.version = "1.0.0"
        
        # Risk keywords and patterns
        self.risk_keywords = {
            'financial': ['budget', 'cost', 'expensive', 'overrun', 'deficit', 'loss', 'debt', 'liability'],
            'operational': ['delay', 'bottleneck', 'failure', 'breakdown', 'issue', 'problem', 'challenge'],
            'compliance': ['violation', 'breach', 'non-compliant', 'audit', 'regulatory', 'legal'],
            'security': ['breach', 'vulnerability', 'threat', 'attack', 'unauthorized', 'hack'],
            'reputation': ['negative', 'criticism', 'complaint', 'dissatisfied', 'poor', 'bad'],
            'market': ['competition', 'disruption', 'decline', 'recession', 'volatility', 'uncertainty']
        }
        
        # Positive indicators
        self.positive_keywords = {
            'growth': ['increase', 'growth', 'expansion', 'improvement', 'enhancement', 'boost'],
            'success': ['success', 'achievement', 'accomplished', 'exceeded', 'outstanding', 'excellent'],
            'innovation': ['innovative', 'breakthrough', 'cutting-edge', 'advanced', 'revolutionary'],
            'efficiency': ['efficient', 'streamlined', 'optimized', 'automated', 'faster', 'improved'],
            'financial': ['profit', 'revenue', 'savings', 'roi', 'return', 'benefit', 'value']
        }
        
        # Business metrics patterns
        self.metric_patterns = {
            'percentage': re.compile(r'(\d+(?:\.\d+)?)\s*%'),
            'currency': re.compile(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:million|billion|M|B)?', re.IGNORECASE),
            'timeline': re.compile(r'(\d+)\s*(month|year|week|day|quarter)s?', re.IGNORECASE),
            'roi': re.compile(r'(?:ROI|return)\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\s*%?', re.IGNORECASE),
            'efficiency': re.compile(r'(?:efficiency|productivity|performance)\s*(?:increase|improvement|boost)\s*(?:of|by)?\s*(\d+(?:\.\d+)?)\s*%?', re.IGNORECASE)
        }
        
        # Compliance frameworks
        self.compliance_frameworks = {
            'gdpr': ['personal data', 'privacy', 'consent', 'data protection', 'gdpr'],
            'sox': ['financial reporting', 'internal controls', 'sarbanes-oxley', 'sox'],
            'hipaa': ['patient data', 'health information', 'medical records', 'hipaa'],
            'pci': ['payment card', 'credit card', 'cardholder data', 'pci-dss'],
            'iso27001': ['information security', 'security management', 'iso 27001'],
            'iso9001': ['quality management', 'quality standards', 'iso 9001']
        }
    
    async def process_message(self, session: GenAISession, message: str) -> Dict[str, Any]:
        """Process incoming message and perform analytics."""
        try:
            # Parse the input message
            request = json.loads(message)
            
            # Extract data from previous agent
            cleaned_text = request.get('cleaned_text', '')
            entities = request.get('entities', {})
            sections = request.get('sections', [])
            key_phrases = request.get('key_phrases', {})
            statistics = request.get('statistics', {})
            
            if not cleaned_text:
                return {
                    "error": "No cleaned text provided",
                    "status": "error"
                }
            
            # Perform comprehensive analysis
            result = await self._perform_analytics(
                cleaned_text, entities, sections, key_phrases, statistics
            )
            
            # Add agent metadata
            result.update({
                "agent": self.name,
                "analyzed_at": datetime.now().isoformat(),
                "status": "success"
            })
            
            logger.info(f"Successfully analyzed content ({len(cleaned_text)} chars)")
            return result
            
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input", "status": "error"}
        except Exception as e:
            logger.error(f"Error performing analytics: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _perform_analytics(
        self, 
        text: str, 
        entities: Dict, 
        sections: List[Dict], 
        key_phrases: Dict, 
        statistics: Dict
    ) -> Dict[str, Any]:
        """Perform comprehensive analytics on the content."""
        
        # Topic analysis
        topics = self._analyze_topics(text, key_phrases)
        
        # Risk assessment
        risk_analysis = self._analyze_risks(text, entities)
        
        # Business metrics extraction
        business_metrics = self._extract_business_metrics(text, entities)
        
        # Compliance analysis
        compliance_analysis = self._analyze_compliance(text)
        
        # Sentiment and tone analysis
        sentiment_analysis = self._analyze_sentiment_and_tone(text)
        
        # Content quality assessment
        quality_assessment = self._assess_content_quality(text, sections, statistics)
        
        # Trend and pattern analysis
        trend_analysis = self._analyze_trends(text, entities)
        
        # Generate insights and recommendations
        insights = self._generate_insights(
            topics, risk_analysis, business_metrics, 
            compliance_analysis, sentiment_analysis
        )
        
        return {
            "topics": topics,
            "risk_analysis": risk_analysis,
            "business_metrics": business_metrics,
            "compliance": compliance_analysis,
            "sentiment_tone": sentiment_analysis,
            "quality_assessment": quality_assessment,
            "trends": trend_analysis,
            "insights": insights,
            "analysis_summary": self._create_summary(
                topics, risk_analysis, business_metrics, insights
            )
        }
    
    def _analyze_topics(self, text: str, key_phrases: Dict) -> Dict[str, Any]:
        """Analyze main topics and themes."""
        # Use key phrases as starting point
        phrases = key_phrases.get('noun_phrases', [])
        phrase_freq = key_phrases.get('phrase_frequencies', {})
        
        # Categorize topics
        topic_categories = {
            'business': ['business', 'company', 'organization', 'corporate', 'enterprise'],
            'financial': ['financial', 'money', 'cost', 'budget', 'revenue', 'profit'],
            'technology': ['technology', 'digital', 'software', 'system', 'platform'],
            'operational': ['operation', 'process', 'workflow', 'procedure', 'management'],
            'strategy': ['strategy', 'plan', 'objective', 'goal', 'vision', 'mission'],
            'market': ['market', 'customer', 'client', 'competition', 'industry'],
            'project': ['project', 'initiative', 'implementation', 'development', 'deployment']
        }
        
        categorized_topics = {}
        for category, keywords in topic_categories.items():
            category_phrases = []
            for phrase in phrases:
                if any(keyword in phrase.lower() for keyword in keywords):
                    category_phrases.append(phrase)
            if category_phrases:
                categorized_topics[category] = category_phrases[:5]  # Top 5 per category
        
        # Extract main themes
        word_freq = Counter(text.lower().split())
        common_words = [word for word, count in word_freq.most_common(20) 
                       if len(word) > 3 and word.isalpha()]
        
        return {
            "categorized_topics": categorized_topics,
            "top_phrases": phrases[:10],
            "common_themes": common_words[:10],
            "topic_diversity": len(categorized_topics),
            "primary_focus": max(categorized_topics.keys(), 
                               key=lambda k: len(categorized_topics[k])) if categorized_topics else "general"
        }
    
    def _analyze_risks(self, text: str, entities: Dict) -> Dict[str, Any]:
        """Analyze potential risks and concerns."""
        text_lower = text.lower()
        detected_risks = {}
        risk_score = 0
        
        # Check for risk keywords
        for risk_category, keywords in self.risk_keywords.items():
            found_keywords = [kw for kw in keywords if kw in text_lower]
            if found_keywords:
                detected_risks[risk_category] = {
                    "keywords": found_keywords,
                    "count": sum(text_lower.count(kw) for kw in found_keywords),
                    "severity": "high" if len(found_keywords) > 3 else "medium" if len(found_keywords) > 1 else "low"
                }
                risk_score += len(found_keywords)
        
        # Financial risk indicators
        financial_risks = []
        if 'currency' in entities:
            amounts = entities['currency']
            large_amounts = [amt for amt in amounts if any(char.isdigit() and int(''.join(filter(str.isdigit, amt))) > 1000000 for char in amt)]
            if large_amounts:
                financial_risks.append("Large financial commitments identified")
        
        if 'percentage' in entities:
            percentages = entities['percentage']
            high_percentages = [pct for pct in percentages if any(char.isdigit() and int(''.join(filter(str.isdigit, pct))) > 50 for char in pct)]
            if high_percentages:
                financial_risks.append("High percentage changes noted")
        
        # Timeline risks
        timeline_risks = []
        if 'timelines' in entities:
            timelines = entities['timelines']
            long_timelines = [tl for tl in timelines if 'year' in tl.lower()]
            if long_timelines:
                timeline_risks.append("Long-term commitments identified")
        
        # Overall risk assessment
        overall_risk = "low"
        if risk_score > 10:
            overall_risk = "high"
        elif risk_score > 5:
            overall_risk = "medium"
        
        return {
            "detected_risks": detected_risks,
            "financial_risks": financial_risks,
            "timeline_risks": timeline_risks,
            "risk_score": risk_score,
            "overall_risk_level": overall_risk,
            "risk_factors_count": len(detected_risks),
            "recommendations": self._generate_risk_recommendations(detected_risks, risk_score)
        }
    
    def _extract_business_metrics(self, text: str, entities: Dict) -> Dict[str, Any]:
        """Extract and analyze business metrics."""
        metrics = {}
        
        # Extract metrics using patterns
        for metric_type, pattern in self.metric_patterns.items():
            matches = pattern.findall(text)
            if matches:
                if metric_type == 'currency':
                    # Parse currency values
                    values = []
                    for match in matches:
                        try:
                            value = float(match.replace(',', ''))
                            values.append(value)
                        except ValueError:
                            continue
                    if values:
                        metrics[metric_type] = {
                            "values": values,
                            "total": sum(values),
                            "average": sum(values) / len(values),
                            "max": max(values),
                            "min": min(values)
                        }
                else:
                    metrics[metric_type] = matches
        
        # ROI Analysis
        roi_indicators = []
        if 'roi' in entities:
            roi_indicators.extend(entities['roi'])
        if 'roi' in metrics:
            roi_indicators.extend(metrics['roi'])
        
        # Performance indicators
        performance_indicators = self._extract_performance_indicators(text)
        
        # Growth indicators
        growth_indicators = self._extract_growth_indicators(text)
        
        return {
            "extracted_metrics": metrics,
            "roi_indicators": list(set(roi_indicators)),
            "performance_indicators": performance_indicators,
            "growth_indicators": growth_indicators,
            "has_financial_data": 'currency' in metrics or 'currency' in entities,
            "has_performance_data": bool(performance_indicators),
            "metrics_confidence": "high" if len(metrics) > 2 else "medium" if metrics else "low"
        }
    
    def _analyze_compliance(self, text: str) -> Dict[str, Any]:
        """Analyze compliance-related content."""
        text_lower = text.lower()
        compliance_matches = {}
        
        for framework, keywords in self.compliance_frameworks.items():
            found_keywords = [kw for kw in keywords if kw in text_lower]
            if found_keywords:
                compliance_matches[framework] = {
                    "keywords": found_keywords,
                    "mentions": sum(text_lower.count(kw) for kw in found_keywords),
                    "relevance": "high" if len(found_keywords) > 2 else "medium"
                }
        
        # General compliance indicators
        compliance_terms = ['compliant', 'compliance', 'regulation', 'standard', 'audit', 'certification']
        compliance_mentions = sum(text_lower.count(term) for term in compliance_terms)
        
        return {
            "framework_matches": compliance_matches,
            "compliance_mentions": compliance_mentions,
            "frameworks_identified": list(compliance_matches.keys()),
            "compliance_focus": "high" if compliance_mentions > 5 else "medium" if compliance_mentions > 2 else "low",
            "recommendations": self._generate_compliance_recommendations(compliance_matches)
        }
    
    def _analyze_sentiment_and_tone(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment and tone of the content."""
        try:
            blob = TextBlob(text)
            
            # Overall sentiment
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Categorize sentiment
            if polarity > 0.3:
                sentiment_label = "positive"
            elif polarity < -0.3:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            # Analyze tone indicators
            tone_analysis = self._analyze_tone(text)
            
            # Confidence analysis
            confidence_indicators = self._analyze_confidence(text)
            
            return {
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "sentiment_label": sentiment_label,
                "tone": tone_analysis,
                "confidence_indicators": confidence_indicators,
                "emotional_intensity": "high" if abs(polarity) > 0.5 else "medium" if abs(polarity) > 0.2 else "low"
            }
            
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {str(e)}")
            return {
                "polarity": 0.0,
                "subjectivity": 0.0,
                "sentiment_label": "neutral",
                "error": "Sentiment analysis unavailable"
            }
    
    def _analyze_tone(self, text: str) -> Dict[str, Any]:
        """Analyze the tone of the document."""
        text_lower = text.lower()
        
        tone_indicators = {
            'professional': ['professional', 'business', 'formal', 'official', 'corporate'],
            'confident': ['confident', 'certain', 'assured', 'definite', 'strong'],
            'cautious': ['careful', 'cautious', 'conservative', 'prudent', 'careful'],
            'urgent': ['urgent', 'immediate', 'critical', 'important', 'asap'],
            'optimistic': ['optimistic', 'positive', 'hopeful', 'promising', 'bright'],
            'analytical': ['analysis', 'data', 'research', 'study', 'examination']
        }
        
        detected_tones = {}
        for tone, keywords in tone_indicators.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            if count > 0:
                detected_tones[tone] = count
        
        primary_tone = max(detected_tones.keys(), key=detected_tones.get) if detected_tones else "neutral"
        
        return {
            "detected_tones": detected_tones,
            "primary_tone": primary_tone,
            "tone_strength": max(detected_tones.values()) if detected_tones else 0
        }
    
    def _analyze_confidence(self, text: str) -> Dict[str, Any]:
        """Analyze confidence indicators in the text."""
        text_lower = text.lower()
        
        high_confidence = ['will', 'definitely', 'certainly', 'guaranteed', 'ensure', 'confirm']
        medium_confidence = ['likely', 'probably', 'expected', 'anticipated', 'should']
        low_confidence = ['might', 'maybe', 'possibly', 'perhaps', 'could', 'may']
        
        high_count = sum(text_lower.count(word) for word in high_confidence)
        medium_count = sum(text_lower.count(word) for word in medium_confidence)
        low_count = sum(text_lower.count(word) for word in low_confidence)
        
        total_indicators = high_count + medium_count + low_count
        
        if total_indicators == 0:
            confidence_level = "neutral"
        elif high_count > medium_count and high_count > low_count:
            confidence_level = "high"
        elif low_count > high_count and low_count > medium_count:
            confidence_level = "low"
        else:
            confidence_level = "medium"
        
        return {
            "high_confidence_indicators": high_count,
            "medium_confidence_indicators": medium_count, 
            "low_confidence_indicators": low_count,
            "overall_confidence": confidence_level,
            "confidence_score": (high_count * 2 + medium_count - low_count) / max(total_indicators, 1)
        }
    
    def _assess_content_quality(self, text: str, sections: List[Dict], statistics: Dict) -> Dict[str, Any]:
        """Assess the quality of the content."""
        quality_score = 0
        quality_factors = []
        
        # Structure quality
        if len(sections) > 1:
            quality_score += 20
            quality_factors.append("Well-structured with multiple sections")
        
        # Length appropriateness
        word_count = statistics.get('word_count', 0)
        if 500 <= word_count <= 5000:
            quality_score += 15
            quality_factors.append("Appropriate length")
        elif word_count > 5000:
            quality_score += 10
            quality_factors.append("Comprehensive content")
        
        # Lexical diversity
        lexical_diversity = statistics.get('lexical_diversity', 0)
        if lexical_diversity > 0.5:
            quality_score += 15
            quality_factors.append("Good vocabulary diversity")
        elif lexical_diversity > 0.3:
            quality_score += 10
            quality_factors.append("Adequate vocabulary diversity")
        
        # Reading ease
        avg_sentence_length = statistics.get('average_words_per_sentence', 0)
        if 10 <= avg_sentence_length <= 20:
            quality_score += 15
            quality_factors.append("Good sentence length")
        elif avg_sentence_length > 0:
            quality_score += 5
            quality_factors.append("Acceptable sentence structure")
        
        # Content completeness
        if any('summary' in section['title'].lower() for section in sections):
            quality_score += 10
            quality_factors.append("Contains summary section")
        
        if any('conclusion' in section['title'].lower() for section in sections):
            quality_score += 10
            quality_factors.append("Contains conclusion")
        
        # Professional indicators
        professional_terms = ['analysis', 'methodology', 'results', 'recommendations', 'objective']
        professional_count = sum(text.lower().count(term) for term in professional_terms)
        if professional_count > 5:
            quality_score += 15
            quality_factors.append("Professional terminology")
        
        quality_level = "excellent" if quality_score >= 80 else "good" if quality_score >= 60 else "fair" if quality_score >= 40 else "needs improvement"
        
        return {
            "quality_score": min(quality_score, 100),
            "quality_level": quality_level,
            "quality_factors": quality_factors,
            "improvement_areas": self._identify_improvement_areas(quality_score, statistics)
        }
    
    def _analyze_trends(self, text: str, entities: Dict) -> Dict[str, Any]:
        """Analyze trends and patterns in the content."""
        # Time-based trends
        dates = entities.get('date', [])
        time_indicators = entities.get('time', [])
        
        # Growth trends
        growth_words = ['increase', 'growth', 'rise', 'expand', 'improve', 'enhance']
        decline_words = ['decrease', 'decline', 'fall', 'reduce', 'drop', 'shrink']
        
        growth_mentions = sum(text.lower().count(word) for word in growth_words)
        decline_mentions = sum(text.lower().count(word) for word in decline_words)
        
        trend_direction = "positive" if growth_mentions > decline_mentions else "negative" if decline_mentions > growth_mentions else "stable"
        
        # Future orientation
        future_words = ['will', 'future', 'next', 'upcoming', 'planned', 'expected']
        future_mentions = sum(text.lower().count(word) for word in future_words)
        
        return {
            "trend_direction": trend_direction,
            "growth_indicators": growth_mentions,
            "decline_indicators": decline_mentions,
            "future_orientation": "high" if future_mentions > 10 else "medium" if future_mentions > 5 else "low",
            "temporal_references": len(dates) + len(time_indicators),
            "trend_strength": abs(growth_mentions - decline_mentions)
        }
    
    def _extract_performance_indicators(self, text: str) -> List[str]:
        """Extract performance-related indicators."""
        performance_patterns = [
            r'(\d+(?:\.\d+)?%)\s*(?:increase|improvement|growth)',
            r'(?:efficiency|productivity|performance)\s*(?:up|increased)\s*(?:by\s*)?(\d+(?:\.\d+)?%?)',
            r'(?:reduced|decreased)\s*(?:by\s*)?(\d+(?:\.\d+)?%?)',
            r'(?:achieved|reached|exceeded)\s*(\d+(?:\.\d+)?%?)'
        ]
        
        indicators = []
        for pattern in performance_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return indicators[:10]  # Return top 10
    
    def _extract_growth_indicators(self, text: str) -> List[str]:
        """Extract growth-related indicators."""
        growth_patterns = [
            r'(\d+(?:\.\d+)?%)\s*growth',
            r'revenue\s*(?:increased|grew)\s*(?:by\s*)?(\$[\d,]+(?:\.\d+)?[MBmb]?)',
            r'market\s*share\s*(?:increased|grew)\s*(?:by\s*)?(\d+(?:\.\d+)?%?)',
            r'customer\s*base\s*(?:grew|increased)\s*(?:by\s*)?(\d+(?:\.\d+)?%?)'
        ]
        
        indicators = []
        for pattern in growth_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            indicators.extend(matches)
        
        return indicators[:10]  # Return top 10
    
    def _generate_risk_recommendations(self, risks: Dict, score: int) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []
        
        if 'financial' in risks:
            recommendations.append("Consider detailed financial risk assessment and mitigation strategies")
        
        if 'operational' in risks:
            recommendations.append("Implement operational risk monitoring and contingency planning")
        
        if 'compliance' in risks:
            recommendations.append("Ensure compliance review with legal team")
        
        if score > 10:
            recommendations.append("High risk factors detected - recommend comprehensive risk analysis")
        
        if not recommendations:
            recommendations.append("Risk levels appear manageable based on current analysis")
        
        return recommendations
    
    def _generate_compliance_recommendations(self, compliance_matches: Dict) -> List[str]:
        """Generate compliance-related recommendations."""
        recommendations = []
        
        for framework in compliance_matches.keys():
            if framework == 'gdpr':
                recommendations.append("Ensure GDPR compliance for data handling and privacy")
            elif framework == 'sox':
                recommendations.append("Review financial reporting controls per SOX requirements")
            elif framework == 'hipaa':
                recommendations.append("Verify HIPAA compliance for health information handling")
        
        if not recommendations:
            recommendations.append("No specific compliance frameworks identified")
        
        return recommendations
    
    def _identify_improvement_areas(self, quality_score: int, statistics: Dict) -> List[str]:
        """Identify areas for content improvement."""
        improvements = []
        
        if quality_score < 60:
            improvements.append("Overall content structure and organization")
        
        lexical_diversity = statistics.get('lexical_diversity', 0)
        if lexical_diversity < 0.3:
            improvements.append("Vocabulary diversity and word choice")
        
        avg_sentence_length = statistics.get('average_words_per_sentence', 0)
        if avg_sentence_length > 25:
            improvements.append("Sentence length and readability")
        elif avg_sentence_length < 8:
            improvements.append("Sentence structure and complexity")
        
        if not improvements:
            improvements.append("Content quality is satisfactory")
        
        return improvements
    
    def _generate_insights(
        self, 
        topics: Dict, 
        risks: Dict, 
        metrics: Dict, 
        compliance: Dict, 
        sentiment: Dict
    ) -> Dict[str, Any]:
        """Generate comprehensive insights from the analysis."""
        insights = {
            "key_findings": [],
            "recommendations": [],
            "opportunities": [],
            "concerns": []
        }
        
        # Key findings
        primary_focus = topics.get('primary_focus', 'general')
        insights["key_findings"].append(f"Primary document focus: {primary_focus}")
        
        if metrics.get('has_financial_data'):
            insights["key_findings"].append("Contains significant financial information")
        
        if risks.get('overall_risk_level') != 'low':
            insights["key_findings"].append(f"Risk level assessed as: {risks.get('overall_risk_level')}")
        
        # Recommendations
        if sentiment.get('sentiment_label') == 'negative':
            insights["recommendations"].append("Review negative sentiment indicators and address concerns")
        
        if compliance.get('compliance_focus') == 'high':
            insights["recommendations"].append("Ensure compliance requirements are properly addressed")
        
        # Opportunities
        if 'growth' in topics.get('categorized_topics', {}):
            insights["opportunities"].append("Growth opportunities identified in content")
        
        if metrics.get('has_performance_data'):
            insights["opportunities"].append("Performance metrics available for further analysis")
        
        # Concerns
        if risks.get('risk_score', 0) > 8:
            insights["concerns"].append("Multiple risk factors identified requiring attention")
        
        if compliance.get('frameworks_identified'):
            insights["concerns"].append("Compliance frameworks mentioned - ensure adherence")
        
        return insights
    
    def _create_summary(
        self, 
        topics: Dict, 
        risks: Dict, 
        metrics: Dict, 
        insights: Dict
    ) -> Dict[str, Any]:
        """Create a comprehensive analysis summary."""
        return {
            "document_focus": topics.get('primary_focus', 'general'),
            "risk_level": risks.get('overall_risk_level', 'unknown'),
            "has_metrics": metrics.get('has_financial_data', False),
            "key_insights_count": len(insights.get('key_findings', [])),
            "recommendations_count": len(insights.get('recommendations', [])),
            "analysis_confidence": "high" if metrics.get('metrics_confidence') == 'high' else "medium"
        }


async def main():
    """Main function to run the Analytics Agent."""
    agent = AnalyticsAgent()
    
    # Connect to GenAI AgentOS
    session = GenAISession(
        ws_url="ws://localhost:8080/ws",
        agent_name=agent.name,
        agent_description=agent.description,
        agent_version=agent.version
    )
    
    logger.info(f"Starting {agent.name} agent...")
    
    try:
        await session.connect()
        logger.info("Connected to GenAI AgentOS")
        
        # Listen for messages
        async for message in session.listen():
            logger.info(f"Received message: {message.id}")
            
            try:
                result = await agent.process_message(session, message.content)
                await session.send_response(message.id, json.dumps(result))
                logger.info(f"Sent response for message: {message.id}")
                
            except Exception as e:
                error_response = {
                    "error": f"Processing failed: {str(e)}",
                    "status": "error",
                    "agent": agent.name
                }
                await session.send_response(message.id, json.dumps(error_response))
                logger.error(f"Error processing message {message.id}: {str(e)}")
                
    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
    finally:
        await session.disconnect()
        logger.info("Agent disconnected")


if __name__ == "__main__":
    asyncio.run(main())