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



from pydantic import BaseModel, Field, StrictInt, constr, validator

class SimpleChallengeInputDataType(BaseModel):
    """
    A simple challenge input data type.
    """
    id: StrictInt = Field(..., description="The unique identifier of a challenge input data type.")
    slug: constr(strict=True, max_length=30, min_length=3) = Field(..., description="The slug of the challenge input data type.")
    name: constr(strict=True, max_length=50, min_length=3) = Field(..., description="The name of the challenge input data type.")
    __properties = ["id", "slug", "name"]

    @validator('slug')
    def slug_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", value):
            raise ValueError(r"must validate the regular expression /^[a-z0-9]+(?:-[a-z0-9]+)*$/")
        return value

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
    def from_json(cls, json_str: str) -> SimpleChallengeInputDataType:
        """Create an instance of SimpleChallengeInputDataType from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SimpleChallengeInputDataType:
        """Create an instance of SimpleChallengeInputDataType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SimpleChallengeInputDataType.parse_obj(obj)

        _obj = SimpleChallengeInputDataType.parse_obj({
            "id": obj.get("id"),
            "slug": obj.get("slug"),
            "name": obj.get("name")
        })
        return _obj


