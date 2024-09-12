# coding: utf-8

"""
    OpenChallenges REST API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

import openchallenges_client
from openchallenges_client.models.challenge import Challenge  # noqa: E501
from openchallenges_client.rest import ApiException


class TestChallenge(unittest.TestCase):
    """Challenge unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Challenge
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `Challenge`
        """
        model = openchallenges_client.models.challenge.Challenge()  # noqa: E501
        if include_optional :
            return Challenge(
                id = 1, 
                slug = 'awesome-challenge', 
                name = '012', 
                headline = 'Example challenge headline', 
                description = 'This is an example description of the challenge.', 
                doi = '', 
                status = 'active', 
                difficulty = 'intermediate', 
                platform = openchallenges_client.models.simple_challenge_platform.SimpleChallengePlatform(
                    id = 1, 
                    slug = 'example-challenge-platform', 
                    name = '012', ), 
                website_url = '', 
                avatar_url = '', 
                incentives = [
                    'publication'
                    ], 
                submission_types = [
                    'container_image'
                    ], 
                input_data_types = [
                    openchallenges_client.models.simple_challenge_input_data_type.SimpleChallengeInputDataType(
                        id = 1, 
                        slug = 'gene-expression', 
                        name = 'gene expression', )
                    ], 
                start_date = 'Fri Jul 21 00:00:00 UTC 2017', 
                end_date = 'Fri Jul 21 00:00:00 UTC 2017', 
                starred_count = 56, 
                created_at = '2022-07-04T22:19:11Z', 
                updated_at = '2022-07-04T22:19:11Z'
            )
        else :
            return Challenge(
                id = 1,
                slug = 'awesome-challenge',
                name = '012',
                description = 'This is an example description of the challenge.',
                status = 'active',
                difficulty = 'intermediate',
                platform = openchallenges_client.models.simple_challenge_platform.SimpleChallengePlatform(
                    id = 1, 
                    slug = 'example-challenge-platform', 
                    name = '012', ),
                incentives = [
                    'publication'
                    ],
                submission_types = [
                    'container_image'
                    ],
                starred_count = 56,
                created_at = '2022-07-04T22:19:11Z',
                updated_at = '2022-07-04T22:19:11Z',
        )
        """

    def testChallenge(self):
        """Test Challenge"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
