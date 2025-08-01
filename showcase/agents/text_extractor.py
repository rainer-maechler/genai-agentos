#!/usr/bin/env python3
"""
Text Extractor Agent for GenAI AgentOS Showcase

This agent cleans and structures extracted text from the Document Parser.
Capabilities:
- Text normalization and cleaning
- Language detection
- Section identification
- Entity extraction (names, dates, amounts)
- Content structure analysis
"""

import asyncio
import json
import re
from typing import Dict, Any, List, Tuple
from datetime import datetime
from loguru import logger

# Text processing imports
from textblob import TextBlob

# GenAI Protocol
from genai_protocol import GenAISession


class TextExtractorAgent:
    """Agent that cleans, normalizes, and structures text content."""
    
    def __init__(self):
        self.name = "text_extractor"
        self.description = "Cleans and structures text content, performs entity extraction"
        self.version = "1.0.0"
        
        # Regex patterns for entity extraction
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
            'date': re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            'currency': re.compile(r'\$[\d,]+\.?\d*|\b\d+\.\d{2}\s*(?:USD|EUR|GBP|CAD|AUD)\b'),
            'percentage': re.compile(r'\b\d+\.?\d*%\b'),
            'url': re.compile(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?'),
            'company': re.compile(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|LLC|Corp|Ltd|Co|Company|Industries|Group|Solutions|Systems|Technologies)\.?)\b'),
            'person': re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'),  # Simple name pattern
            'time': re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b'),
            'address': re.compile(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\.?'),
        }
        
        # Section headers patterns
        self.section_patterns = [
            re.compile(r'^(Executive Summary|Summary)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Introduction|Overview)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Background|Context)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Objectives?|Goals?)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Methodology|Approach|Methods?)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Results?|Findings?)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Discussion|Analysis)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Conclusions?|Summary)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Recommendations?|Next Steps)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(References?|Bibliography)[:.]?', re.IGNORECASE | re.MULTILINE),
            re.compile(r'^(Appendix|Appendices)[:.]?', re.IGNORECASE | re.MULTILINE),
        ]
    
    async def process_message(self, session: GenAISession, message: str) -> Dict[str, Any]:
        """Process incoming message and extract structured text."""
        try:
            # Parse the input message
            request = json.loads(message)
            text_content = request.get('full_text', '')
            document_type = request.get('document_type', 'unknown')
            metadata = request.get('metadata', {})
            options = request.get('options', {})
            
            if not text_content:
                return {
                    "error": "No text content provided",
                    "status": "error"
                }
            
            # Process the text
            result = await self._extract_and_structure_text(
                text_content, document_type, metadata, options
            )
            
            # Add agent metadata
            result.update({
                "agent": self.name,
                "processed_at": datetime.now().isoformat(),
                "status": "success"
            })
            
            logger.info(f"Successfully processed text content ({len(text_content)} chars)")
            return result
            
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input", "status": "error"}
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return {"error": str(e), "status": "error"}
    
    async def _extract_and_structure_text(
        self, 
        text: str, 
        document_type: str, 
        metadata: Dict, 
        options: Dict
    ) -> Dict[str, Any]:
        """Extract and structure text content."""
        
        # Clean and normalize text
        cleaned_text = self._clean_text(text)
        
        # Detect language
        language_info = self._detect_language(cleaned_text)
        
        # Extract entities
        entities = self._extract_entities(cleaned_text)
        
        # Identify sections
        sections = self._identify_sections(cleaned_text)
        
        # Extract key phrases and topics
        key_phrases = self._extract_key_phrases(cleaned_text)
        
        # Analyze text structure
        structure_analysis = self._analyze_structure(cleaned_text)
        
        # Generate text statistics
        stats = self._generate_statistics(cleaned_text)
        
        return {
            "original_text": text,
            "cleaned_text": cleaned_text,
            "language": language_info,
            "entities": entities,
            "sections": sections,
            "key_phrases": key_phrases,
            "structure": structure_analysis,
            "statistics": stats,
            "document_type": document_type,
            "processing_options": options
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\(\)\-\"\'\$\%\@\#]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Strip and clean up
        text = text.strip()
        
        return text
    
    def _detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of the text."""
        try:
            blob = TextBlob(text[:1000])  # Use first 1000 chars for detection
            detected_lang = blob.detect_language()
            
            # Map language codes to names
            lang_names = {
                'en': 'English',
                'es': 'Spanish', 
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese',
                'nl': 'Dutch',
                'ru': 'Russian',
                'zh': 'Chinese',
                'ja': 'Japanese',
                'ko': 'Korean',
                'ar': 'Arabic'
            }
            
            return {
                "code": detected_lang,
                "name": lang_names.get(detected_lang, detected_lang),
                "confidence": "high" if len(text) > 100 else "low"
            }
            
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return {
                "code": "en",
                "name": "English",
                "confidence": "assumed"
            }
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text."""
        entities = {}
        
        for entity_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            # Remove duplicates and clean up
            unique_matches = list(set([match.strip() for match in matches if match.strip()]))
            if unique_matches:
                entities[entity_type] = unique_matches
        
        # Extract additional business-specific entities
        entities.update(self._extract_business_entities(text))
        
        return entities
    
    def _extract_business_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract business-specific entities."""
        business_entities = {}
        
        # ROI and financial metrics
        roi_pattern = re.compile(r'\b(?:ROI|return on investment)\s*[:=]?\s*(\d+(?:\.\d+)?%?)\b', re.IGNORECASE)
        roi_matches = roi_pattern.findall(text)
        if roi_matches:
            business_entities['roi'] = roi_matches
        
        # Timeline and duration
        timeline_pattern = re.compile(r'\b(\d+)\s*(?:month|year|week|day)s?\b', re.IGNORECASE)
        timeline_matches = timeline_pattern.findall(text)
        if timeline_matches:
            business_entities['timelines'] = [f"{match} units" for match in timeline_matches]
        
        # Metrics and KPIs
        metric_pattern = re.compile(r'\b(?:increase|decrease|improve|reduce)\s+(?:by\s+)?(\d+(?:\.\d+)?%)\b', re.IGNORECASE)
        metric_matches = metric_pattern.findall(text)
        if metric_matches:
            business_entities['metrics'] = [f"{match}%" for match in metric_matches]
        
        return business_entities
    
    def _identify_sections(self, text: str) -> List[Dict[str, Any]]:
        """Identify document sections."""
        sections = []
        lines = text.split('\n')
        
        current_section = None
        section_content = []
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches any section pattern
            section_match = None
            for pattern in self.section_patterns:
                if pattern.match(line):
                    section_match = pattern.match(line).group(1)
                    break
            
            if section_match:
                # Save previous section
                if current_section and section_content:
                    sections.append({
                        "title": current_section,
                        "content": '\n'.join(section_content),
                        "word_count": len(' '.join(section_content).split()),
                        "start_line": line_num - len(section_content),
                        "end_line": line_num
                    })
                
                # Start new section
                current_section = section_match
                section_content = []
            else:
                # Add to current section
                if current_section:
                    section_content.append(line)
        
        # Add final section
        if current_section and section_content:
            sections.append({
                "title": current_section,
                "content": '\n'.join(section_content),
                "word_count": len(' '.join(section_content).split()),
                "start_line": len(lines) - len(section_content),
                "end_line": len(lines)
            })
        
        # If no sections found, treat entire text as one section
        if not sections:
            sections.append({
                "title": "Main Content",
                "content": text,
                "word_count": len(text.split()),
                "start_line": 0,
                "end_line": len(lines)
            })
        
        return sections
    
    def _extract_key_phrases(self, text: str) -> Dict[str, Any]:
        """Extract key phrases and topics from text."""
        try:
            blob = TextBlob(text)
            
            # Extract noun phrases
            noun_phrases = list(set([str(phrase).lower() for phrase in blob.noun_phrases 
                                   if len(phrase.split()) <= 4 and len(phrase) > 3]))
            
            # Sort by frequency
            phrase_freq = {}
            for phrase in noun_phrases:
                phrase_freq[phrase] = text.lower().count(phrase)
            
            # Get top phrases
            top_phrases = sorted(phrase_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "noun_phrases": [phrase for phrase, _ in top_phrases],
                "phrase_frequencies": dict(top_phrases),
                "total_phrases": len(noun_phrases)
            }
            
        except Exception as e:
            logger.warning(f"Key phrase extraction failed: {str(e)}")
            return {
                "noun_phrases": [],
                "phrase_frequencies": {},
                "total_phrases": 0
            }
    
    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze text structure and formatting."""
        lines = text.split('\n')
        sentences = text.split('.')
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Analyze sentence structure
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # Analyze paragraph structure
        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        # Detect lists and bullet points
        list_items = len([line for line in lines if re.match(r'^\s*[-*•]\s+', line)])
        numbered_items = len([line for line in lines if re.match(r'^\s*\d+\.?\s+', line)])
        
        return {
            "line_count": len(lines),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "average_sentence_length": round(avg_sentence_length, 2),
            "average_paragraph_length": round(avg_paragraph_length, 2),
            "list_items": list_items,
            "numbered_items": numbered_items,
            "has_lists": list_items > 0 or numbered_items > 0,
            "structure_complexity": "high" if len(paragraphs) > 10 else "medium" if len(paragraphs) > 3 else "low"
        }
    
    def _generate_statistics(self, text: str) -> Dict[str, Any]:
        """Generate comprehensive text statistics."""
        words = text.split()
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', ''))
        
        # Character frequency
        char_freq = {}
        for char in text.lower():
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        # Word frequency
        word_freq = {}
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word and len(clean_word) > 2:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Top words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Reading metrics
        sentences = len([s for s in text.split('.') if s.strip()])
        avg_words_per_sentence = len(words) / sentences if sentences > 0 else 0
        
        return {
            "word_count": len(words),
            "character_count": chars,
            "character_count_no_spaces": chars_no_spaces,
            "sentence_count": sentences,
            "average_words_per_sentence": round(avg_words_per_sentence, 2),
            "top_words": dict(top_words),
            "unique_words": len(set(word_freq.keys())),
            "lexical_diversity": round(len(set(word_freq.keys())) / len(words), 3) if words else 0,
            "estimated_reading_time_minutes": round(len(words) / 200, 1)  # Average 200 WPM
        }


async def main():
    """Main function to run the Text Extractor Agent."""
    agent = TextExtractorAgent()
    
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