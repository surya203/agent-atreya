"""Structured spec the tech lead hands to the rest of the crew."""

from pydantic import BaseModel, Field


class ApiEndpoint(BaseModel):
    method: str = Field(..., description="HTTP method in uppercase, such as GET or POST.")
    path: str = Field(..., description="URL path starting with /.")
    request_body: str = Field(..., description="Request body shape, or 'none'.")
    response_body: str = Field(..., description="Response body shape.")
    purpose: str = Field(..., description="What this endpoint does.")


class EngineeringSpec(BaseModel):
    summary: str = Field(..., description="What the project does, in a few sentences.")
    api_endpoints: list[ApiEndpoint] = Field(..., description="Endpoints the backend must implement.")
    data_models: list[str] = Field(..., description="Data the app stores, one model per entry.")
    ui_pages: list[str] = Field(..., description="Pages the frontend must build. Use a single page.")
    acceptance_criteria: list[str] = Field(..., description="Checks QA can mark pass, fail, or not checked.")
    file_plan: list[str] = Field(
        ...,
        description="Repo-relative files to create, such as backend/main.py and frontend/index.html.",
    )
