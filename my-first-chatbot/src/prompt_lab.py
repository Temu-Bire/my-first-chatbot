from .llm import call_llm

def run_prompt(prompt, text):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]

    return call_llm(messages)

def run_multiple(prompts, text):
    results = []
    for p in prompts:
        if p.strip():
            results.append(run_prompt(p, text))
        else:
            results.append("")
    return results