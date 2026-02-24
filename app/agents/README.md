# app/agents

**Purpose:** Orchestration logic — the “brain” that runs the MCP loop: reason with the LLM, decide which tool to call, execute tools, feed results back, repeat until a final answer is ready.

**What students will implement:**
- **validator_agent.py:** Main agent that:
  1. Takes a startup idea (and optional context from memory).
  2. Uses the LLM (from `app/models`) to decide the next step: either call a tool or produce a final validation response.
  3. Calls tools from `app/tools` and passes results back to the LLM.
  4. Stops when the agent outputs a structured validation (use `app/schemas`).
- Optionally: parse LLM output for tool names + arguments; or use native tool-calling API.

**Weeks:** 5 (core orchestration), with Week 2 (model) and Week 3 (tools) as prerequisites.
