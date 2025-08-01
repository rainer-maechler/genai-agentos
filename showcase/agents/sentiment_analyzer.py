#!/usr/bin/env python3
"""
Sentiment Analyzer Agent for GenAI AgentOS Showcase

This agent analyzes emotional tone and sentiment of content.
Capabilities:
- Sentiment scoring (-1 to +1)
- Emotion classification
- Confidence levels
- Context-aware analysis
- Multi-dimensional sentiment analysis
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Tuple
from datetime import datetime
from collections import Counter
from loguru import logger

# Text processing imports
from textblob import TextBlob

# GenAI Protocol
from genai_protocol import GenAISession


class SentimentAnalyzerAgent:
    """Agent that performs comprehensive sentiment and emotional analysis."""
    
    def __init__(self):
        self.name = "sentiment_analyzer"
        self.description = "Analyzes sentiment, emotions, and psychological tone of content"
        self.version = "1.0.0"
        
        # Emotion keywords mapping
        self.emotion_keywords = {
            'joy': ['happy', 'joyful', 'pleased', 'delighted', 'excited', 'cheerful', 'satisfied', 'glad'],
            'trust': ['confident', 'reliable', 'trustworthy', 'dependable', 'secure', 'assured', 'certain'],
            'fear': ['afraid', 'worried', 'concerned', 'anxious', 'nervous', 'uncertain', 'risk', 'threat'],
            'surprise': ['surprised', 'unexpected', 'amazed', 'astonished', 'shocking', 'remarkable', 'stunning'],
            'sadness': ['sad', 'disappointed', 'unfortunate', 'regret', 'sorry', 'upset', 'discouraged'],
            'disgust': ['disgusted', 'revolted', 'appalled', 'outraged', 'horrified', 'repulsed'],
            'anger': ['angry', 'furious', 'annoyed', 'frustrated', 'irritated', 'outraged', 'mad'],
            'anticipation': ['expecting', 'hopeful', 'looking forward', 'anticipating', 'eager', 'ready']
        }
        
        # Sentiment modifiers
        self.intensifiers = ['very', 'extremely', 'highly', 'incredibly', 'absolutely', 'completely', 'totally']
        self.diminishers = ['somewhat', 'rather', 'quite', 'fairly', 'slightly', 'moderately', 'relatively']
        self.negations = ['not', 'no', 'never', 'nothing', 'nobody', 'none', 'neither', 'nowhere']
        
        # Context-specific sentiment patterns
        self.business_sentiment_patterns = {
            'positive': [
                r'\b(?:excellent|outstanding|exceptional|superior|impressive)\s+(?:performance|results|outcome)',
                r'\b(?:significant|substantial|major)\s+(?:improvement|growth|increase)',
                r'\b(?:successful|effective|efficient|optimal)\s+(?:implementation|execution|operation)',
                r'\b(?:exceeded|surpassed|outperformed)\s+(?:expectations|targets|goals)',
                r'\b(?:strong|robust|solid|healthy)\s+(?:financial|business|market)\s+(?:performance|position)'
            ],
            'negative': [
                r'\b(?:poor|weak|disappointing|unsatisfactory)\s+(?:performance|results|outcome)',
                r'\b(?:significant|substantial|major)\s+(?:decline|decrease|reduction|loss)',
                r'\b(?:failed|unsuccessful|ineffective)\s+(?:implementation|execution|operation)',
                r'\b(?:missed|fell short of|underperformed)\s+(?:expectations|targets|goals)',
                r'\b(?:weak|poor|declining)\s+(?:financial|business|market)\s+(?:performance|position)'
            ]
        }
        
        # Confidence indicators
        self.confidence_patterns = {
            'high': [r'\b(?:definitely|certainly|absolutely|guaranteed|ensure|confirm)\b'],
            'medium': [r'\b(?:likely|probably|expected|anticipated|should|would)\b'],
            'low': [r'\b(?:might|maybe|possibly|perhaps|could|may|uncertain)\b']
        }
    
    async def process_message(self, session: GenAISession, message: str) -> Dict[str, Any]:
        """Process incoming message and perform sentiment analysis."""
        try:
            # Parse the input message
            request = json.loads(message)
            
            # Extract text and context from previous agents
            text = request.get('cleaned_text', '')
            sections = request.get('sections', [])
            entities = request.get('entities', {})
            analytics = request.get('risk_analysis', {})
            
            if not text:
                return {
                    "error": "No text content provided",
                    "status": "error"
                }
            
            # Perform sentiment analysis
            result = await self._analyze_sentiment(text, sections, entities, analytics)
            
            # Add agent metadata
            result.update({
                "agent": self.name,
                "analyzed_at": datetime.now().isoformat(),
                "status": "success"
            })
            
            logger.info(f"Successfully analyzed sentiment for {len(text)} characters")
            return result
            
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input", "status": "error"}
        except Exception as e:
            logger.error(f"Error performing sentiment analysis: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _analyze_sentiment(
        self, 
        text: str, 
        sections: List[Dict], 
        entities: Dict, 
        analytics: Dict
    ) -> Dict[str, Any]:
        """Perform comprehensive sentiment analysis."""
        
        # Overall sentiment analysis
        overall_sentiment = self._analyze_overall_sentiment(text)
        
        # Emotion analysis
        emotion_analysis = self._analyze_emotions(text)
        
        # Section-wise sentiment
        section_sentiment = self._analyze_section_sentiment(sections)
        
        # Context-aware business sentiment
        business_sentiment = self._analyze_business_sentiment(text)
        
        # Confidence and certainty analysis
        confidence_analysis = self._analyze_confidence_levels(text)
        
        # Sentiment trends and patterns
        sentiment_patterns = self._analyze_sentiment_patterns(text)
        
        # Psychological indicators
        psychological_indicators = self._analyze_psychological_indicators(text)
        
        # Entity-based sentiment
        entity_sentiment = self._analyze_entity_sentiment(text, entities)
        
        # Generate sentiment insights
        insights = self._generate_sentiment_insights(
            overall_sentiment, emotion_analysis, business_sentiment, 
            confidence_analysis, psychological_indicators
        )
        
        return {
            "overall_sentiment": overall_sentiment,
            "emotions": emotion_analysis,
            "section_sentiment": section_sentiment,
            "business_sentiment": business_sentiment,
            "confidence_levels": confidence_analysis,
            "sentiment_patterns": sentiment_patterns,
            "psychological_indicators": psychological_indicators,
            "entity_sentiment": entity_sentiment,
            "insights": insights,
            "sentiment_summary": self._create_sentiment_summary(
                overall_sentiment, emotion_analysis, business_sentiment
            )
        }
    
    def _analyze_overall_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze overall sentiment using TextBlob and custom analysis."""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment_label = "positive"
            elif polarity < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            # Determine intensity
            intensity = abs(polarity)
            if intensity > 0.6:
                intensity_label = "strong"
            elif intensity > 0.3:
                intensity_label = "moderate"
            else:
                intensity_label = "weak"
            
            # Calculate confidence based on text length and subjectivity
            confidence = min(0.95, 0.5 + (len(text) / 2000) * 0.3 + subjectivity * 0.2)
            
            return {
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "sentiment_label": sentiment_label,
                "intensity": intensity_label,
                "confidence": round(confidence, 3),
                "sentiment_score": round((polarity + 1) * 50, 1),  # 0-100 scale
                "objectivity": round(1 - subjectivity, 3)
            }
            
        except Exception as e:
            logger.warning(f"Overall sentiment analysis failed: {str(e)}")
            return {
                "polarity": 0.0,
                "subjectivity": 0.5,
                "sentiment_label": "neutral",
                "intensity": "unknown",
                "confidence": 0.0,
                "error": "Analysis unavailable"
            }
    
    def _analyze_emotions(self, text: str) -> Dict[str, Any]:
        """Analyze emotions using keyword-based approach."""
        text_lower = text.lower()
        emotion_scores = {}
        emotion_contexts = {}
        
        # Count emotion keywords
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            contexts = []
            
            for keyword in keywords:
                count = text_lower.count(keyword)
                if count > 0:
                    score += count
                    # Find context around keyword
                    contexts.extend(self._extract_context(text, keyword, 50))
            
            if score > 0:
                emotion_scores[emotion] = score
                emotion_contexts[emotion] = contexts[:3]  # Keep top 3 contexts
        
        # Normalize scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_percentages = {
                emotion: round((score / total_score) * 100, 1)
                for emotion, score in emotion_scores.items()
            }
        else:
            emotion_percentages = {}
        
        # Determine dominant emotion
        dominant_emotion = max(emotion_scores.keys(), key=emotion_scores.get) if emotion_scores else "neutral"
        
        # Emotional complexity
        complexity = len(emotion_scores)
        complexity_label = "high" if complexity > 4 else "medium" if complexity > 2 else "low"
        
        return {
            "emotion_scores": emotion_scores,
            "emotion_percentages": emotion_percentages,
            "emotion_contexts": emotion_contexts,
            "dominant_emotion": dominant_emotion,
            "emotional_complexity": complexity_label,
            "total_emotional_indicators": total_score,
            "emotions_detected": list(emotion_scores.keys())
        }
    
    def _analyze_section_sentiment(self, sections: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze sentiment for each section."""
        section_sentiments = []
        
        for section in sections:
            section_text = section.get('content', '')
            if not section_text:
                continue
            
            try:
                blob = TextBlob(section_text)
                polarity = blob.sentiment.polarity
                
                sentiment_label = "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
                
                section_sentiments.append({
                    "section_title": section.get('title', 'Unknown'),
                    "polarity": round(polarity, 3),
                    "sentiment_label": sentiment_label,
                    "word_count": section.get('word_count', 0),
                    "sentiment_strength": abs(polarity)
                })
                
            except Exception as e:
                logger.warning(f"Section sentiment analysis failed for {section.get('title', 'Unknown')}: {str(e)}")
                continue
        
        return section_sentiments
    
    def _analyze_business_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze business-specific sentiment patterns."""
        text_lower = text.lower()
        
        positive_matches = []
        negative_matches = []
        
        # Check business sentiment patterns
        for pattern in self.business_sentiment_patterns['positive']:
            matches = re.findall(pattern, text_lower)
            positive_matches.extend(matches)
        
        for pattern in self.business_sentiment_patterns['negative']:
            matches = re.findall(pattern, text_lower)
            negative_matches.extend(matches)
        
        # Calculate business sentiment score
        positive_score = len(positive_matches)
        negative_score = len(negative_matches)
        
        if positive_score > negative_score:
            business_sentiment = "positive"
            confidence = positive_score / (positive_score + negative_score + 1)
        elif negative_score > positive_score:
            business_sentiment = "negative"
            confidence = negative_score / (positive_score + negative_score + 1)
        else:
            business_sentiment = "neutral"
            confidence = 0.5
        
        # Business-specific indicators
        financial_indicators = self._analyze_financial_sentiment(text_lower)
        performance_indicators = self._analyze_performance_sentiment(text_lower)
        
        return {
            "business_sentiment": business_sentiment,
            "confidence": round(confidence, 3),
            "positive_indicators": positive_matches,
            "negative_indicators": negative_matches,
            "financial_sentiment": financial_indicators,
            "performance_sentiment": performance_indicators,
            "business_tone": self._determine_business_tone(positive_score, negative_score)
        }
    
    def _analyze_confidence_levels(self, text: str) -> Dict[str, Any]:
        """Analyze confidence and certainty levels in the text."""
        text_lower = text.lower()
        confidence_counts = {'high': 0, 'medium': 0, 'low': 0}
        confidence_phrases = {'high': [], 'medium': [], 'low': []}
        
        for level, patterns in self.confidence_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                confidence_counts[level] += len(matches)
                confidence_phrases[level].extend(matches[:5])  # Keep top 5
        
        # Overall confidence level
        total_indicators = sum(confidence_counts.values())
        if total_indicators == 0:
            overall_confidence = "neutral"
            confidence_score = 0.5
        else:
            weighted_score = (
                confidence_counts['high'] * 1.0 + 
                confidence_counts['medium'] * 0.6 + 
                confidence_counts['low'] * 0.2
            ) / total_indicators
            
            if weighted_score > 0.7:
                overall_confidence = "high"
            elif weighted_score > 0.4:
                overall_confidence = "medium"
            else:
                overall_confidence = "low"
            
            confidence_score = weighted_score
        
        return {
            "confidence_counts": confidence_counts,
            "confidence_phrases": confidence_phrases,
            "overall_confidence": overall_confidence,
            "confidence_score": round(confidence_score, 3),
            "total_confidence_indicators": total_indicators
        }
    
    def _analyze_sentiment_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment patterns and trends."""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        sentence_sentiments = []
        
        # Analyze sentiment of each sentence
        for sentence in sentences[:20]:  # Limit to first 20 sentences
            try:
                blob = TextBlob(sentence)
                polarity = blob.sentiment.polarity
                sentence_sentiments.append({
                    "sentence": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                    "polarity": round(polarity, 3),
                    "sentiment": "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
                })
            except:
                continue
        
        # Analyze sentiment flow
        polarities = [s['polarity'] for s in sentence_sentiments]
        
        sentiment_flow = "stable"
        if len(polarities) > 5:
            # Check for trends
            first_half = polarities[:len(polarities)//2]
            second_half = polarities[len(polarities)//2:]
            
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)
            
            if avg_second > avg_first + 0.2:
                sentiment_flow = "improving"
            elif avg_second < avg_first - 0.2:
                sentiment_flow = "declining"
        
        return {
            "sentence_sentiments": sentence_sentiments,
            "sentiment_flow": sentiment_flow,
            "sentiment_variability": round(self._calculate_variability(polarities), 3) if polarities else 0,
            "most_positive_sentence": max(sentence_sentiments, key=lambda x: x['polarity']) if sentence_sentiments else None,
            "most_negative_sentence": min(sentence_sentiments, key=lambda x: x['polarity']) if sentence_sentiments else None
        }
    
    def _analyze_psychological_indicators(self, text: str) -> Dict[str, Any]:
        """Analyze psychological indicators in the text."""
        text_lower = text.lower()
        
        # Psychological patterns
        stress_indicators = ['stress', 'pressure', 'overwhelmed', 'burden', 'strain', 'exhausted']
        optimism_indicators = ['optimistic', 'hopeful', 'positive', 'bright', 'promising', 'encouraging']
        uncertainty_indicators = ['uncertain', 'unclear', 'confused', 'doubt', 'unsure', 'ambiguous']
        authority_indicators = ['must', 'should', 'required', 'mandatory', 'essential', 'critical']
        
        psychological_scores = {
            'stress': sum(text_lower.count(word) for word in stress_indicators),
            'optimism': sum(text_lower.count(word) for word in optimism_indicators),
            'uncertainty': sum(text_lower.count(word) for word in uncertainty_indicators),
            'authority': sum(text_lower.count(word) for word in authority_indicators)
        }
        
        # Determine dominant psychological tone
        dominant_tone = max(psychological_scores.keys(), key=psychological_scores.get) if any(psychological_scores.values()) else "neutral"
        
        return {
            "psychological_scores": psychological_scores,
            "dominant_psychological_tone": dominant_tone,
            "psychological_intensity": max(psychological_scores.values()),
            "psychological_balance": self._calculate_psychological_balance(psychological_scores)
        }
    
    def _analyze_entity_sentiment(self, text: str, entities: Dict) -> Dict[str, Any]:
        """Analyze sentiment towards specific entities."""
        entity_sentiments = {}
        
        # Analyze sentiment towards companies
        if 'company' in entities:
            for company in entities['company'][:5]:  # Limit to 5 companies
                context_sentences = self._extract_context(text, company, 200)
                if context_sentences:
                    avg_sentiment = 0
                    for sentence in context_sentences:
                        try:
                            blob = TextBlob(sentence)
                            avg_sentiment += blob.sentiment.polarity
                        except:
                            continue
                    
                    if context_sentences:
                        avg_sentiment /= len(context_sentences)
                        entity_sentiments[company] = {
                            "sentiment": round(avg_sentiment, 3),
                            "label": "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral",
                            "contexts": context_sentences[:2]
                        }
        
        # Analyze sentiment towards people
        if 'person' in entities:
            for person in entities['person'][:3]:  # Limit to 3 people
                context_sentences = self._extract_context(text, person, 150)
                if context_sentences:
                    avg_sentiment = 0
                    for sentence in context_sentences:
                        try:
                            blob = TextBlob(sentence)
                            avg_sentiment += blob.sentiment.polarity
                        except:
                            continue
                    
                    if context_sentences:
                        avg_sentiment /= len(context_sentences)
                        entity_sentiments[person] = {
                            "sentiment": round(avg_sentiment, 3),
                            "label": "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral",
                            "contexts": context_sentences[:2]
                        }
        
        return entity_sentiments
    
    def _analyze_financial_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment towards financial aspects."""
        financial_positive = ['profit', 'revenue', 'growth', 'savings', 'return', 'gain', 'increase']
        financial_negative = ['loss', 'debt', 'deficit', 'cost', 'expense', 'decline', 'decrease']
        
        positive_count = sum(text.count(word) for word in financial_positive)
        negative_count = sum(text.count(word) for word in financial_negative)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "financial_tone_strength": abs(positive_count - negative_count)
        }
    
    def _analyze_performance_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment towards performance aspects."""
        performance_positive = ['excellent', 'outstanding', 'improved', 'successful', 'effective', 'efficient']
        performance_negative = ['poor', 'failed', 'disappointing', 'ineffective', 'unsuccessful', 'inadequate']
        
        positive_count = sum(text.count(word) for word in performance_positive)
        negative_count = sum(text.count(word) for word in performance_negative)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "performance_tone_strength": abs(positive_count - negative_count)
        }
    
    def _determine_business_tone(self, positive_score: int, negative_score: int) -> str:
        """Determine overall business tone."""
        if positive_score > negative_score * 1.5:
            return "optimistic"
        elif negative_score > positive_score * 1.5:
            return "pessimistic"
        elif positive_score > 0 or negative_score > 0:
            return "balanced"
        else:
            return "neutral"
    
    def _extract_context(self, text: str, keyword: str, context_length: int = 100) -> List[str]:
        """Extract context around a keyword."""
        contexts = []
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        start = 0
        while True:
            pos = text_lower.find(keyword_lower, start)
            if pos == -1:
                break
            
            # Extract context
            context_start = max(0, pos - context_length // 2)
            context_end = min(len(text), pos + len(keyword) + context_length // 2)
            context = text[context_start:context_end].strip()
            
            if context and context not in contexts:
                contexts.append(context)
            
            start = pos + len(keyword)
            
            if len(contexts) >= 3:  # Limit contexts
                break
        
        return contexts
    
    def _calculate_variability(self, values: List[float]) -> float:
        """Calculate variability (standard deviation) of sentiment values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _calculate_psychological_balance(self, scores: Dict[str, int]) -> str:
        """Calculate psychological balance."""
        total = sum(scores.values())
        if total == 0:
            return "neutral"
        
        # Check if any single factor dominates
        max_score = max(scores.values())
        if max_score > total * 0.6:
            return "imbalanced"
        elif max_score > total * 0.4:
            return "slightly_imbalanced"
        else:
            return "balanced"
    
    def _generate_sentiment_insights(
        self,
        overall: Dict,
        emotions: Dict,
        business: Dict,
        confidence: Dict,
        psychological: Dict
    ) -> Dict[str, Any]:
        """Generate comprehensive sentiment insights."""
        insights = {
            "key_findings": [],
            "recommendations": [],
            "concerns": [],
            "strengths": []
        }
        
        # Key findings
        sentiment_label = overall.get('sentiment_label', 'neutral')
        intensity = overall.get('intensity', 'weak')
        insights["key_findings"].append(f"Overall sentiment: {sentiment_label} ({intensity} intensity)")
        
        dominant_emotion = emotions.get('dominant_emotion', 'neutral')
        if dominant_emotion != 'neutral':
            insights["key_findings"].append(f"Dominant emotion: {dominant_emotion}")
        
        business_sentiment = business.get('business_sentiment', 'neutral')
        if business_sentiment != 'neutral':
            insights["key_findings"].append(f"Business sentiment: {business_sentiment}")
        
        # Recommendations
        if sentiment_label == 'negative':
            insights["recommendations"].append("Consider addressing negative sentiment indicators")
        
        if confidence.get('overall_confidence') == 'low':
            insights["recommendations"].append("Increase certainty and confidence in statements")
        
        if psychological.get('dominant_psychological_tone') == 'stress':
            insights["recommendations"].append("Address stress indicators and improve tone")
        
        # Concerns
        if overall.get('polarity', 0) < -0.5:
            insights["concerns"].append("Strong negative sentiment detected")
        
        if emotions.get('emotional_complexity') == 'high' and sentiment_label == 'negative':
            insights["concerns"].append("Complex negative emotions present")
        
        # Strengths
        if sentiment_label == 'positive' and intensity in ['moderate', 'strong']:
            insights["strengths"].append("Strong positive sentiment throughout content")
        
        if confidence.get('overall_confidence') == 'high':
            insights["strengths"].append("High confidence and certainty in statements")
        
        return insights
    
    def _create_sentiment_summary(
        self,
        overall: Dict,
        emotions: Dict,
        business: Dict
    ) -> Dict[str, Any]:
        """Create a comprehensive sentiment summary."""
        return {
            "overall_sentiment": overall.get('sentiment_label', 'neutral'),
            "sentiment_score": overall.get('sentiment_score', 50),
            "confidence": overall.get('confidence', 0.5),
            "dominant_emotion": emotions.get('dominant_emotion', 'neutral'),
            "business_tone": business.get('business_tone', 'neutral'),
            "emotional_complexity": emotions.get('emotional_complexity', 'low'),
            "analysis_quality": "high" if overall.get('confidence', 0) > 0.7 else "medium"
        }


async def main():
    """Main function to run the Sentiment Analyzer Agent."""
    agent = SentimentAnalyzerAgent()
    
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