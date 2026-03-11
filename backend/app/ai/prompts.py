# backend/app/ai/prompts.py
"""
Prompt templates for AI analysis.
These templates structure how we ask the AI to analyze metrics.
Good prompts = good AI responses.
"""


SYSTEM_PROMPT = """You are a senior financial advisor for startups. You analyze unit economics metrics 
and provide clear, actionable insights to startup founders. 

Your responses should be:
- Clear and simple (avoid jargon unless explaining it)
- Data-driven (reference specific numbers)
- Actionable (give specific recommendations)
- Concise (keep insights focused)

Always structure your analysis with specific metrics and clear recommendations."""


INSIGHTS_PROMPT = """Analyze these startup financial metrics and provide insights:

OVERALL METRICS:
- Total Ad Spend: ${total_ad_spend:,.2f}
- Total Conversions: {total_conversions:,}
- Customer Acquisition Cost (CAC): ${cac:,.2f}
- Estimated Lifetime Value (LTV): ${ltv:,.2f}
- LTV:CAC Ratio: {ltv_cac_ratio:.2f}x
- Monthly Burn Rate: ${burn_rate:,.2f}
- Estimated Runway: {runway:.1f} months
- Is Profitable: {is_profitable}

CHANNEL PERFORMANCE:
{channel_data}

Provide exactly 5 insights in this format:
1. [SEVERITY: good/warning/critical] INSIGHT TITLE: Your analysis here. RECOMMENDATION: Your specific action item.
2. [SEVERITY: good/warning/critical] INSIGHT TITLE: Your analysis here. RECOMMENDATION: Your specific action item.
3. [SEVERITY: good/warning/critical] INSIGHT TITLE: Your analysis here. RECOMMENDATION: Your specific action item.
4. [SEVERITY: good/warning/critical] INSIGHT TITLE: Your analysis here. RECOMMENDATION: Your specific action item.
5. [SEVERITY: good/warning/critical] INSIGHT TITLE: Your analysis here. RECOMMENDATION: Your specific action item.

Focus on: profitability, CAC efficiency, LTV optimization, burn rate concerns, and runway risk."""


CAC_ANALYSIS_PROMPT = """Analyze this Customer Acquisition Cost (CAC) data for a startup:

Overall CAC: ${cac:,.2f}

CAC by Channel:
{channel_cac_data}

Provide a brief analysis (3-4 sentences) covering:
1. Whether the overall CAC is healthy
2. Which channels are most/least efficient
3. One specific recommendation to reduce CAC"""


LTV_ANALYSIS_PROMPT = """Analyze this Customer Lifetime Value (LTV) data:

Overall LTV: ${ltv:,.2f}
LTV:CAC Ratio: {ltv_cac_ratio:.2f}x

LTV by Customer Segment:
{ltv_segment_data}

Provide a brief analysis (3-4 sentences) covering:
1. Whether LTV is healthy relative to CAC
2. Which customer segments are most valuable
3. One recommendation to increase LTV"""


BURN_RATE_PROMPT = """Analyze this startup's burn rate:

Monthly Burn Rate: ${burn_rate:,.2f}
Monthly Revenue: ${revenue:,.2f}
Monthly Expenses: ${expenses:,.2f}
Estimated Runway: {runway:.1f} months

Burn Rate by Channel:
{burn_channel_data}

Provide a brief analysis (3-4 sentences) covering:
1. Whether the burn rate is sustainable
2. Biggest cost drivers
3. One recommendation to reduce burn"""


RUNWAY_ANALYSIS_PROMPT = """Analyze this startup's runway:

Current Runway: {runway:.1f} months
Monthly Burn Rate: ${burn_rate:,.2f}
Bank Balance: ${bank_balance:,.2f}

Scenario Analysis:
{scenario_data}

Provide a brief analysis (3-4 sentences) covering:
1. Whether the runway is safe
2. Most realistic scenario
3. One urgent recommendation if runway is under 12 months"""


CHAT_SYSTEM_PROMPT = """You are an AI financial advisor for startup founders. You have access to the startup's 
financial metrics and can answer questions about:

- Customer Acquisition Cost (CAC) - how much it costs to acquire a customer
- Lifetime Value (LTV) - how much revenue a customer generates over their lifetime
- LTV:CAC Ratio - should be above 3x for a healthy startup
- Burn Rate - monthly cash outflow
- Runway - how many months until the startup runs out of money
- Conversion rates and marketing efficiency
- Channel performance and ROI

CURRENT STARTUP METRICS:
{metrics_context}

Answer the founder's question clearly and concisely. Reference specific numbers from the metrics.
If asked about something not in the data, say so honestly.
Always end with one actionable recommendation."""