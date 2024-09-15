"""
This module defines the API routes for interacting with project components, specifically specifications.
"""

from fastapi import APIRouter, status, Response
from services import get_component
from services import update_component_by_ai
from services import update_component
from models import ComponentIdentify, Specifications
from .common import UpdateComponentByAIRequest
from generation.specifications import SpecificationsGenerate
from pydantic import BaseModel


router = APIRouter(
    tags=["model"],
    prefix="/model",
)


@router.get(
    "/specifications/{project_id}",
    status_code=status.HTTP_200_OK,
)
def get_specifications(project_id: str):
    """
    Retrieves the specifications component for the specified project.

    :param str project_id: The unique identifier of the project.
    """
    return get_component(project_id, ComponentIdentify.SPECIFICATIONS.value)


@router.post(
    "/specifications/ai-update",
    status_code=status.HTTP_200_OK,
)
def update_specifications_by_ai(request: UpdateComponentByAIRequest):
    """
    Updates the specifications component for the specified project using AI-based generation.

    :param UpdateComponentByAIRequest request: The request object containing project ID and query for component update.
    """
    update_component_by_ai(request, SpecificationsGenerate)
    return Response(status_code=status.HTTP_200_OK)


class UpdateSpecificationsRequest(BaseModel):
    """
    The request object for updating the specifications component by value provided by user.
    """

    project_id: str
    new_val: Specifications


@router.put(
    "/specifications/update",
    status_code=status.HTTP_200_OK,
)
def update_specifications(request: UpdateSpecificationsRequest):
    """
    Updates the specifications component for the specified project using value provided by user.

    :param UpdateSpecificationsRequest request: The request object containing project ID and new value.
    """
    update_component(request, SpecificationsGenerate)
    return Response(status_code=status.HTTP_200_OK)
