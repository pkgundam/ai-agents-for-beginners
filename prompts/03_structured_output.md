# 03 · Structured Output

In this video we get the LLM's answer back as a filled form, so our code can use it to make decisions.
All the code goes in one new file, 03_structured_output.py.

## Step 1 - the problem. The code responds back with plain text.

1. Create a new file 03_structured_output.py if it does not exist.
2. Define a system prompt: "You are a friendly front-desk assistant for a clinic." - as a variable called system_prompt.
3. Make this a conversational chatbot. The user must enter "quit" to exit the chat
4. inside the while loop 3. Define the user's message - as a variable called user_prompt.
5. define a variable called messages_going_to_llm and add #2 and #4 to it.
6. Invoke the LLM.
7. Print the response

## Step 2 - solution. The code responds back with structured output, a json, a class we define.

Now let's give the LLM a form to fill, instead of a free-text answer.
Use pydantic to define a class called ClinicReply with three fields:

- summary: a short summary of what the patient wants
- intent: only one of "book_appointment", "ask_hours" or "other"
- next_question: the question our assistant should ask next
- Add one line to the system prompt: "Fill every field in the form."
  - Change the call so the LLM returns a filled ClinicReply.
  - print the intent
  - Then our code acts on the intent.
    - book_appointment: print "App: start the booking"
    - ask_hours: print "App: share the clinic hours"
    - anything else: print "App: pass it to the front desk
  - print the next question.
