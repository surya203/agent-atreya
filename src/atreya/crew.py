"""Sequential developer crew. Every specialist runs on every task."""

import os
from pathlib import Path
from typing import List

from crewai import Agent, Crew, LLM, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from atreya.models import EngineeringSpec
from atreya.tools.project_files import ReadProjectFileTool, SaveProjectFileTool

load_dotenv()


def build_llm() -> LLM:
    model = os.getenv("MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    if "/" not in model:
        model = f"openai/{model}"
    return LLM(model=model)


@CrewBase
class DevCrew:
    """Tech lead, backend, frontend, and QA, in that order."""

    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    run_dir: str = ""

    def __init__(self, run_dir: str | Path):
        self.run_dir = str(Path(run_dir).resolve())
        Path(self.run_dir).mkdir(parents=True, exist_ok=True)

    def _file_tools(self) -> list:
        return [
            SaveProjectFileTool(run_dir=self.run_dir),
            ReadProjectFileTool(run_dir=self.run_dir),
        ]

    @agent
    def tech_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_lead"],  # type: ignore[index]
            verbose=True,
            llm=build_llm(),
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_engineer"],  # type: ignore[index]
            verbose=True,
            llm=build_llm(),
            tools=self._file_tools(),
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["frontend_engineer"],  # type: ignore[index]
            verbose=True,
            llm=build_llm(),
            tools=self._file_tools(),
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_engineer"],  # type: ignore[index]
            verbose=True,
            llm=build_llm(),
            tools=self._file_tools(),
        )

    @task
    def spec_task(self) -> Task:
        return Task(
            config=self.tasks_config["spec_task"],  # type: ignore[index]
            output_pydantic=EngineeringSpec,
            output_file=str(Path(self.run_dir) / "SPEC.md"),
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_task"],  # type: ignore[index]
            context=[self.spec_task()],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config["frontend_task"],  # type: ignore[index]
            context=[self.spec_task(), self.backend_task()],
        )

    @task
    def qa_task(self) -> Task:
        return Task(
            config=self.tasks_config["qa_task"],  # type: ignore[index]
            context=[self.spec_task(), self.backend_task(), self.frontend_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
