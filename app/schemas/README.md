
# Schemas Layer 📋

**Week 2: Pydantic Data Models + API Contracts**

Structured input/output for idea validation. Type-safe contracts for all layers.

## 🎯 Purpose

- **Input**: `IdeaInput` - User startup ideas (your original design preserved)
- **Output**: `ValidationReport` - Structured agent results (Week 5-6)
- **Contracts**: Exact API shapes for FastAPI + agent tooling
- **Validation**: Runtime type checking + examples
- **API Contracts**: Define exact JSON shapes for `/validate-idea` endpoint
- **Type Safety**: Validate inputs/outputs across MCP layers
- **Documentation**: Auto-generate OpenAPI docs via FastAPI

# Schema validation
pytest tests/test_schemas.py

# API contract testing  
pytest tests/test_main.py::test_validate_idea_placeholder

# Live docs
http://localhost:8000/docs  # Auto-generated Swagger

