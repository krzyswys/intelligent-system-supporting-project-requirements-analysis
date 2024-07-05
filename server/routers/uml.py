import json
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from server.database import project_collection
from server.modules.uml.routes import UmlModule
from server.utils.openaiUtils import Model
from pymongo import ReturnDocument
from server.models import UmlsModel

router = APIRouter(
    tags=["uml"],
    prefix="/uml",
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{project_id}",
)
async def get_uml(project_id: str):
    if (
        project := await project_collection.find_one({"_id": ObjectId(project_id)})
    ) is not None:

        uml = project["umls"]
        return uml
    else:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")


@router.post("/generate/{project_id}")
async def generate_uml(project_id: str):
    print(f"Generating uml for project {project_id}")
    project = await project_collection.find_one({"_id": ObjectId(project_id)})
    if project:
        uml = UmlModule(Model.GPT3)
        for_who = project["for_who"]
        doing_what = project["doing_what"]
        additional_info = project["additional_info"]
        content = uml.get_content(
            for_who,
            doing_what,
            additional_info,
            False,
        )
        print(content)

        data = json.loads(content)
        uml_model = UmlsModel(**data)
        project["umls"] = uml_model.dict()
        await project_collection.find_one_and_update(
            {"_id": ObjectId(project_id)},
            {"$set": project},
            return_document=ReturnDocument.AFTER,
        )
        return uml_model
    raise HTTPException(status_code=404, detail=f"Project {project_id} not found")