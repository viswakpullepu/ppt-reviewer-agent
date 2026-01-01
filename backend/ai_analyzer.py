"""AI-powered analysis of PowerPoint presentations using OpenAI API."""
import asyncio
import logging
from typing import Dict, List
from openai import OpenAI, AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Analyze presentations using OpenAI's language models."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.async_client = AsyncOpenAI(api_key=settings.openai_api_key)

    def analyze_slide_content(self, slide_data: Dict) -> Dict:
        """Analyze content quality of a slide.
        
        Args:
            slide_data: Dictionary containing slide text and metadata
            
        Returns:
            Dictionary with analysis results and suggestions
        """
        try:
            slide_text = slide_data.get("text_content", "")
            title = slide_data.get("title", "")
            word_count = slide_data.get("word_count", 0)
            
            prompt = f"""
            Analyze this PowerPoint slide and provide constructive feedback:
            
            Title: {title}
            Content: {slide_text}
            Word Count: {word_count}
            
            Please provide:
            1. Content Clarity Score (0-100)
            2. Engagement Score (0-100)
            3. Key strengths (list 2-3 points)
            4. Areas for improvement (list 2-3 points)
            5. Specific suggestions for enhancement
            
            Format response as JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert presentation coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            
            analysis = {
                "slide_number": slide_data.get("slide_number"),
                "ai_feedback": response.choices[0].message.content,
                "model_used": "gpt-3.5-turbo",
            }
            
            logger.info(f"Analyzed slide {slide_data.get('slide_number')}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing slide: {str(e)}")
            return {
                "slide_number": slide_data.get("slide_number"),
                "error": str(e),
                "ai_feedback": "Unable to analyze at this time",
            }

    def analyze_presentation_structure(self, slides_data: List[Dict]) -> Dict:
        """Analyze overall presentation structure and flow.
        
        Args:
            slides_data: List of slide data dictionaries
            
        Returns:
            Dictionary with presentation-level analysis
        """
        try:
            # Extract key information from all slides
            titles = [s.get("title", "") for s in slides_data]
            total_words = sum(s.get("word_count", 0) for s in slides_data)
            avg_words = total_words // len(slides_data) if slides_data else 0
            
            slide_summary = "\n".join([f"Slide {s['slide_number']}: {s['title']}" for s in slides_data])
            
            prompt = f"""
            Analyze this presentation's overall structure and flow:
            
            Total Slides: {len(slides_data)}
            Average Words per Slide: {avg_words}
            
            Slide Outline:
            {slide_summary}
            
            Please evaluate:
            1. Logical Flow Score (0-100)
            2. Message Clarity Score (0-100)
            3. Presentation Coherence Score (0-100)
            4. Overall Assessment (brief paragraph)
            5. Top 3 Recommendations for improvement
            
            Format response as JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a presentation strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600,
            )
            
            return {
                "presentation_structure_analysis": response.choices[0].message.content,
                "total_slides": len(slides_data),
                "average_slide_length": avg_words,
            }
            
        except Exception as e:
            logger.error(f"Error analyzing presentation structure: {str(e)}")
            return {
                "error": str(e),
                "presentation_structure_analysis": "Unable to analyze structure at this time",
            }

    def generate_suggestions(self, slide_analysis: Dict) -> List[str]:
        """Generate specific, actionable suggestions for a slide.
        
        Args:
            slide_analysis: Dictionary with slide analysis data
            
        Returns:
            List of suggestion strings
        """
        try:
            content = slide_analysis.get("text_content", "")
            title = slide_analysis.get("title", "")
            
            prompt = f"""
            Provide 5 specific, actionable suggestions to improve this slide:
            
            Title: {title}
            Content: {content}
            
            Focus on:
            - Visual improvements
            - Content clarity
            - Audience engagement
            - Design best practices
            
            Return as a JSON list of strings, where each string is one specific suggestion.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional presentation designer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400,
            )
            
            # Parse response and extract suggestions
            suggestions_text = response.choices[0].message.content
            return self._parse_suggestions(suggestions_text)
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return ["Unable to generate suggestions at this time"]

    def _parse_suggestions(self, response_text: str) -> List[str]:
        """Parse AI response to extract suggestions.
        
        Args:
            response_text: Raw response from OpenAI
            
        Returns:
            List of suggestions
        """
        try:
            import json
            # Try to extract JSON from response
            start = response_text.find("[")
            end = response_text.rfind("]") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Could not parse suggestions as JSON: {str(e)}")
        
        # Fallback: split by common delimiters
        suggestions = []
        for line in response_text.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                # Remove numbering
                suggestion = line.lstrip("0123456789.-) ")
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions if suggestions else [response_text]

    async def analyze_slide_async(self, slide_data: Dict) -> Dict:
        """Async version of slide analysis for better performance.
        
        Args:
            slide_data: Dictionary containing slide data
            
        Returns:
            Dictionary with analysis results
        """
        try:
            slide_text = slide_data.get("text_content", "")
            title = slide_data.get("title", "")
            
            prompt = f"""
            Analyze this slide and rate its quality (0-100) in: clarity, engagement, design.
            Title: {title}
            Content: {slide_text}
            
            Respond with JSON: {{"clarity": X, "engagement": Y, "design": Z, "feedback": "..."}}
            """
            
            response = await self.async_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a presentation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,
            )
            
            return {
                "slide_number": slide_data.get("slide_number"),
                "analysis": response.choices[0].message.content,
            }
            
        except Exception as e:
            logger.error(f"Error in async analysis: {str(e)}")
            return {"slide_number": slide_data.get("slide_number"), "error": str(e)}
