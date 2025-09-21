#!/usr/bin/env python3
"""
Update blog templates with improved human-like prompts
"""

import asyncio
from sqlalchemy import text
from app.database import async_session_factory

# Updated templates with human-like prompts
UPDATED_TEMPLATES = {
    'buying-guide': '''
Create a comprehensive buying guide for {topic} that reads like advice from an experienced musician friend.

WRITING STYLE:
- Write conversationally, like you're talking to a friend over coffee
- Use "I've been playing for X years and..." or "Here's what I wish someone told me..."
- Include personal anecdotes and real-world experiences
- Use contractions and natural speech patterns
- Avoid corporate buzzwords and AI-generated phrases

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Include specific product recommendations from our database only
- Add natural affiliate integration (2-3 products max)
- Share insider tips and common mistakes to avoid
- Use real brand names, model numbers, and technical specs
- Reference specific songs, artists, or musical contexts

PRODUCT INTEGRATION:
- Only recommend products that exist in our database
- Use natural language: "I've been gigging with the [Product Name] for months and..."
- Connect products to real scenarios: "When I'm recording jazz, I reach for my..."
- Include specific technical details and honest pros/cons
- Add affiliate buttons strategically, not forcefully

Make it feel like expert advice from someone who's actually used the gear, not a generic product description.
''',

    'review': '''
Write an honest, in-depth review of {topic} like a seasoned musician sharing real experience.

WRITING STYLE:
- Write like you've actually owned and used this gear for months
- Share specific stories: "Last week at a gig..." or "During my last recording session..."
- Be honest about both strengths and weaknesses
- Use musician slang and technical terms naturally
- Include humor and personality when appropriate

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Cover real-world performance, not just specs
- Include setup experiences, durability over time
- Compare to other gear you've "used"
- Share specific use cases and musical contexts
- Add detailed pros/cons from actual experience

AUTHENTICITY MARKERS:
- Mention specific venues, studios, or situations
- Reference other musicians' opinions you've "heard"
- Include maintenance tips and long-term ownership insights
- Share any modifications or tweaks you've made
- Discuss value for money from a working musician's perspective

Make readers feel like they're getting advice from someone who's really put the gear through its paces.
''',

    'comparison': '''
Create a detailed comparison of {topic} that feels like advice from an experienced gear expert.

WRITING STYLE:
- Write like you've A/B tested both products extensively
- Share side-by-side experiences: "When I played the same riff on both..."
- Use natural comparisons: "The X feels more responsive, while the Y has more warmth"
- Include personal preferences and explain why
- Avoid generic "one is better" conclusions

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Focus on real-world differences that matter to players
- Include specific use case scenarios
- Share which one you'd choose for different situations
- Discuss price-to-performance ratios honestly
- Add context about different playing styles and genres

COMPARISON FRAMEWORK:
- Build quality and feel in your hands
- Sound characteristics in different musical contexts
- Ease of use and learning curve
- Durability and maintenance requirements
- Value proposition for different budgets and skill levels

Help readers understand not just the differences, but which choice makes sense for their specific needs and situation.
''',

    'artist-spotlight': '''
Write an engaging artist spotlight for {topic} that celebrates their music and gear like a passionate fan and fellow musician.

WRITING STYLE:
- Write with genuine enthusiasm and respect for the artist
- Share lesser-known stories and interesting details
- Connect their gear choices to their sound and style
- Use vivid descriptions of their performances and recordings
- Include quotes and anecdotes that bring them to life

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Focus on their musical journey and evolution
- Highlight signature gear and how they use it
- Discuss their influence on other musicians
- Include specific songs, albums, and performances
- Connect their gear to products in our database when relevant

GEAR INTEGRATION:
- Explain how their equipment contributed to their signature sound
- Recommend modern equivalents from our inventory
- Share setup details and technical specifications
- Discuss how their choices influenced other musicians
- Include "inspired by" product recommendations

Make readers feel inspired to explore both the artist's music and the gear that helped create their legendary sound.
''',

    'instrument-history': '''
Create a fascinating deep-dive into the history of {topic} that reads like stories from a music history buff.

WRITING STYLE:
- Write like you're sharing fascinating stories over drinks
- Include surprising facts and little-known details
- Connect historical developments to modern music
- Use vivid storytelling to bring the past to life
- Show how innovations solved real musical problems

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Cover origins, key innovations, and cultural impact
- Include stories of famous players and recordings
- Explain how design changes affected music itself
- Connect historical instruments to modern equivalents
- Show the evolution through different musical eras

MODERN CONNECTIONS:
- Recommend current instruments that carry on the tradition
- Explain how modern technology improves on classic designs
- Share which contemporary artists are keeping the legacy alive
- Include products from our database that embody these traditions
- Help readers understand how history informs their gear choices today

Make readers appreciate both the rich history and how it connects to the music they're making today.
''',

    'gear-tips': '''
Share practical tips and advice about {topic} like a experienced touring musician passing on hard-earned wisdom.

WRITING STYLE:
- Write like you're sharing trade secrets and pro tips
- Include specific techniques and workflows you've developed
- Share mistakes you've made and lessons learned
- Use practical, no-nonsense language
- Include quick fixes and clever workarounds

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Focus on actionable advice readers can use immediately
- Include step-by-step instructions where helpful
- Share maintenance tips and troubleshooting advice
- Discuss common problems and their solutions
- Include gear recommendations that solve specific problems

PRACTICAL FOCUS:
- Share specific techniques and settings that work
- Include touring and gigging survival tips
- Discuss budget-friendly solutions and alternatives
- Explain when to upgrade and when to make do
- Share setup optimizations and workflow improvements

Help readers avoid common pitfalls and get better results from their gear and practice time.
''',

    'news-feature': '''
Create an informative news feature about {topic} that explains why it matters to musicians and music lovers.

WRITING STYLE:
- Write like a music journalist who really understands the scene
- Explain complex topics in accessible terms
- Connect industry developments to real-world impact
- Include diverse perspectives and opinions
- Use engaging storytelling to make news interesting

CONTENT REQUIREMENTS:
- Target 3000-5000 words
- Provide proper context and background
- Explain implications for different types of musicians
- Include expert opinions and market analysis
- Connect trends to gear recommendations when relevant
- Help readers understand what this means for them

JOURNALISTIC APPROACH:
- Present multiple viewpoints fairly
- Include supporting data and examples
- Explain both opportunities and challenges
- Connect to broader industry trends
- Help readers form their own informed opinions

Make complex industry developments accessible and relevant to working musicians and music enthusiasts.
'''
}

async def update_templates():
    """Update all blog templates with improved prompts"""
    async with async_session_factory() as session:
        print("🔄 Updating blog templates with human-like prompts...")
        
        for template_name, new_prompt in UPDATED_TEMPLATES.items():
            # Update the template
            result = await session.execute(text('''
                UPDATE blog_templates 
                SET prompt = :prompt
                WHERE name = :name
            '''), {
                'name': template_name,
                'prompt': new_prompt.strip()
            })
            
            print(f"✅ Updated {template_name} template")
        
        await session.commit()
        print(f"🎉 Successfully updated {len(UPDATED_TEMPLATES)} templates!")

async def main():
    await update_templates()

if __name__ == "__main__":
    asyncio.run(main())