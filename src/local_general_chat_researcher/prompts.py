
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


summarize_web_search_results = """
<GOAL>
Your goal is to summarize the web search results, retrieving the information
that is most relevant to the user prompt. Do this with the knowledge that they are
web search results.

In other words, ignore any information that is not relevant to the
user prompt (potential ads, website copyrights, other website details that are
not relevant to the user prompt, etc)
</GOAL>

<CONTEXT> 
The current date is {current_date}.
The results that you are being analyzed are web search results and may contain
content that is irrelevant to the user prompt; that content should be ignored.
</CONTEXT>

<USER_PROMPT>
{user_prompt}
</USER_PROMPT>

<SEARCH_RESULT1>
This content is from url: {search_result1_url}.

{search_result1}
</SEARCH_RESULT1>

<SEARCH_RESULT2>
This content is from url: {search_result2_url}.

{search_result2}
</SEARCH_RESULT2>

<FORMAT>
The result will be a JSON string that is a list of objects with the following keys:
- url: the url of the resource that was summarized
- summary: the summary that was generated
</FORMAT>
"""