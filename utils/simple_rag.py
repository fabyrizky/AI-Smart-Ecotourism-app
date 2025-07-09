import pandas as pd
import numpy as np
from typing import List, Dict, Any
import json
import re
from datetime import datetime

class SimpleRAG:
    """Lightweight RAG system for tourism knowledge"""
    
    def __init__(self):
        self.knowledge_base = self._init_knowledge_base()
        self.cache = {}
    
    def _init_knowledge_base(self):
        """Initialize simple knowledge base"""
        return {
            'sustainability': {
                'carbon_neutral': 'Achieve carbon neutrality through renewable energy, efficient transportation, and verified offset programs.',
                'waste_management': 'Implement circular economy principles with 95%+ waste diversion through recycling and composting.',
                'water_conservation': 'Deploy smart water systems with rainwater harvesting and greywater recycling.',
                'biodiversity': 'Protect ecosystems through visitor quotas, habitat restoration, and wildlife corridors.'
            },
            'marketing': {
                'green_marketing': 'Promote eco-credentials through transparent impact reporting and third-party certifications.',
                'digital_strategy': 'Leverage social media, influencer partnerships, and virtual experiences for reach.',
                'community_marketing': 'Highlight authentic local experiences and community benefit stories.',
                'educational_focus': 'Market learning outcomes and skill development opportunities.'
            },
            'operations': {
                'visitor_management': 'Use dynamic pricing and real-time capacity monitoring to manage flow.',
                'staff_training': 'Comprehensive sustainability and cultural sensitivity training programs.',
                'technology_integration': 'IoT sensors, mobile apps, and AI analytics for optimization.',
                'partnership_development': 'Collaborate with local businesses, NGOs, and government agencies.'
            },
            'economics': {
                'revenue_optimization': 'Premium pricing for sustainable experiences with clear value proposition.',
                'cost_reduction': 'Energy efficiency, waste reduction, and operational automation.',
                'roi_calculation': 'Track environmental, social, and economic returns on investment.',
                'funding_sources': 'Green bonds, impact investments, and government sustainability grants.'
            }
        }
    
    def query_knowledge(self, query: str) -> str:
        """Simple knowledge retrieval"""
        query_lower = query.lower()
        
        # Check cache first
        if query in self.cache:
            return self.cache[query]
        
        # Simple keyword matching
        responses = []
        
        for category, topics in self.knowledge_base.items():
            for topic, content in topics.items():
                # Check if query keywords match topic
                if any(word in topic for word in query_lower.split()) or \
                   any(word in content.lower() for word in query_lower.split()):
                    responses.append({
                        'category': category,
                        'topic': topic,
                        'content': content,
                        'relevance': self._calculate_relevance(query_lower, topic, content)
                    })
        
        # Sort by relevance and format response
        responses.sort(key=lambda x: x['relevance'], reverse=True)
        formatted_response = self._format_response(query, responses[:3])
        
        # Cache the response
        self.cache[query] = formatted_response
        return formatted_response
    
    def _calculate_relevance(self, query: str, topic: str, content: str) -> float:
        """Calculate simple relevance score"""
        query_words = set(query.split())
        topic_words = set(topic.split('_'))
        content_words = set(content.lower().split())
        
        topic_overlap = len(query_words.intersection(topic_words))
        content_overlap = len(query_words.intersection(content_words))
        
        return topic_overlap * 2 + content_overlap
    
    def _format_response(self, query: str, responses: List[Dict]) -> str:
        """Format the response nicely"""
        if not responses:
            return "I don't have specific information about that topic in my knowledge base."
        
        formatted = f"**Knowledge Base Response for: '{query}'**\n\n"
        
        for i, resp in enumerate(responses, 1):
            formatted += f"**{i}. {resp['topic'].replace('_', ' ').title()}** ({resp['category']})\n"
            formatted += f"{resp['content']}\n\n"
        
        return formatted

# Global instance
simple_rag = SimpleRAG()
