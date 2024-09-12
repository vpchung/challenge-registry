# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from schematic_api.models.base_model_ import Model
from schematic_api.models.dataset_metadata import DatasetMetadata
from schematic_api import util

from schematic_api.models.dataset_metadata import DatasetMetadata  # noqa: E501


class DatasetMetadataPageAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, datasets=None):  # noqa: E501
        """DatasetMetadataPageAllOf - a model defined in OpenAPI

        :param datasets: The datasets of this DatasetMetadataPageAllOf.  # noqa: E501
        :type datasets: List[DatasetMetadata]
        """
        self.openapi_types = {"datasets": List[DatasetMetadata]}

        self.attribute_map = {"datasets": "datasets"}

        self._datasets = datasets

    @classmethod
    def from_dict(cls, dikt) -> "DatasetMetadataPageAllOf":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DatasetMetadataPage_allOf of this DatasetMetadataPageAllOf.  # noqa: E501
        :rtype: DatasetMetadataPageAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def datasets(self):
        """Gets the datasets of this DatasetMetadataPageAllOf.

        An array of dataset meatdata.  # noqa: E501

        :return: The datasets of this DatasetMetadataPageAllOf.
        :rtype: List[DatasetMetadata]
        """
        return self._datasets

    @datasets.setter
    def datasets(self, datasets):
        """Sets the datasets of this DatasetMetadataPageAllOf.

        An array of dataset meatdata.  # noqa: E501

        :param datasets: The datasets of this DatasetMetadataPageAllOf.
        :type datasets: List[DatasetMetadata]
        """
        if datasets is None:
            raise ValueError(
                "Invalid value for `datasets`, must not be `None`"
            )  # noqa: E501

        self._datasets = datasets
