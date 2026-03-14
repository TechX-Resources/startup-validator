"""
Tests for the prompt templates module (app/prompts/).
Week 2–3: Ensure prompts are well-structured and functions assemble correctly.
Run: pytest tests/test_prompts.py -v
"""

from app.prompts.templates import (
    SYSTEM_PROMPT,
    RESPONSE_FORMAT_INSTRUCTIONS,
    build_user_prompt,
    build_validation_messages,
    build_tool_result_message,
)


# ── Constants ──────────────────────────────────────


class TestPromptConstants:
    def test_system_prompt_is_nonempty_string(self):
        assert isinstance(SYSTEM_PROMPT, str)
        assert len(SYSTEM_PROMPT) > 100

    def test_system_prompt_mentions_output_schema_fields(self):
        for field in ("score", "summary", "strengths", "risks", "competitors", "market_notes"):
            assert field in SYSTEM_PROMPT

    def test_response_format_instructions_is_string(self):
        assert isinstance(RESPONSE_FORMAT_INSTRUCTIONS, str)
        assert "JSON" in RESPONSE_FORMAT_INSTRUCTIONS


# ── build_user_prompt ──────────────────────────────


class TestBuildUserPrompt:
    def test_idea_only(self):
        prompt = build_user_prompt("Uber for dogs")
        assert "Uber for dogs" in prompt
        assert "## Startup Idea" in prompt

    def test_includes_web_results_when_provided(self):
        prompt = build_user_prompt("My idea", web_results="Result snippet here")
        assert "## Web Search Results" in prompt
        assert "Result snippet here" in prompt

    def test_excludes_web_results_when_none(self):
        prompt = build_user_prompt("My idea", web_results=None)
        assert "Web Search Results" not in prompt

    def test_includes_all_tool_sections(self):
        prompt = build_user_prompt(
            "My idea",
            web_results="web data",
            competitor_results="comp data",
            market_results="market data",
            memory_context="past context",
        )
        assert "## Web Search Results" in prompt
        assert "## Competitor Research" in prompt
        assert "## Market Data" in prompt
        assert "## Prior Context" in prompt

    def test_ends_with_instruction(self):
        prompt = build_user_prompt("Test idea")
        assert prompt.strip().endswith("JSON object.")


# ── build_validation_messages ──────────────────────


class TestBuildValidationMessages:
    def test_returns_two_messages(self):
        msgs = build_validation_messages("Test idea")
        assert isinstance(msgs, list)
        assert len(msgs) == 2

    def test_first_message_is_system(self):
        msgs = build_validation_messages("Test idea")
        assert msgs[0]["role"] == "system"
        assert msgs[0]["content"] == SYSTEM_PROMPT

    def test_second_message_is_user(self):
        msgs = build_validation_messages("Test idea")
        assert msgs[1]["role"] == "user"
        assert "Test idea" in msgs[1]["content"]

    def test_tool_results_flow_through(self):
        msgs = build_validation_messages("Test idea", web_results="some data")
        assert "Web Search Results" in msgs[1]["content"]


# ── build_tool_result_message ──────────────────────


class TestBuildToolResultMessage:
    def test_string_result(self):
        msg = build_tool_result_message("WebSearch", "Found 3 results")
        assert msg["role"] == "user"
        assert "WebSearch" in msg["content"]
        assert "Found 3 results" in msg["content"]

    def test_dict_result_serialized(self):
        msg = build_tool_result_message("CompetitorFinder", {"count": 2})
        assert '"count": 2' in msg["content"]

    def test_list_result_serialized(self):
        msg = build_tool_result_message("MarketEstimator", ["$4B TAM"])
        assert "$4B TAM" in msg["content"]
