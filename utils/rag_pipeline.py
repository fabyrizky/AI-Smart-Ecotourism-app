import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import json
import re
from datetime import datetime
import random

class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline for Tourism Knowledge Base
    Combines vector similarity search with contextual generation
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.document_embeddings = self._create_embeddings()
        self.retrieval_cache = {}
        
    def _initialize_knowledge_base(self):
        """Initialize comprehensive tourism knowledge base"""
        return {
            'documents': [
                {
                    'id': 'doc_001',
                    'title': 'Sustainable Tourism Development Guidelines',
                    'content': 'Sustainable tourism development requires careful balance between economic growth, environmental protection, and cultural preservation. Key principles include carrying capacity management, local community involvement, and environmental impact assessment.',
                    'category': 'sustainability',
                    'relevance_score': 9.2,
                    'source': 'UNWTO Guidelines',
                    'last_updated': '2024-01-15'
                },
                {
                    'id': 'doc_002',
                    'title': 'Educational Tourism Best Practices',
                    'content': 'Educational tourism combines learning with travel, offering immersive experiences that enhance knowledge and cultural understanding. Effective programs include hands-on activities, expert guides, and structured learning outcomes.',
                    'category': 'education',
                    'relevance_score': 8.8,
                    'source': 'Tourism Education Institute',
                    'last_updated': '2024-02-01'
                },
                {
                    'id': 'doc_003',
                    'title': 'Green Marketing in Tourism Industry',
                    'content': 'Green marketing in tourism focuses on promoting environmentally responsible travel options. Strategies include eco-certification, carbon footprint transparency, and sustainable accommodation partnerships.',
                    'category': 'marketing',
                    'relevance_score': 9.0,
                    'source': 'Green Tourism Council',
                    'last_updated': '2024-01-20'
                },
                {
                    'id': 'doc_004',
                    'title': 'Cultural Heritage Conservation in Tourism',
                    'content': 'Protecting cultural heritage sites while promoting tourism requires visitor management, conservation funding, and community engagement. Digital documentation and virtual experiences can reduce physical impact.',
                    'category': 'heritage',
                    'relevance_score': 8.7,
                    'source': 'UNESCO Heritage Guidelines',
                    'last_updated': '2024-01-10'
                },
                {
                    'id': 'doc_005',
                    'title': 'Smart Tourism Technology Integration',
                    'content': 'Smart tourism leverages IoT, AI, and big data to enhance visitor experiences and optimize resource management. Applications include crowd monitoring, personalized recommendations, and predictive analytics.',
                    'category': 'technology',
                    'relevance_score': 8.9,
                    'source': 'Smart Tourism Research Lab',
                    'last_updated': '2024-02-05'
                },
                {
                    'id': 'doc_006',
                    'title': 'Community-Based Tourism Development',
                    'content': 'Community-based tourism empowers local communities to control and benefit from tourism development. This approach ensures cultural authenticity, environmental protection, and equitable economic distribution.',
                    'category': 'community',
                    'relevance_score': 9.1,
                    'source': 'Community Tourism Network',
                    'last_updated': '2024-01-25'
                },
                {
                    'id': 'doc_007',
                    'title': 'Carbon Neutral Tourism Strategies',
                    'content': 'Achieving carbon neutrality in tourism requires comprehensive emission reduction and offset programs. Key strategies include renewable energy adoption, efficient transportation, and verified carbon credits.',
                    'category': 'environment',
                    'relevance_score': 9.3,
                    'source': 'Climate Action Tourism',
                    'last_updated': '2024-02-10'
                },
                {
                    'id': 'doc_008',
                    'title': 'Visitor Experience Optimization',
                    'content': 'Optimizing visitor experiences involves understanding visitor motivations, preferences, and behaviors. Data analytics, personalization technologies, and continuous feedback collection are essential tools.',
                    'category': 'experience',
                    'relevance_score': 8.6,
                    'source': 'Visitor Experience Research Center',
                    'last_updated': '2024-01-30'
                },
                {
                    'id': 'doc_009',
                    'title': 'Digital Transformation in Tourism',
                    'content': 'Digital transformation revolutionizes tourism through mobile apps, virtual reality, blockchain verification, and AI-powered services. These technologies enhance efficiency, transparency, and visitor satisfaction.',
                    'category': 'digital',
                    'relevance_score': 8.8,
                    'source': 'Digital Tourism Initiative',
                    'last_updated': '2024-02-08'
                },
                {
                    'id': 'doc_010',
                    'title': 'Biodiversity Conservation in Eco-Tourism',
                    'content': 'Eco-tourism can support biodiversity conservation through education, research funding, and habitat protection. Successful programs balance visitor access with ecosystem preservation.',
                    'category': 'conservation',
                    'relevance_score': 9.0,
                    'source': 'Biodiversity Tourism Alliance',
                    'last_updated': '2024-01-18'
                }
            ],
            'regulations': [
                {
                    'id': 'reg_001',
                    'title': 'Environmental Impact Assessment Regulation',
                    'content': 'Tourism developments must undergo environmental impact assessments to evaluate potential ecological effects and mitigation measures.',
                    'jurisdiction': 'National',
                    'compliance_level': 'Mandatory',
                    'effective_date': '2024-01-01'
                },
                {
                    'id': 'reg_002',
                    'title': 'Cultural Heritage Protection Law',
                    'content': 'Tourism activities near cultural heritage sites must comply with protection standards and visitor management protocols.',
                    'jurisdiction': 'Regional',
                    'compliance_level': 'Mandatory',
                    'effective_date': '2023-06-15'
                },
                {
                    'id': 'reg_003',
                    'title': 'Sustainable Tourism Certification Standards',
                    'content': 'Tourism operators can obtain sustainability certification by meeting environmental, social, and economic criteria.',
                    'jurisdiction': 'International',
                    'compliance_level': 'Voluntary',
                    'effective_date': '2024-03-01'
                }
            ],
            'trends': [
                {
                    'id': 'trend_001',
                    'name': 'AI-Powered Personalization',
                    'description': 'Artificial intelligence enables personalized tourism experiences based on visitor preferences and behaviors.',
                    'adoption_rate': 0.35,
                    'growth_projection': 0.85,
                    'impact_level': 'High'
                },
                {
                    'id': 'trend_002',
                    'name': 'Virtual and Augmented Reality',
                    'description': 'VR/AR technologies create immersive educational experiences and virtual destination previews.',
                    'adoption_rate': 0.28,
                    'growth_projection': 0.75,
                    'impact_level': 'Medium'
                },
                {
                    'id': 'trend_003',
                    'name': 'Blockchain Verification',
                    'description': 'Blockchain technology provides transparent verification of sustainability claims and certifications.',
                    'adoption_rate': 0.15,
                    'growth_projection': 0.65,
                    'impact_level': 'Medium'
                },
                {
                    'id': 'trend_004',
                    'name': 'Carbon Footprint Tracking',
                    'description': 'Real-time carbon footprint tracking helps tourists make environmentally conscious decisions.',
                    'adoption_rate': 0.42,
                    'growth_projection': 0.90,
                    'impact_level': 'High'
                }
            ]
        }
    
    def _create_embeddings(self):
        """Create simple embeddings for document similarity"""
        # Simplified embedding simulation - in production, use proper embeddings
        embeddings = {}
        
        for doc in self.knowledge_base['documents']:
            # Create simple embedding based on keywords and content
            content = doc['content'].lower()
            embedding = self._text_to_vector(content)
            embeddings[doc['id']] = embedding
            
        return embeddings
    
    def _text_to_vector(self, text: str) -> np.ndarray:
        """Convert text to vector representation (simplified)"""
        # Keywords for different categories
        keywords = {
            'sustainability': ['sustainable', 'environment', 'green', 'eco', 'carbon', 'renewable'],
            'education': ['education', 'learning', 'knowledge', 'teaching', 'academic', 'research'],
            'technology': ['technology', 'digital', 'ai', 'smart', 'innovation', 'data'],
            'community': ['community', 'local', 'culture', 'heritage', 'tradition', 'social'],
            'tourism': ['tourism', 'travel', 'visitor', 'destination', 'experience', 'hospitality']
        }
        
        # Create vector based on keyword frequency
        vector = np.zeros(len(keywords))
        
        for i, (category, category_keywords) in enumerate(keywords.items()):
            for keyword in category_keywords:
                if keyword in text:
                    vector[i] += text.count(keyword)
        
        # Normalize vector
        if np.linalg.norm(vector) > 0:
            vector = vector / np.linalg.norm(vector)
            
        return vector
    
    def retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents for a query"""
        # Check cache first
        cache_key = f"{query}_{top_k}"
        if cache_key in self.retrieval_cache:
            return self.retrieval_cache[cache_key]
        
        # Create query embedding
        query_vector = self._text_to_vector(query.lower())
        
        # Calculate similarities
        similarities = []
        for doc in self.knowledge_base['documents']:
            doc_vector = self.document_embeddings[doc['id']]
            similarity = self._cosine_similarity(query_vector, doc_vector)
            
            # Boost similarity based on category relevance
            category_boost = self._get_category_boost(query, doc['category'])
            final_score = similarity * (1 + category_boost)
            
            similarities.append({
                'document': doc,
                'similarity': final_score,
                'base_similarity': similarity,
                'category_boost': category_boost
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_documents = [item['document'] for item in similarities[:top_k]]
        
        # Cache results
        self.retrieval_cache[cache_key] = top_documents
        
        return top_documents
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _get_category_boost(self, query: str, category: str) -> float:
        """Get category-specific boost for relevance scoring"""
        query_lower = query.lower()
        
        category_keywords = {
            'sustainability': ['sustainable', 'green', 'eco', 'environment', 'carbon', 'climate'],
            'education': ['education', 'learning', 'teach', 'student', 'academic', 'curriculum'],
            'marketing': ['marketing', 'promotion', 'campaign', 'brand', 'advertising'],
            'technology': ['technology', 'digital', 'ai', 'smart', 'innovation', 'app'],
            'heritage': ['heritage', 'culture', 'history', 'tradition', 'monument'],
            'community': ['community', 'local', 'resident', 'stakeholder', 'participation'],
            'environment': ['environment', 'ecosystem', 'biodiversity', 'conservation'],
            'experience': ['experience', 'visitor', 'satisfaction', 'service', 'quality'],
            'digital': ['digital', 'online', 'virtual', 'augmented', 'mobile'],
            'conservation': ['conservation', 'protection', 'preserve', 'wildlife', 'habitat']
        }
        
        if category in category_keywords:
            keywords = category_keywords[category]
            matches = sum(1 for keyword in keywords if keyword in query_lower)
            return min(matches * 0.2, 0.5)  # Max boost of 50%
        
        return 0.0
    
    def generate_rag_response(self, query: str) -> str:
        """Generate response using retrieved documents"""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_documents(query, top_k=3)
        
        # Create context from retrieved documents
        context = self._create_context(relevant_docs)
        
        # Generate response based on context and query
        response = self._generate_contextual_response(query, context, relevant_docs)
        
        return response
    
    def _create_context(self, documents: List[Dict]) -> str:
        """Create context string from retrieved documents"""
        context_parts = []
        
        for doc in documents:
            context_part = f"Document: {doc['title']}\n"
            context_part += f"Content: {doc['content']}\n"
            context_part += f"Source: {doc['source']}\n"
            context_part += f"Category: {doc['category']}\n"
            context_parts.append(context_part)
        
        return "\n---\n".join(context_parts)
    
    def _generate_contextual_response(self, query: str, context: str, documents: List[Dict]) -> str:
        """Generate response using context and query"""
        # Analyze query intent
        query_intent = self._analyze_query_intent(query)
        
        # Generate response based on intent and context
        if query_intent == 'information_seeking':
            return self._generate_information_response(query, documents)
        elif query_intent == 'strategy_planning':
            return self._generate_strategy_response(query, documents)
        elif query_intent == 'problem_solving':
            return self._generate_solution_response(query, documents)
        else:
            return self._generate_general_response(query, documents)
    
    def _analyze_query_intent(self, query: str) -> str:
        """Analyze the intent behind the query"""
        query_lower = query.lower()
        
        information_keywords = ['what', 'how', 'why', 'when', 'where', 'explain', 'describe']
        strategy_keywords = ['strategy', 'plan', 'approach', 'method', 'implement', 'develop']
        problem_keywords = ['problem', 'issue', 'challenge', 'solution', 'fix', 'improve']
        
        if any(keyword in query_lower for keyword in strategy_keywords):
            return 'strategy_planning'
        elif any(keyword in query_lower for keyword in problem_keywords):
            return 'problem_solving'
        elif any(keyword in query_lower for keyword in information_keywords):
            return 'information_seeking'
        else:
            return 'general'
    
    def _generate_information_response(self, query: str, documents: List[Dict]) -> str:
        """Generate information-focused response"""
        response = "📚 **Information from Knowledge Base:**\n\n"
        
        for i, doc in enumerate(documents, 1):
            response += f"**{i}. {doc['title']}**\n"
            response += f"{doc['content'][:200]}...\n"
            response += f"*Source: {doc['source']}*\n\n"
        
        # Add synthesis
        response += "🔗 **Key Insights:**\n"
        response += self._synthesize_information(documents)
        
        return response
    
    def _generate_strategy_response(self, query: str, documents: List[Dict]) -> str:
        """Generate strategy-focused response"""
        response = "🎯 **Strategic Recommendations Based on Best Practices:**\n\n"
        
        # Extract actionable insights from documents
        strategies = []
        for doc in documents:
            content = doc['content']
            # Extract strategy-related sentences
            if any(word in content.lower() for word in ['strategy', 'approach', 'method', 'implementation']):
                strategies.append({
                    'source': doc['title'],
                    'strategy': content[:150] + "..."
                })
        
        for i, strategy in enumerate(strategies, 1):
            response += f"**Strategy {i}: From {strategy['source']}**\n"
            response += f"{strategy['strategy']}\n\n"
        
        # Add implementation guidance
        response += "📋 **Implementation Steps:**\n"
        response += "1. Assess current situation and resources\n"
        response += "2. Define clear objectives and KPIs\n"
        response += "3. Develop detailed action plan\n"
        response += "4. Implement pilot program\n"
        response += "5. Monitor, evaluate, and scale\n"
        
        return response
    
    def _generate_solution_response(self, query: str, documents: List[Dict]) -> str:
        """Generate problem-solving response"""
        response = "🛠️ **Solution Framework:**\n\n"
        
        # Identify problem elements from query
        response += "**Problem Analysis:**\n"
        response += f"Based on your query about: {query}\n\n"
        
        # Provide solutions from knowledge base
        response += "**Evidence-Based Solutions:**\n"
        for i, doc in enumerate(documents, 1):
            response += f"**Solution {i}: {doc['title']}**\n"
            response += f"• {doc['content'][:100]}...\n"
            response += f"• Source reliability: {doc['relevance_score']}/10\n\n"
        
        # Add success factors
        response += "✅ **Success Factors:**\n"
        response += "• Stakeholder engagement and buy-in\n"
        response += "• Adequate resource allocation\n"
        response += "• Continuous monitoring and adaptation\n"
        response += "• Clear communication and coordination\n"
        
        return response
    
    def _generate_general_response(self, query: str, documents: List[Dict]) -> str:
        """Generate general response"""
        response = "💡 **Knowledge Base Insights:**\n\n"
        
        # Provide relevant information
        for doc in documents:
            response += f"**{doc['title']}**\n"
            response += f"{doc['content']}\n"
            response += f"*Category: {doc['category']} | Source: {doc['source']}*\n\n"
        
        return response
    
    def _synthesize_information(self, documents: List[Dict]) -> str:
        """Synthesize information from multiple documents"""
        categories = set(doc['category'] for doc in documents)
        synthesis = ""
        
        if len(categories) > 1:
            synthesis += "This query spans multiple domains: " + ", ".join(categories) + ".\n"
        
        # Find common themes
        all_content = " ".join(doc['content'] for doc in documents)
        common_keywords = self._extract_common_keywords(all_content)
        
        if common_keywords:
            synthesis += f"Key themes include: {', '.join(common_keywords[:5])}.\n"
        
        synthesis += f"Based on {len(documents)} authoritative sources, the evidence suggests integrated approaches work best."
        
        return synthesis
    
    def _extract_common_keywords(self, text: str) -> List[str]:
        """Extract common keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = {}
        
        # Count word frequencies
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'they', 'have', 'will', 'been', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return most frequent words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words if freq > 1][:10]
    
    def search_regulations(self, query: str) -> List[Dict]:
        """Search relevant regulations"""
        query_lower = query.lower()
        relevant_regulations = []
        
        for reg in self.knowledge_base['regulations']:
            title_match = any(word in reg['title'].lower() for word in query_lower.split())
            content_match = any(word in reg['content'].lower() for word in query_lower.split())
            
            if title_match or content_match:
                relevant_regulations.append(reg)
        
        return relevant_regulations
    
    def get_trend_analysis(self, query: str = "") -> Dict:
        """Get trend analysis based on query or general trends"""
        if query:
            query_lower = query.lower()
            relevant_trends = []
            
            for trend in self.knowledge_base['trends']:
                if any(word in trend['description'].lower() for word in query_lower.split()):
                    relevant_trends.append(trend)
        else:
            relevant_trends = self.knowledge_base['trends']
        
        # Sort by adoption rate and impact
        relevant_trends.sort(key=lambda x: (x['adoption_rate'], x['growth_projection']), reverse=True)
        
        return {
            'trends': relevant_trends,
            'summary': self._generate_trend_summary(relevant_trends)
        }
    
    def _generate_trend_summary(self, trends: List[Dict]) -> str:
        """Generate summary of trends"""
        if not trends:
            return "No specific trends found for this query."
        
        summary = f"Analysis of {len(trends)} relevant trends:\n\n"
        
        for trend in trends[:3]:  # Top 3 trends
            summary += f"• **{trend['name']}**: "
            summary += f"Current adoption at {trend['adoption_rate']:.0%}, "
            summary += f"projected growth to {trend['growth_projection']:.0%}. "
            summary += f"Impact level: {trend['impact_level']}.\n"
        
        # Overall insights
        avg_adoption = np.mean([t['adoption_rate'] for t in trends])
        avg_growth = np.mean([t['growth_projection'] for t in trends])
        
        summary += f"\n**Overall Market Insights:**\n"
        summary += f"• Average current adoption: {avg_adoption:.0%}\n"
        summary += f"• Average projected growth: {avg_growth:.0%}\n"
        summary += f"• Market maturity: {'Early' if avg_adoption < 0.3 else 'Growing' if avg_adoption < 0.6 else 'Mature'}\n"
        
        return summary
    
    def update_knowledge_base(self, new_document: Dict):
        """Add new document to knowledge base"""
        # Assign new ID
        new_id = f"doc_{len(self.knowledge_base['documents']) + 1:03d}"
        new_document['id'] = new_id
        new_document['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        # Add to knowledge base
        self.knowledge_base['documents'].append(new_document)
        
        # Create embedding for new document
        embedding = self._text_to_vector(new_document['content'].lower())
        self.document_embeddings[new_id] = embedding
        
        # Clear cache to ensure fresh retrievals
        self.retrieval_cache.clear()
        
        return new_id
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        docs = self.knowledge_base['documents']
        
        stats = {
            'total_documents': len(docs),
            'categories': {},
            'sources': {},
            'average_relevance': np.mean([doc['relevance_score'] for doc in docs]),
            'last_update': max(doc['last_updated'] for doc in docs),
            'total_regulations': len(self.knowledge_base['regulations']),
            'total_trends': len(self.knowledge_base['trends'])
        }
        
        # Count by category
        for doc in docs:
            category = doc['category']
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        # Count by source
        for doc in docs:
            source = doc['source']
            stats['sources'][source] = stats['sources'].get(source, 0) + 1
        
        return stats
    
    def semantic_search(self, query: str, filters: Dict = None) -> List[Dict]:
        """Advanced semantic search with optional filters"""
        # Get base results
        results = self.retrieve_relevant_documents(query, top_k=10)
        
        # Apply filters if provided
        if filters:
            filtered_results = []
            for doc in results:
                include = True
                
                if 'category' in filters and doc['category'] not in filters['category']:
                    include = False
                
                if 'min_relevance' in filters and doc['relevance_score'] < filters['min_relevance']:
                    include = False
                
                if 'source' in filters and doc['source'] not in filters['source']:
                    include = False
                
                if include:
                    filtered_results.append(doc)
            
            results = filtered_results
        
        return results
    
    def get_document_summary(self, doc_id: str) -> Dict:
        """Get detailed summary of a specific document"""
        doc = next((d for d in self.knowledge_base['documents'] if d['id'] == doc_id), None)
        
        if not doc:
            return {'error': 'Document not found'}
        
        # Generate summary
        content_words = len(doc['content'].split())
        key_topics = self._extract_common_keywords(doc['content'])
        
        summary = {
            'id': doc['id'],
            'title': doc['title'],
            'category': doc['category'],
            'source': doc['source'],
            'relevance_score': doc['relevance_score'],
            'last_updated': doc['last_updated'],
            'word_count': content_words,
            'key_topics': key_topics[:5],
            'content_preview': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
        }
        
        return summary