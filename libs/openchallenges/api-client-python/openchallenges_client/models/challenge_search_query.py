# coding: utf-8

"""
    OpenChallenges REST API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import date
from typing import List, Optional
from pydantic import (
    BaseModel,
    Field,
    StrictInt,
    StrictStr,
    conint,
    conlist,
    constr,
    validator,
)
from openchallenges_client.models.challenge_category import ChallengeCategory
from openchallenges_client.models.challenge_difficulty import ChallengeDifficulty
from openchallenges_client.models.challenge_direction import ChallengeDirection
from openchallenges_client.models.challenge_incentive import ChallengeIncentive
from openchallenges_client.models.challenge_sort import ChallengeSort
from openchallenges_client.models.challenge_status import ChallengeStatus
from openchallenges_client.models.challenge_submission_type import (
    ChallengeSubmissionType,
)


class ChallengeSearchQuery(BaseModel):
    """
    A challenge search query.
    """

    page_number: Optional[conint(strict=True, ge=0)] = Field(
        0, alias="pageNumber", description="The page number."
    )
    page_size: Optional[conint(strict=True, ge=1)] = Field(
        100, alias="pageSize", description="The number of items in a single page."
    )
    sort: Optional[ChallengeSort] = None
    sort_seed: Optional[conint(strict=True, le=2147483647, ge=0)] = Field(
        None,
        alias="sortSeed",
        description="The seed that initializes the random sorter.",
    )
    direction: Optional[ChallengeDirection] = None
    difficulties: Optional[conlist(ChallengeDifficulty)] = Field(
        None,
        description="An array of challenge difficulty levels used to filter the results.",
    )
    incentives: Optional[conlist(ChallengeIncentive)] = Field(
        None,
        description="An array of challenge incentive types used to filter the results.",
    )
    min_start_date: Optional[date] = Field(
        None,
        alias="minStartDate",
        description="Keep the challenges that start at this date or later.",
    )
    max_start_date: Optional[date] = Field(
        None,
        alias="maxStartDate",
        description="Keep the challenges that start at this date or sooner.",
    )
    platforms: Optional[conlist(constr(strict=True, max_length=30, min_length=3))] = (
        Field(
            None,
            description="An array of challenge platform ids used to filter the results.",
        )
    )
    organizations: Optional[conlist(StrictInt)] = Field(
        None, description="An array of organization ids used to filter the results."
    )
    input_data_types: Optional[
        conlist(constr(strict=True, max_length=30, min_length=3))
    ] = Field(
        None,
        alias="inputDataTypes",
        description="An array of challenge input data type ids used to filter the results.",
    )
    status: Optional[conlist(ChallengeStatus)] = Field(
        None, description="An array of challenge status used to filter the results."
    )
    submission_types: Optional[conlist(ChallengeSubmissionType)] = Field(
        None,
        alias="submissionTypes",
        description="An array of challenge submission types used to filter the results.",
    )
    categories: Optional[conlist(ChallengeCategory)] = Field(
        None,
        description="The array of challenge categories used to filter the results.",
    )
    search_terms: Optional[StrictStr] = Field(
        None,
        alias="searchTerms",
        description="A string of search terms used to filter the results.",
    )
    __properties = [
        "pageNumber",
        "pageSize",
        "sort",
        "sortSeed",
        "direction",
        "difficulties",
        "incentives",
        "minStartDate",
        "maxStartDate",
        "platforms",
        "organizations",
        "inputDataTypes",
        "status",
        "submissionTypes",
        "categories",
        "searchTerms",
    ]

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ChallengeSearchQuery:
        """Create an instance of ChallengeSearchQuery from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # set to None if sort_seed (nullable) is None
        # and __fields_set__ contains the field
        if self.sort_seed is None and "sort_seed" in self.__fields_set__:
            _dict["sortSeed"] = None

        # set to None if direction (nullable) is None
        # and __fields_set__ contains the field
        if self.direction is None and "direction" in self.__fields_set__:
            _dict["direction"] = None

        # set to None if min_start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.min_start_date is None and "min_start_date" in self.__fields_set__:
            _dict["minStartDate"] = None

        # set to None if max_start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.max_start_date is None and "max_start_date" in self.__fields_set__:
            _dict["maxStartDate"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ChallengeSearchQuery:
        """Create an instance of ChallengeSearchQuery from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ChallengeSearchQuery.parse_obj(obj)

        _obj = ChallengeSearchQuery.parse_obj(
            {
                "page_number": (
                    obj.get("pageNumber") if obj.get("pageNumber") is not None else 0
                ),
                "page_size": (
                    obj.get("pageSize") if obj.get("pageSize") is not None else 100
                ),
                "sort": obj.get("sort"),
                "sort_seed": obj.get("sortSeed"),
                "direction": obj.get("direction"),
                "difficulties": obj.get("difficulties"),
                "incentives": obj.get("incentives"),
                "min_start_date": obj.get("minStartDate"),
                "max_start_date": obj.get("maxStartDate"),
                "platforms": obj.get("platforms"),
                "organizations": obj.get("organizations"),
                "input_data_types": obj.get("inputDataTypes"),
                "status": obj.get("status"),
                "submission_types": obj.get("submissionTypes"),
                "categories": obj.get("categories"),
                "search_terms": obj.get("searchTerms"),
            }
        )
        return _obj
