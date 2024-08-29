import ray

from typing import List
from pydantic import BaseModel

from models.model import generate_model, save_model_to_database
from modules.actors import ActorsModule
from ai.ai import AI


class Actor(BaseModel):
    name: str
    description: str


class Actors(BaseModel):
    actors: List[Actor]


@ray.remote
def generate_actors(
    for_who: str,
    doing_what: str,
    additional_info: str,
    project_id: str,
    model_ai: type[AI],
):
    actors_module = ActorsModule(model=model_ai())
    actors = generate_model(
        actors_module, for_who, doing_what, additional_info, Actors,
    )
    save_model_to_database(project_id, "actors", actors)
