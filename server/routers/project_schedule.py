"""
This module defines the API routes for interacting with project components, specifically project schedule.
"""

from fastapi import APIRouter, status, Response
from services import get_component
from services import update_component_by_ai
from services import update_component
from models import ComponentIdentify, ProjectSchedule
from .common import UpdateComponentByAIRequest
from generation.project_schedule import ProjectScheduleGenerate
from pydantic import BaseModel


router = APIRouter(
    tags=["model"],
    prefix="/model",
)


@router.get(
    "/project_schedule/{project_id}",
    status_code=status.HTTP_200_OK,
)
def get_project_schedule(project_id: str):
    """
    Retrieves the project schedule component for the specified project.

    :param str project_id: The unique identifier of the project.
    """
    return get_component(project_id, ComponentIdentify.PROJECT_SCHEDULE.value)


@router.post(
    "/project_schedule/ai-update",
    status_code=status.HTTP_200_OK,
)
def update_project_schedule_by_ai(request: UpdateComponentByAIRequest):
    """
    Updates the project schedule component for the specified project using AI-based generation.

    :param UpdateComponentByAIRequest request: The request object containing project ID and query for component update.
    """
    update_component_by_ai(request, ProjectScheduleGenerate)
    return Response(status_code=status.HTTP_200_OK)


class UpdateProjectScheduleRequest(BaseModel):
    """
    The request object for updating the project schedule component by value provided by user.
    """

    project_id: str
    new_val: ProjectSchedule


@router.put(
    "/project_schedule/update",
    status_code=status.HTTP_200_OK,
)
def update_project_schedule(request: UpdateComponentByAIRequest):
    """
    Updates the project schedule component for the specified project using value provided by user.

    :param UpdateProjectScheduleRequest request: The request object containing project ID and new value.
    """
    update_component(request, ProjectScheduleGenerate)
    return Response(status_code=status.HTTP_200_OK)
