
check_if_web_search_is_necessary = """
<GOAL>
Your goal is to determine if the user prompt requires a web search to answer accurately from your perspective.
</GOAL>

<CONTEXT>
The current date is {current_date}.
</CONTEXT>

<USER_PROMPT>
{user_prompt}
</USER_PROMPT>

<FORMAT>
Format your response as either a boolean True or False.
</FORMAT>

<EXAMPLE>
Example input: Hello
Example output: False

Example input: Who is the current US president?
Example output: True
</EXAMPLE>
"""

generate_query_from_user_prompt = """
<GOAL>
Your goal is to generate the most optimal web search query to answer the user prompt. In other words,
if you were using a search engine to find relevant information to answer the user prompt, what keywords
would you use?
You must also determine the most relevant topic for that query from the following list of
possible topics: general, news, finance.
</GOAL>

<CONTEXT>
The current date is {current_date}.
</CONTEXT>

<USER_PROMPT>
{user_prompt}
</USER_PROMPT>

<FORMAT>
Format your response to be a JSON string containing the following keys:
- query: The web search query
- topic: The topic
</FORMAT>
"""