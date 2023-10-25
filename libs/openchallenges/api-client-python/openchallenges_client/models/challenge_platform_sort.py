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





class ChallengePlatformSort(str, Enum):
    """
    What to sort results by.
    """

    """
    allowed enum values
    """
    NAME = 'name'
    RELEVANCE = 'relevance'

    @classmethod
    def from_json(cls, json_str: str) -> ChallengePlatformSort:
        """Create an instance of ChallengePlatformSort from a JSON string"""
        return ChallengePlatformSort(json.loads(json_str))


