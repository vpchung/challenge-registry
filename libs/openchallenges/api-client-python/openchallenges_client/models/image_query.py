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


from typing import Optional
from pydantic import BaseModel, Field, constr, validator
from openchallenges_client.models.image_aspect_ratio import ImageAspectRatio
from openchallenges_client.models.image_height import ImageHeight


class ImageQuery(BaseModel):
    """
    An image query.
    """

    object_key: constr(strict=True) = Field(
        ..., alias="objectKey", description="The unique identifier of the image."
    )
    height: Optional[ImageHeight] = None
    aspect_ratio: Optional[ImageAspectRatio] = Field(None, alias="aspectRatio")
    __properties = ["objectKey", "height", "aspectRatio"]

    @validator("object_key")
    def object_key_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-zA-Z0-9\/_-]+.[a-zA-Z0-9\/_-]+", value):
            raise ValueError(
                r"must validate the regular expression /^[a-zA-Z0-9\/_-]+.[a-zA-Z0-9\/_-]+/"
            )
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
    def from_json(cls, json_str: str) -> ImageQuery:
        """Create an instance of ImageQuery from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ImageQuery:
        """Create an instance of ImageQuery from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ImageQuery.parse_obj(obj)

        _obj = ImageQuery.parse_obj(
            {
                "object_key": obj.get("objectKey"),
                "height": obj.get("height"),
                "aspect_ratio": obj.get("aspectRatio"),
            }
        )
        return _obj
