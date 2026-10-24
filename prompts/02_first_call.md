# 02 · What is an LLM: our first call

In this video we make our first call to an LLM, in two ways:
All the code goes in one new file, 02_first_call.py.

## Step 1

Create a new file 02_first_call.py.
Make our first call to the LLM with only a user prompt, no system prompt:
"In one sentence, what is a large language model?" - define this as a variable called user_prompt.
Print "Method 1:" and then the LLM's answer.

## Step 2

Below Method 1, add a second call with the same question.
This time, also send a system prompt:
"You are a friendly teacher. Explain things so a 10-year-old can understand, in one short sentence." - define this as a variable called system_prompt.
Print "Method 2:" and then the LLM's answer.
Keep Method 1 as it is.

## Step 3

Comment out the code for Method-1
Extend the Method-2 code to accept the user prompt as an input.
Take this input and send it to the LLM and print the answer so that it looks like a conversational chatbot.
To exit out of the chat - the user has to type "quit".
