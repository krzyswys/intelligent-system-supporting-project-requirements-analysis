import ray

from typing import List
from pydantic import BaseModel

from models.model import generate_model, save_model_to_database
from modules.project_schedule.routes import ScheduleModule


class Milestone(BaseModel):
    name: str
    description: str
    duration: str


class ProjectSchedule(BaseModel):
    milestones: List[Milestone]


@ray.remote
def generate_project_schedule(for_who: str, doing_what: str, additional_info: str, project_id: str):
    project_schedule = generate_model(ScheduleModule, for_who, doing_what, additional_info, ProjectSchedule)
    save_model_to_database(project_id, "project_schedule", project_schedule)