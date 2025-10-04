#!/usr/bin/env python3
"""
创建Mock Agent数据的脚本
"""
import asyncio
import json
from datetime import datetime, timedelta
import random
from decimal import Decimal

from sqlalchemy import select
from agentpedia.core.database import AsyncSessionLocal
from agentpedia.models.agent import Agent, AgentType, AgentStatus, AgentVisibility, ModelProvider
from agentpedia.models.user import User


async def create_mock_agents():
    """创建Mock Agent数据"""
    async with AsyncSessionLocal() as session:
        # 检查是否已有mock用户
        result = await session.execute(
            select(User).where(User.username == "mock_admin")
        )
        mock_user = result.scalar_one_or_none()

        if not mock_user:
            print("Mock admin user not found. Please run the application first to create the mock user.")
            return

        # Mock Agent数据
        mock_agents = [
            {
                "name": "ChatGPT Plus",
                "description": "OpenAI's advanced conversational AI model with enhanced capabilities",
                "type": AgentType.CHATBOT,
                "visibility": AgentVisibility.PUBLIC,
                "model_provider": ModelProvider.OPENAI,
                "model_name": "gpt-4",
                "model_version": "4.0",
                "system_prompt": "You are a helpful AI assistant with advanced reasoning capabilities.",
                "temperature": 0.7,
                "max_tokens": 4096,
                "website_url": "https://openai.com",
                "one_liner": "Advanced conversational AI with superior reasoning and creativity",
                "tags": json.dumps(["AI", "Chat", "Productivity", "Writing", "Analysis"]),
                "detailed_description": """# ChatGPT Plus

ChatGPT Plus is OpenAI's premium conversational AI service that provides access to advanced language models including GPT-4. This powerful AI assistant can help with a wide range of tasks including writing, analysis, coding, research, and creative endeavors.

## Key Features

- **Advanced Reasoning**: Superior logical thinking and problem-solving capabilities
- **Creative Writing**: Generate stories, poems, scripts, and other creative content
- **Code Generation**: Write and debug code in multiple programming languages
- **Research Assistant**: Help with information gathering and analysis
- **Multilingual Support**: Communicate in dozens of languages

## Use Cases

- Professional writing and editing
- Software development and debugging
- Academic research and homework help
- Creative projects and brainstorming
- Data analysis and visualization

## Pricing

Available through OpenAI's subscription model at $20/month with unlimited access to GPT-4 and other premium features.""",
                "pricing_info": json.dumps([
                    {"tier": "Monthly", "price": 20.0, "currency": "USD", "features": ["Unlimited GPT-4 access", "Priority access", "Advanced features"]}
                ]),
                "average_rating": 4.7,
                "total_ratings": 15234,
                "total_reviews": 3421,
                "total_favorites": 8932,
                "monthly_active_users": 1500000,
                "annual_active_users": 8500000,
                "annual_recurring_revenue": 204000000.0,
                "monthly_recurring_revenue": 17000000.0,
                "growth_rate": 45.2,
                "traffic_rank": 42,
                "published_at": datetime.utcnow() - timedelta(days=365)
            },
            {
                "name": "Claude Pro",
                "description": "Anthropic's constitutional AI assistant with strong safety principles",
                "type": AgentType.ASSISTANT,
                "visibility": AgentVisibility.PUBLIC,
                "model_provider": ModelProvider.ANTHROPIC,
                "model_name": "claude-3-sonnet",
                "model_version": "3.0",
                "system_prompt": "You are Claude, an AI assistant designed to be helpful, harmless, and honest.",
                "temperature": 0.6,
                "max_tokens": 4096,
                "website_url": "https://anthropic.com",
                "one_liner": "Constitutional AI assistant with exceptional analytical capabilities",
                "tags": json.dumps(["AI", "Analysis", "Writing", "Safe", "Productivity"]),
                "detailed_description": """# Claude Pro

Claude Pro is Anthropic's premium AI assistant built with constitutional AI principles. It excels at analytical tasks, complex reasoning, and maintaining safety while providing helpful responses.

## Key Features

- **Constitutional AI**: Built with strong safety and ethical principles
- **Analytical Excellence**: Exceptional at complex analysis and reasoning
- **Long Context**: Can process and understand very long documents
- **Safety First**: Designed to avoid harmful content while remaining helpful
- **Professional Quality**: Excels at business and academic tasks

## Use Cases

- Complex data analysis and interpretation
- Academic research and writing
- Business strategy and planning
- Legal document analysis
- Technical documentation

## Pricing

Professional subscription at $20/month with enhanced capabilities and priority access.""",
                "pricing_info": json.dumps([
                    {"tier": "Professional", "price": 20.0, "currency": "USD", "features": ["Enhanced capabilities", "Priority access", "Longer context"]}
                ]),
                "average_rating": 4.6,
                "total_ratings": 8932,
                "total_reviews": 2145,
                "total_favorites": 5623,
                "monthly_active_users": 980000,
                "annual_active_users": 5200000,
                "annual_recurring_revenue": 124800000.0,
                "monthly_recurring_revenue": 10400000.0,
                "growth_rate": 38.7,
                "traffic_rank": 67,
                "published_at": datetime.utcnow() - timedelta(days=280)
            },
            {
                "name": "GitHub Copilot",
                "description": "AI-powered code completion and programming assistant",
                "type": AgentType.GENERATOR,
                "visibility": AgentVisibility.PUBLIC,
                "model_provider": ModelProvider.OPENAI,
                "model_name": "gpt-3.5-turbo",
                "model_version": "3.5",
                "system_prompt": "You are a programming assistant that helps developers write better code faster.",
                "temperature": 0.2,
                "max_tokens": 2048,
                "website_url": "https://github.com/features/copilot",
                "one_liner": "AI pair programmer that helps you write code faster and better",
                "tags": json.dumps(["Programming", "Development", "AI", "Productivity", "Code"]),
                "detailed_description": """# GitHub Copilot

GitHub Copilot is an AI-powered code completion tool that helps developers write code faster and more accurately. It acts as an AI pair programmer, suggesting code completions and entire functions in real-time.

## Key Features

- **Real-time Suggestions**: Code completions as you type
- **Multi-language Support**: Works with dozens of programming languages
- **Context Aware**: Understands your project structure and coding style
- **Function Generation**: Can generate entire functions from comments
- **Test Generation**: Helps write unit tests automatically

## Use Cases

- Rapid prototyping and development
- Learning new programming languages
- Code refactoring and optimization
- Writing boilerplate code
- Debugging and troubleshooting

## Pricing

- Individual: $10/month
- Business: $19/month
- Enterprise: Custom pricing""",
                "pricing_info": json.dumps([
                    {"tier": "Individual", "price": 10.0, "currency": "USD", "features": ["Basic features", "Personal use"]},
                    {"tier": "Business", "price": 19.0, "currency": "USD", "features": ["Advanced features", "Team management", "Compliance"]}
                ]),
                "average_rating": 4.4,
                "total_ratings": 12543,
                "total_reviews": 3821,
                "total_favorites": 9876,
                "monthly_active_users": 1200000,
                "annual_active_users": 6800000,
                "annual_recurring_revenue": 163200000.0,
                "monthly_recurring_revenue": 13600000.0,
                "growth_rate": 52.3,
                "traffic_rank": 89,
                "published_at": datetime.utcnow() - timedelta(days=420)
            },
            {
                "name": "Midjourney",
                "description": "AI-powered image generation and artistic creativity tool",
                "type": AgentType.GENERATOR,
                "visibility": AgentVisibility.PUBLIC,
                "model_provider": ModelProvider.CUSTOM,
                "model_name": "midjourney-v5",
                "model_version": "5.2",
                "system_prompt": "Create stunning, artistic, and imaginative images from text descriptions.",
                "temperature": 0.8,
                "max_tokens": 1024,
                "website_url": "https://midjourney.com",
                "one_liner": "Create breathtaking AI art from your imagination",
                "tags": json.dumps(["Art", "Design", "Creative", "Images", "AI"]),
                "detailed_description": """# Midjourney

Midjourney is an independent research lab that produces an artificial intelligence program that creates images from textual descriptions, similar to OpenAI's DALL-E or Stable Diffusion.

## Key Features

- **Artistic Excellence**: Creates highly artistic and detailed images
- **Style Versatility**: Can generate in many artistic styles
- **High Resolution**: Produces high-quality, detailed outputs
- **Community Driven**: Strong artist community and regular updates
- **Iterative Process**: Can refine and improve generated images

## Use Cases

- Digital art and illustration
- Concept art for games and films
- Marketing and advertising visuals
- Book covers and illustrations
- Architectural visualization

## Pricing

- Basic: $10/month (200 images)
- Standard: $30/month (unlimited relaxed images)
- Pro: $60/month (unlimited fast images)
- Mega: $120/month (unlimited everything + priority)""",
                "pricing_info": json.dumps([
                    {"tier": "Basic", "price": 10.0, "currency": "USD", "features": ["200 images/month", "Basic features"]},
                    {"tier": "Standard", "price": 30.0, "currency": "USD", "features": ["Unlimited relaxed images", "Commercial license"]},
                    {"tier": "Pro", "price": 60.0, "currency": "USD", "features": ["Unlimited fast images", "Priority queue"]}
                ]),
                "average_rating": 4.5,
                "total_ratings": 18765,
                "total_reviews": 5432,
                "total_favorites": 15432,
                "monthly_active_users": 1500000,
                "annual_active_users": 7800000,
                "annual_recurring_revenue": 234000000.0,
                "monthly_recurring_revenue": 19500000.0,
                "growth_rate": 67.8,
                "traffic_rank": 156,
                "published_at": datetime.utcnow() - timedelta(days=540)
            },
            {
                "name": "Perplexity AI",
                "description": "AI-powered search engine and research assistant",
                "type": AgentType.ANALYZER,
                "visibility": AgentVisibility.PUBLIC,
                "model_provider": ModelProvider.ANTHROPIC,
                "model_name": "claude-2",
                "model_version": "2.1",
                "system_prompt": "You are an AI research assistant that provides accurate, up-to-date information with citations.",
                "temperature": 0.3,
                "max_tokens": 3072,
                "website_url": "https://perplexity.ai",
                "one_liner": "AI-powered search that gives you answers, not just links",
                "tags": json.dumps(["Search", "Research", "AI", "Information", "Citations"]),
                "detailed_description": """# Perplexity AI

Perplexity AI is an advanced search engine and research assistant that uses artificial intelligence to provide direct answers to questions with citations from reliable sources.

## Key Features

- **Direct Answers**: Provides comprehensive answers instead of just links
- **Real-time Information**: Accesses up-to-date information from the internet
- **Source Citations**: Every answer includes reliable source citations
- **Conversational Interface**: Natural language interaction
- **Research Mode**: Deep analysis for complex topics

## Use Cases

- Academic research and homework
- Business intelligence and market research
- Fact-checking and verification
- Learning new topics
- Professional research and analysis

## Pricing

- Free: Limited searches with basic features
- Pro: $20/month (unlimited searches, advanced features, file uploads)
- Enterprise: Custom pricing with additional features""",
                "pricing_info": json.dumps([
                    {"tier": "Free", "price": 0.0, "currency": "USD", "features": ["Limited searches", "Basic features"]},
                    {"tier": "Pro", "price": 20.0, "currency": "USD", "features": ["Unlimited searches", "Advanced features", "File uploads", "API access"]}
                ]),
                "average_rating": 4.3,
                "total_ratings": 7234,
                "total_reviews": 1821,
                "total_favorites": 4532,
                "monthly_active_users": 870000,
                "annual_active_users": 4200000,
                "annual_recurring_revenue": 100800000.0,
                "monthly_recurring_revenue": 8400000.0,
                "growth_rate": 124.5,
                "traffic_rank": 234,
                "published_at": datetime.utcnow() - timedelta(days=180)
            }
        ]

        # 检查是否已有mock agents数据（检查是否有website_url字段）
        result = await session.execute(select(Agent).where(Agent.website_url.isnot(None)).limit(1))
        existing_mock_agent = result.scalar_one_or_none()

        if existing_mock_agent:
            print("Mock agents already exist in database. Skipping creation.")
            return

        # 删除现有的测试agents（没有website_url的）
        result = await session.execute(select(Agent).where(Agent.website_url.is_(None)))
        test_agents = result.scalars().all()

        if test_agents:
            print(f"Deleting {len(test_agents)} test agents...")
            for agent in test_agents:
                await session.delete(agent)
            await session.commit()
            print("Test agents deleted successfully.")

        # 创建agents
        for agent_data in mock_agents:
            agent = Agent(
                owner_id=mock_user.id,
                **agent_data,
                status=AgentStatus.ACTIVE,
                enable_memory=True,
                enable_tools=False,
                enable_web_search=True,
                enable_code_execution=False,
                max_conversation_length=50,
                memory_window=10,
                rate_limit_per_minute=60,
                rate_limit_per_hour=1000,
                rate_limit_per_day=10000,
                usage_count=random.randint(1000, 100000),
                total_tokens_used=random.randint(100000, 10000000),
                average_response_time=random.uniform(0.5, 3.0),
                success_rate=random.uniform(85.0, 99.5),
                last_used_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
            )
            session.add(agent)

        await session.commit()
        print(f"Created {len(mock_agents)} mock agents successfully!")


if __name__ == "__main__":
    asyncio.run(create_mock_agents())