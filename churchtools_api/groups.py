"""module containing parts used for groups handling."""

import json
import logging

import requests

from churchtools_api.churchtools_api_abstract import ChurchToolsApiAbstract

logger = logging.getLogger(__name__)


class ChurchToolsApiGroups(ChurchToolsApiAbstract):
    """Part definition of ChurchToolsApi which focuses on groups.

    Args:
        ChurchToolsApiAbstract: template with minimum references
    """

    def __init__(self) -> None:
        """Inherited initialization."""
        super()

    def get_groups(self, **kwargs: dict) -> list[dict]:
        """Gets list of all groups.

        Keywords:
            group_id: int: optional filter by group id (only to be used on it's own)
            kwargs: keyword arguments passthrough e.g. query

        Keywords:
            group_id

        Permissions:
            requires "view group" for all groups which should be considered

        Returns:
            list of groups - either all or filtered by keyword

        """
        url = self.domain + "/api/groups"
        params = {}
        if "group_id" in kwargs:
            url = url + "/{}".format(kwargs["group_id"])
        else:
            params = {**kwargs}

        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            return [response_data] if isinstance(response_data, dict) else response_data
        logger.warning(
            "%s Something went wrong fetching groups: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_groups_hierarchies(self) -> dict:
        """Get list of all group hierarchies and convert them to a dict.

        Returns:
            list of all group hierarchies using groupId as key
        """
        url = self.domain + "/api/groups/hierarchies"
        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers)
        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Groups Hierarchies successful len=%s",
                len(response_content),
            )

            return {group["groupId"]: group for group in response_data}

        logger.warning(
            "%s Something went wrong fetching groups hierarchies: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_group_statistics(self, group_id: int) -> dict:
        """Get statistics for the given group.

        Args:
            group_id: required group_id

        Returns:
            statistics
        """
        url = self.domain + f"/api/groups/{group_id}/statistics"
        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            logger.debug(
                "First response of Group Statistics successful len=%s",
                len(response_content),
            )
            return response_data
        logger.warning(
            "%s Something went wrong fetching group statistics: %s",
            response.status_code,
            response.content,
        )
        return None

    def create_group(
        self,
        name: str,
        group_status_id: int,
        grouptype_id: int,
        **kwargs: dict,
    ) -> dict:
        """Create a new group.

        Args:
            name: required name
            group_status_id: required status id
            grouptype_id: required grouptype id
            kwargs: keywords see below

        Kwargs:
            campus_id: int: optional campus id
            superior_group_id: int: optional superior group id
            force: bool: set to force create if a group with this name already exists

        Required Permissions:
            administer groups
            create group of grouptype

        Returns:
            dict with created group group - similar to get_group
        """
        url = self.domain + "/api/groups"
        headers = {"accept": "application/json"}
        data = {
            "groupStatusId": group_status_id,
            "groupTypeId": grouptype_id,
            "name": name,
        }

        if "campus_id" in kwargs:
            data["campusId"] = kwargs["campus_id"]

        if "force" in kwargs:
            data["force"] = kwargs["force"]

        if "superior_group_id" in kwargs:
            data["superiorGroupId"] = kwargs["superior_group_id"]

        response = self.session.post(url=url, headers=headers, data=data)

        if response.status_code != requests.codes.created:
            logger.warning(json.loads(response.content)["translatedMessage"])
            return None

        response_content = json.loads(response.content)
        response_data = self.combine_paginated_response_data(
            response_content,
            url=url,
            headers=headers,
        )
        logger.debug(
            "First response of Create Group successful len=%s",
            len(response_content),
        )

        return response_data

    def update_group(self, group_id: int, data: dict) -> dict:
        """Update a field of the given group.

        to loookup available names use get_group(group_id=xxx).

        Arguments:
            group_id: number of the group to update
            data: all group fields

        Returns:
            dict with updated group
        """
        url = self.domain + f"/api/groups/{group_id}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = self.session.patch(url=url, headers=headers, data=json.dumps(data))

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Update Group successful len=%s",
                len(response_content),
            )

            return response_data
        logger.warning(
            "%s Something went wrong updating group: %s",
            response.status_code,
            response.content,
        )
        return None
    
    def update_group_member(self, group_id: int, member_id: int, data: dict) -> dict:
        """Update a field of the given member in group.

        to loookup available names use get_group_member(group_id=xxx).

        Arguments:
            group_id: number of the group to update
            member_id: number of the member to update
            data: all group member fields

        Returns:
            dict with updated group member
        """
        url = self.domain + f"/api/groups/{group_id}/members/{member_id}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = self.session.patch(url=url, headers=headers, data=json.dumps(data))

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Update Group Member successful len=%s",
                len(response_content),
            )

            return response_data
        logger.warning(
            "%s Something went wrong updating group: %s",
            response.status_code,
            response.content,
        )
        return None

    def update_group_member(self, group_id: int, person_id: int, data: dict) -> dict:
        """Update a field of the given member in group.

        to loookup available names use get_group_member(group_id=xxx).

        Arguments:
            group_id: number of the group to update
            person_id: number of the member to update
            data: all group member fields

        Returns:
            dict with updated group member
        """
        url = self.domain + f"/api/groups/{group_id}/members/{person_id}"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        response = self.session.patch(url=url, headers=headers, json=data)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Update Group Member successful len=%s",
                len(response_content),
            )

            return response_data
        logger.warning(
            "%s Something went wrong updating group: %s",
            response.status_code,
            response.content,
        )
        return None

    def delete_group(self, group_id: int) -> bool:
        """Delete the given group.

        Arguments:
            group_id: group_id

        Required Permissions
            delete group

        Returns:
            True if successful
        """
        url = self.domain + f"/api/groups/{group_id}"
        response = self.session.delete(url=url)

        if response.status_code == requests.codes.no_content:
            logger.debug("First response of Delete Group successful")
            return True
        logger.warning(
            "%s Something went wrong deleting group: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_grouptypes(self, **kwargs: dict) -> dict:
        """Get list of all grouptypes.

        Arguments:
            kwargs: keyword arguments as listed below

        Keywords:
            grouptype_id: int: optional filter by grouptype id
            dict with all grouptypes with id as key (even if only one)
        """
        url = self.domain + "/api/group/grouptypes"
        if "grouptype_id" in kwargs:
            url = url + "/{}".format(kwargs["grouptype_id"])
        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Grouptypes successful len=%s",
                len(response_content),
            )
            if isinstance(response_data, list):
                result = {group["id"]: group for group in response_data}
            else:
                result = {response_data["id"]: response_data}
            return result
        logger.warning(
            "%s Something went wrong fetching grouptypes: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_group_permissions(self, group_id: int) -> dict:
        """Get permissions of the current user for the given group.

        Arguments:
            group_id: required group_id
        Returns:
            dict with permissions
        """
        url = self.domain + f"/api/permissions/internal/groups/{group_id}"
        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            response_data = response_content["data"].copy()
            logger.debug(
                "First response of Group Permissions successful len=%s",
                len(response_content),
            )
            return response_data
        logger.warning(
            "%s Something went wrong fetching group permissions: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_group_members(self, group_id: int, **kwargs: dict) -> list[dict]:
        """Get list of members for the given group.

        Arguments:
            group_id: group id
            kwargs: see API documentation - only tested cases below

        Kwargs:
            role_ids: list[int]: optional filter list of role ids
            person_ids: list[int]: optional filter by person_id

        Returns:
            list of group member dicts
        """
        url = self.domain + f"/api/groups/{group_id}/members"
        headers = {"accept": "application/json"}
        params = {}

        if "role_ids" in kwargs:
            params["role_ids[]"] = kwargs["role_ids"]
        if "person_ids" in kwargs:
            params["person_id[]"] = kwargs["person_ids"]

        response = self.session.get(url=url, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            return [response_data] if isinstance(response_data, dict) else response_data

        logger.warning(
            "%s Something went wrong fetching group members: %s",
            response.status_code,
            response.content,
        )
        return None
    
    def get_group_memberfields(self, group_id: int) -> list[dict]:
        """Get list of member fields for the given group.

        Arguments:
            group_id: group id

        Returns:
            list of group member fields dicts
        """
        url = self.domain + f"/api/groups/{group_id}/memberfields"
        headers = {"accept": "application/json"}
        params = {}

        response = self.session.get(url=url, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            return [response_data] if isinstance(response_data, dict) else response_data

        logger.warning(
            "%s Something went wrong fetching group member fields: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_group_memberfields(self, group_id: int) -> list[dict]:
        """Get list of member fields for the given group.

        Arguments:
            group_id: group id

        Returns:
            list of dicts with {"type":"group","field":dict} that shows member fields
        """
        url = self.domain + f"/api/groups/{group_id}/memberfields"
        headers = {"accept": "application/json"}
        params = {}

        response = self.session.get(url=url, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            return [response_data] if isinstance(response_data, dict) else response_data

        logger.warning(
            "%s Something went wrong fetching group member fields: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_groups_members(
        self,
        group_ids: list[int] | None = None,
        *,
        with_deleted: bool = False,
        **kwargs: dict,
    ) -> list[dict]:
        """Access to /groups/members to lookup group memberships.

        Similar to get_group_members but not specific to a single group.

        Args:
            group_ids: list of group ids to look for. Defaults to Any
            with_deleted: If true return also delted group members. Defaults to True
            kwargs: see below

        Keywords:
            grouptype_role_ids: list[int] of grouptype_role_ids to consider
            person_ids: list[int]: person to consider for result

        Permissions:
            requires "administer persons"

        Returns:
            list of person to group assignments
        """
        url = self.domain + "/api/groups/members"
        headers = {"accept": "application/json"}
        params = {"ids[]": group_ids, with_deleted: with_deleted}

        response = self.session.get(url=url, headers=headers, params=params)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
                params=params,
            )
            result_list = (
                [response_data] if isinstance(response_data, dict) else response_data
            )
            if grouptype_role_ids := kwargs.get("grouptype_role_ids"):
                result_list = [
                    group
                    for group in result_list
                    if group["groupTypeRoleId"] in grouptype_role_ids
                ]
            if person_ids := kwargs.get("person_ids"):
                result_list = [
                    group for group in result_list if group["personId"] in person_ids
                ]

            return result_list

            return result_list
        logger.warning(
            "%s Something went wrong fetching group members: %s",
            response.status_code,
            response.content,
        )
        return None

    def add_group_member(self, group_id: int, person_id: int, **kwargs: dict) -> dict:
        """Add a member to a group.

        Arguments:
            group_id: required group id
            person_id: required person id
            kwargs: implemented see below

        Keywords:
            grouptype_role_id: int: optional grouptype role id
            group_member_status: str: optional member status
            fields: dict: {"fieldname":"value" ...} to define groupmemberfields

        Returns:
            dict with group member
        """
        url = self.domain + f"/api/groups/{group_id}/members/{person_id}"
        headers = {
            "accept": "application/json",
        }

        data = {}
        if "grouptype_role_id" in kwargs:
            data["groupTypeRoleId"] = kwargs["grouptype_role_id"]
        if "group_member_status" in kwargs:
            data["group_member_status"] = kwargs["group_member_status"]
        if "fields" in kwargs:
            data["fields"] = kwargs["fields"]

        response = self.session.put(url=url, json=data, headers=headers)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)
            # For unknown reasons the endpoint returns a list of items instead
            # of a single item as specified in the API documentation.
            return response_content["data"][0].copy()

        logger.warning(
            "%s Something went wrong adding group member: %s",
            response.status_code,
            response.content,
        )
        return None

    def remove_group_member(self, group_id: int, person_id: int) -> bool:
        """Remove the given group member.

        Arguments:
            group_id: int: required group id
            person_id: int: required person id

        Required Permissions:
            edit group memberships of groups
        Returns:
            True if successful
        """
        url = self.domain + f"/api/groups/{group_id}/members/{person_id}"
        response = self.session.delete(url=url)

        if response.status_code == requests.codes.no_content:
            return True
        logger.warning(
            "%s Something went wrong removing group member: %s",
            response.status_code,
            response.content,
        )
        return None

    def get_group_roles(self, group_id: int) -> list[dict]:
        """Get list of all roles for the given group.

        Arguments:
            group_id: int: required group id
        Returns:
            list with group roles dicts
        """
        url = self.domain + f"/api/groups/{group_id}/roles"
        headers = {"accept": "application/json"}
        response = self.session.get(url=url, headers=headers)

        if response.status_code == requests.codes.ok:
            response_content = json.loads(response.content)

            response_data = self.combine_paginated_response_data(
                response_content,
                url=url,
                headers=headers,
            )
            return [response_data] if isinstance(response_data, dict) else response_data
        logger.warning(
            "%s Something went wrong fetching group roles: %s",
            response.status_code,
            response.content,
        )
        return None

    def add_parent_group(self, group_id: int, parent_group_id: int) -> bool:
        """Add a parent group for a group.

        Arguments:
            group_id: required group id
            parent_group_id: required parent group id

        Required Permissions:
            administer groups

        Returns:
        True if successful
        """
        url = self.domain + f"/api/groups/{group_id}/parents/{parent_group_id}"
        response = self.session.put(url=url)

        if response.status_code == requests.codes.created:
            logger.debug("First response of Add Parent Group successful")
            return True
        logger.warning(
            "%s Something went wrong adding parent group: %s",
            response.status_code,
            response.content,
        )
        return None

    def remove_parent_group(self, group_id: int, parent_group_id: int) -> bool:
        """Remove a parent group from a group.

        Arguments:
            group_id: required group id
            parent_group_id: required parent group id

        Returns:
        True if successful
        """
        url = self.domain + f"/api/groups/{group_id}/parents/{parent_group_id}"
        response = self.session.delete(url=url)

        if response.status_code == requests.codes.no_content:
            logger.debug("First response of Remove Parent Group successful")
            return True
        logger.warning(
            "%s Something went wrong removing parent group: %s",
            response.status_code,
            response.content,
        )
        return None
