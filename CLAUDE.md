# How I like my code

I am a beginner learning building AI agents using python from the very beginning. First I watch the theory video and then I try to write code for the respective video.

## How we work together

- Every video has a prompt file in `prompts/`, with numbered steps (for example `prompts/02_first_call.md`).
  When I say "do step 2", read that file and do only step 2. Nothing from the later steps.
- If a step is not clear, ask me instead of guessing.
- Don't run the code. I run it myself in the terminal.
- Don't do git. I do git myself.
- Never open, read or print `.env`. Never print or hard-code an API key.
- After a change, reply short: which files changed, one line each.
- Please keep your responses very brief.

## Code

- Plain Python: plain functions, short clear names, plain `for` loops.
  No list comprehensions, lambdas, decorators or clever one-liners.
- Write code in such a way a beginner can easily understand.
- If we need to install packages, pause and ask me to run the "uv add" command with the respective package name.
- OpenAI Responses API (`client.responses.create`), model `gpt-4.1-mini`.
- At the top: `load_dotenv()` then `client = OpenAI()`.
- The system prompt is always its own variable, `system_prompt`.
  Every call sends a system message and a user message, unless the step says otherwise.
- Add prints that show what is happening at each step, so we can follow it when we run the code. Prepend logs with [LOG]
- Long calls and dicts: one argument per line.

## Comments

- A plain "we ..." line above every line a beginner could reason about. Say what it does AND why:
  `# we add the tool's result to the list of messages so the LLM can see it in the next call`
- An inline comment on conversions: `json.loads(...)  # string to dict`, `json.dumps(...)  # dict to string`
- Name the concept the first time it shows up: `# this is called a schema`

## Files

- Each lesson's main file starts with the lesson number, for example `02_first_call.py`.
- Don't change earlier lessons' files unless the step says so.
