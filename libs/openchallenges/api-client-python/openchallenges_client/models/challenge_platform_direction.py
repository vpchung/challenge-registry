# coding: utf-8

"""
    OpenChallenges REST API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg


class ChallengePlatformDirection(str, Enum):
    """
    The direction to sort the results by.
    """

    """
    allowed enum values
    """
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def from_json(cls, json_str: str) -> ChallengePlatformDirection:
        """Create an instance of ChallengePlatformDirection from a JSON string"""
        return ChallengePlatformDirection(json.loads(json_str))
