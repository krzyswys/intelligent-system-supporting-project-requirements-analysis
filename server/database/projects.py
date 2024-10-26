"""
This module serves as a Data Access Object (DAO) for performing operations on the chat-related
collections in the MongoDB database. It provides a wrapper around the MongoDB operations for projects.
"""

from typing import Optional, List, Dict

from bson import ObjectId
from datetime import datetime

from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

from models import Project

from .chats import ChatDAO


class ProjectDAO:
    """
    This class provides a DAO for projects in the MongoDB database.
    """

    def __init__(self, mongo_db, collection_name):
        self.collection = mongo_db.get_collection(collection_name)

    def get_project(self, project_id: str) -> Optional[Dict]:
        """
        :param str project_id: The id of the project to retrieve.
        :return: The project with the specified id.
        :rtype: dict
        """
        project = self.collection.find_one({"_id": ObjectId(project_id)})
        return project

    def get_projects_by_owner(self, owner_id: str) -> List[Dict]:
        """
        Returns the projects where the specified user is the owner.

        :param str owner_id: The id of the owner of the projects to retrieve.
        :return: The projects where the specified user is the owner with only id, name, owner, and description.
        :rtype: list of dict
        """
        return list(
            self.collection.find(
                {"owner": ObjectId(owner_id)},
                {"_id": 1, "name": 1, "description": 1, "owner": 1},
            )
        )

    def get_projects_by_member(self, member_id: str) -> List[Dict]:
        """
        Returns the projects where the specified user is a member (but not owner).

        :param str member_id: The id of the member of the projects to retrieve.
        :return: The projects where the specified user is a member (but not owner) with only id, name, owner, and description.
        :rtype: list of dict
        """
        return list(
            self.collection.find(
                {"members": ObjectId(member_id), "owner": {"$ne": ObjectId(member_id)}},
                {"_id": 1, "name": 1, "description": 1, "owner": 1},
            )
        )

    def get_projects_by_member_or_owner(self, user_id: str) -> List[Dict]:
        """
        Returns the projects where the specified user is either the owner or a member.

        :param str user_id: The id of the user to retrieve projects for.
        :return: The projects where the specified user is either the owner or a member with only id, name, owner, and description.
        :rtype: list of dict
        """
        return list(
            self.collection.find(
                {"$or": [{"owner": ObjectId(user_id)}, {"members": ObjectId(user_id)}]},
                {"_id": 1, "name": 1, "description": 1, "owner": 1},
            )
        )

    def get_project_component(self, project_id: str, component_name: str) -> List[Dict]:
        """
        Returns a specific component of a project. (e.g. actors, business_scenarios)

        :param str project_id: The id of the project.
        :param str component_name: The name of the component to retrieve.
        :return: The component of the project with the specified name.
        :rtype: dict
        """
        project = self.get_project(project_id)
        if project and component_name in project:
            return project[component_name]
        else:
            return None

    def update_project_component(
        self, project_id: str, component_name: str, component
    ) -> UpdateResult:
        """
        Saves a specific component of a project. (e.g. actors, business_scenarios)

        :param str project_id: The id of the project.
        :param str component_name: The name of the component to save.
        :param component: The component to save.
        :return: The result of the mongodb update operation.
        """
        return self.collection.update_one(
            {"_id": ObjectId(project_id)}, {"$set": {component_name: component.dict()}}
        )

    def save_project(self, project: Project) -> InsertOneResult:
        """
        Saves a project to the database.

        :param Project project: The project to save.
        :return: The result of the mongodb insert operation.
        """
        return self.collection.insert_one(project.dict(exclude={"id"}))

    def update_project(self, project_id: str, project: Project) -> UpdateResult:
        """
        Updates a project with the specified id.

        :param str project_id: The id of the project to update.
        :param Project project: The updated project.
        :return: The result of the mongodb update operation.
        """
        return self.collection.update_one(
            {"_id": ObjectId(project_id)}, {"$set": project.dict(exclude={"id"})}
        )

    # TODO: below method should be a transaction.
    def delete_project(self, project_id: str, chat_dao: ChatDAO) -> DeleteResult | None:
        """
        Deletes a project and its associated chats.

        :param str project_id: The id of the project to delete.
        :param ChatDAO chat_dao: The chat DAO to use for deleting chats.
        :return: The result of the mongodb delete operation.
        """
        project = self.get_project(project_id)
        if project is None:
            return None
        chat_id = str(project["chat_id"])
        ai_chat_id = str(project["ai_chat_id"])

        chat_dao.delete_chat(chat_id)
        chat_dao.delete_chat(ai_chat_id)
        return self.collection.delete_one({"_id": ObjectId(project_id)})

    # TODO: below method should be a transaction.
    def create_project(
        self,
        project_name: str,
        owner_id: str,
        description: str,
        for_who: str,
        doing_what: str,
        additional_info: str,
        chat_dao: ChatDAO,
    ) -> str:
        """
        Creates new empty project with the specified details and returns the project id.
        Also creates two chats for the project: discussion_chat and ai_chat.

        :param str project_name: The name of the project.
        :param str owner_id: The id of the owner of the project.
        :param str description: The description of the project.
        :param str for_who: The intended recipient of the application.
        :param str doing_what: The purpose of the application.
        :param str additional_info: Additional information about the application.
        :param ChatDAO chat_dao: The chat DAO to use for creating chats.

        :return: The id of the newly created project.
        :rtype: str
        """

        discussion_chat_id = chat_dao.create_chat()
        ai_chat_id = chat_dao.create_chat()

        new_project = Project(
            name=project_name,
            for_who=for_who,
            doing_what=doing_what,
            additional_info=additional_info,
            description=description,
            owner=ObjectId(owner_id),
            members=[ObjectId(owner_id)],
            managers=[ObjectId(owner_id)],
            created_at=datetime.now(),
            chat_id=ObjectId(discussion_chat_id),
            ai_chat_id=ObjectId(ai_chat_id),
        )

        result = self.save_project(new_project)
        return str(result.inserted_id)

    def is_project_exist(self, project_id: str) -> bool:
        """
        Checks if a project with the specified id exists.

        :param str project_id: The id of the project to check.
        :return: True if the project exists, False otherwise.
        :rtype: bool
        """
        return self.collection.count_documents({"_id": ObjectId(project_id)}) > 0

    def add_member_to_project(self, project_id: str, member_id: str):
        """
        Adds a member to the project.

        :param str project_id: The id of the project.
        :param str member_id: The id of the member to add.
        :return: The result of the mongodb update operation.
        """
        return self.collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$addToSet": {"members": ObjectId(member_id)}},
        )

    def remove_member_from_project(self, project_id: str, member_id: str):
        """
        Removes a member from the project.

        :param str project_id: The id of the project.
        :param str member_id: The id of the member to remove.
        :return: The result of the mongodb update operation.
        """

        return self.collection.update_one(
            {"_id": ObjectId(project_id)}, {"$pull": {"members": ObjectId(member_id)}}
        )

    def unassign_manager_from_project(self, project_id: str, manager_id: str):
        """
        Removes a manager from the project.

        :param str project_id: The id of the project.
        :param str manager_id: The id of the manager to remove.
        :return: The result of the mongodb update operation.
        """
        return self.collection.update_one(
            {"_id": ObjectId(project_id)}, {"$pull": {"managers": ObjectId(manager_id)}}
        )

    def assign_manager_to_project(self, project_id: str, manager_id: str):
        """
        Assigns a manager to the project.

        :param str project_id: The id of the project.
        :param str manager_id: The id of the manager to add.
        :return: The result of the mongodb update operation.
        """
        return self.collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$addToSet": {"managers": ObjectId(manager_id)}},
        )

    def get_project_model_and_basic_information(self, project_id: str):
        """
        Retrieves the project model along with basic project information, excluding certain fields.

        Args:
            project_id (str): The ID of the project to retrieve.
        """
        project = self.collection.find_one(
            {"_id": ObjectId(project_id)},
            {
                "chat_id": 0,
                "ai_chat_id": 0,
                "_id": 0,
                "logo": 0,
                "owner": 0,
                "description": 0,
                "members": 0,
                "managers": 0,
                "created_at": 0,
            },
        )

        if not project:
            return None

        return project
