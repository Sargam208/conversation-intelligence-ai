from langchain_core.prompts import ChatPromptTemplate


SUMMARY_PROMPT = ChatPromptTemplate.from_template(
"""
You are an expert Conversation Intelligence AI.

Analyze the conversation and return ONLY the JSON in the required format.

{format_instructions}

Guidelines:

1. Executive Summary
- Write a concise professional summary (5-8 sentences).
- Mention the main purpose of the conversation.
- Mention the final outcome if one exists.
- Mention important bookings, purchases, plans or agreements.

2. Key Discussion Points
- Return 5-10 precise discussion topics.
- Use specific names instead of generic words.
Examples:
- Kasol Trip Planning
- The Hosteller Kasol Booking
- ZingBus Reservation
- Splitwise Expense Sharing
NOT:
- Travel
- Hotel
- Discussion

3. Important Decisions
Extract ONLY decisions that were actually finalized.

Each decision must contain:
- title
- details
- confidence

Examples:
Title:
Accommodation Finalized

Details:
The group finalized The Hosteller Kasol for the stay from 18-20 May.

Do NOT include suggestions or discussions.

4. Action Items
Extract every actionable task.

For every task identify:
- assignee
- task
- deadline
- priority

Examples:

Assignee:
Divyam

Task:
Complete web check-in for ZingBus.

Deadline:
Before departure.

Priority:
High

5. Deadlines
Include:
- Check-in dates
- Check-out dates
- Bus timings
- Payment deadlines
- Meeting timings
- Submission dates

6. Preserve Important Entities

Always preserve exact names whenever available:

- Hotels
- Hostels
- Bus operators
- Flight numbers
- Train names
- Cafes
- Restaurants
- Places
- Payment apps
- UPI IDs
- Booking IDs
- Phone numbers
- Prices
- Amounts
- Dates
- Times

Never replace them with generic words like:
hotel
bus
friend
location
payment

7. Ignore

Ignore:
- greetings
- emojis
- stickers
- reactions
- repeated messages
- casual small talk
- one-word acknowledgements

Only extract information that is useful later.

Conversation:

{conversation}
"""
)

TOPIC_PROMPT = ChatPromptTemplate.from_template(
    """
Identify the major topics discussed in this conversation.

Return ONLY a comma-separated list.

Conversation:
{conversation}
"""
)

MERGE_SUMMARY_PROMPT = ChatPromptTemplate.from_template(
"""
You are an expert Conversation Intelligence AI.

Below are summaries generated from different parts of the SAME conversation.

Merge them into ONE coherent summary.

Rules:
- Remove duplicate information.
- Keep all important decisions.
- Keep all action items.
- Keep all deadlines.
- Preserve names, places, hotels, bus names and dates.
- Do NOT invent information.
- Return ONLY valid JSON.

{format_instructions}

Chunk Summaries:

{summaries}
"""
)
TASK_PROMPT = ChatPromptTemplate.from_template(
    """
Extract all action items.

Return JSON.

Conversation:
{conversation}
"""
)


QUESTION_PROMPT = ChatPromptTemplate.from_template(
    """
Answer the user's question ONLY using the provided context.

If the answer is not present, reply:
"I couldn't find that information in the conversation."

Context:
{context}

Question:
{question}
"""
)
MAP_PROMPT = ChatPromptTemplate.from_template(
"""
You are an expert Conversation Intelligence AI.

You are analyzing ONLY ONE PART of a long conversation.

Extract ONLY the important information.

Focus on:

- important events
- decisions made
- action items
- deadlines
- names of people
- places
- hotels
- bus/train/flight names
- payment details
- booking confirmations
- links
- phone numbers
- expenses
- important dates

Ignore greetings, emojis, jokes, stickers and casual chat.

Write a concise factual summary.

Conversation Chunk:

{conversation}
"""
)
REDUCE_PROMPT = ChatPromptTemplate.from_template(
"""
You are a senior Conversation Intelligence AI.

You are given summaries from multiple parts of the same conversation.

Merge them into ONE professional report.

Your report must contain:

## Executive Summary

## Major Discussion Topics

## Important Decisions

## Action Items

## Deadlines

Merge duplicate information.

Preserve names exactly.

Preserve hotel names, locations, booking IDs, bus names, payment apps, prices, dates and links whenever present.

Do not invent information.

Chunk Summaries:

{summaries}
"""
)