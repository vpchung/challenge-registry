import json
import pytest
from tests import NoneType
from api.resolvers.resolver_helpers.paging_utils import from_cursor_hash, to_cursor_hash


@pytest.fixture(scope="module")
def dr_feature():
    return "Module11_Prolif_score"


@pytest.fixture(scope="module")
def dr_mutation():
    return "KANSL1:(OM)"


@pytest.fixture(scope="module")
def mutation_code():
    return "(OM)"


@pytest.fixture(scope="module")
def gene_entrez():
    return 284058


@pytest.fixture(scope="module")
def gene_hgnc():
    return "KANSL1"


@pytest.fixture(scope="module")
def dr_tag_name():
    return "BLCA"


@pytest.fixture(scope="module")
def max_p_value():
    return 0.495103


@pytest.fixture(scope="module")
def max_log10_p_value():
    return 0.197782


@pytest.fixture(scope="module")
def min_fold_change():
    return 1.44142


@pytest.fixture(scope="module")
def min_log10_fold_change():
    return -0.0544383


@pytest.fixture(scope="module")
def min_p_value():
    return 0.634187


@pytest.fixture(scope="module")
def min_log10_p_value():
    return 0.30530497


@pytest.fixture(scope="module")
def min_n_mut():
    return 23


@pytest.fixture(scope="module")
def min_n_wt():
    return 383


@pytest.fixture(scope="module")
def common_query_builder():
    def f(query_fields):
        return (
            """query DriverResults(
        $paging: PagingInput
        $distinct: Boolean
        $dataSet: [String!]
        $related: [String!]
        $entrez: [Int!]
        $feature: [String!]
        $mutation: [String!]
        $mutationCode: [String!]
        $tag: [String!]
        $minPValue: Float
        $maxPValue: Float
        $minLog10PValue: Float
        $maxLog10PValue: Float
        $minFoldChange: Float
        $minLog10FoldChange: Float
        $minNumWildTypes: Int
        $minNumMutants: Int
    ) {
        driverResults(
            paging: $paging
            distinct: $distinct
            dataSet: $dataSet
            related: $related
            feature: $feature
            entrez: $entrez
            mutation: $mutation
            mutationCode: $mutationCode
            tag: $tag
            minPValue: $minPValue
            maxPValue: $maxPValue
            minLog10PValue: $minLog10PValue
            maxLog10PValue: $maxLog10PValue
            minFoldChange: $minFoldChange
            minLog10FoldChange: $minLog10FoldChange
            minNumWildTypes: $minNumWildTypes
            minNumMutants: $minNumMutants
        )"""
            + query_fields
            + "}"
        )

    return f


@pytest.fixture(scope="module")
def paging_query(common_query_builder):
    return common_query_builder(
        """{
            items {
                id
            }
            paging {
                type
                pages
                total
                startCursor
                endCursor
                hasPreviousPage
                hasNextPage
                page
                limit
            }
            error
        }"""
    )


@pytest.fixture(scope="module")
def simple_query(common_query_builder):
    return common_query_builder(
        """{
            items {
                pValue
                log10PValue
                foldChange
                log10FoldChange
                numWildTypes
                numMutants
            }
        }"""
    )


@pytest.fixture(scope="module")
def common_query(common_query_builder):
    return common_query_builder(
        """{
            items {
                pValue
                log10PValue
                foldChange
                log10FoldChange
                numWildTypes
                numMutants
                dataSet { name }
                feature { name }
                mutation {
                    name
                    gene {
                        entrez
                        hgnc
                    }
                    mutationCode
                    mutationType {
                        name
                        display
                    }
                }
                tag { name }
            }
        }"""
    )


def test_driverResults_cursor_pagination_first(client, paging_query):
    num = 10
    response = client.post(
        "/api", json={"query": paging_query, "variables": {"paging": {"first": num}}}
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    items = page["items"]
    paging = page["paging"]
    start = from_cursor_hash(paging["startCursor"])
    end = from_cursor_hash(paging["endCursor"])

    assert len(items) == num
    assert paging["hasNextPage"] == True
    assert paging["hasPreviousPage"] == False
    assert start == items[0]["id"]
    assert end == items[num - 1]["id"]


def test_driverResults_cursor_pagination_last(client, paging_query):
    num = 10
    response = client.post(
        "/api",
        json={
            "query": paging_query,
            "variables": {"paging": {"last": num, "before": to_cursor_hash(1000)}},
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    items = page["items"]
    paging = page["paging"]
    start = from_cursor_hash(paging["startCursor"])
    end = from_cursor_hash(paging["endCursor"])

    assert len(items) == num
    assert paging["hasNextPage"] == False
    assert paging["hasPreviousPage"] == True
    assert start == items[0]["id"]
    assert end == items[num - 1]["id"]


def test_driverResults_cursor_distinct_pagination(client, paging_query):
    page_num = 2
    num = 10
    response = client.post(
        "/api",
        json={
            "query": paging_query,
            "variables": {
                "paging": {
                    "page": page_num,
                    "first": num,
                },
                "distinct": True,
                "dataSet": ["TCGA"],
                "tag": ["C1"],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    items = page["items"]

    assert len(items) == num
    assert page_num == page["paging"]["page"]


def test_driverResults_query_with_no_arguments_no_relations(client, simple_query):
    num = 10
    response = client.post(
        "/api", json={"query": simple_query, "variables": {"paging": {"first": num}}}
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    driver_results = page["items"]
    assert isinstance(driver_results, list)
    assert len(driver_results) == num
    for driver_result in driver_results[0:2]:
        assert type(driver_result["foldChange"]) is float or NoneType
        assert type(driver_result["pValue"]) is float or NoneType
        assert type(driver_result["log10PValue"]) is float or NoneType
        assert type(driver_result["log10FoldChange"]) is float or NoneType
        assert type(driver_result["numWildTypes"]) is int or NoneType
        assert type(driver_result["numMutants"]) is int or NoneType


def test_driverResults_query_with_passed_data_set_entrez_feature_and_tag(
    client, common_query, data_set, dr_feature, gene_entrez, dr_tag_name
):
    num = 1
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "tag": [dr_tag_name],
                "paging": {"first": num},
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) == num
    for result in results[0:2]:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert result["tag"]["name"] == dr_tag_name
        assert type(result["mutation"]["name"]) is str
        assert type(result["mutation"]["gene"]["entrez"]) is int
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert type(result["mutation"]["mutationCode"]) is str


def test_driverResults_query_with_passed_data_set_entrez_feature_and_mutation(
    client, common_query, data_set, dr_feature, gene_entrez, mutation_code
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["mutationCode"] == mutation_code
        assert type(result["tag"]["name"]) is str


def test_driverResults_query_with_passed_data_set_related_entrez_feature_and_mutation(
    client, common_query, data_set, dr_feature, gene_entrez, mutation_code, related
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
                "related": ["does_not_exist"],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) == 0

    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
                "related": [related],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["mutationCode"] == mutation_code
        assert type(result["tag"]["name"]) is str


def test_driverResults_query_with_passed_data_set_entrez_mutation_code_and_tag(
    client, common_query, data_set, gene_entrez, mutation_code, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "mutationCode": [mutation_code],
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["dataSet"]["name"] == data_set
        assert type(result["feature"]["name"]) is str
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["mutationCode"] == mutation_code
        assert result["tag"]["name"] == dr_tag_name


def test_driverResults_query_with_passed_data_set_feature_mutation_code_and_tag(
    client, common_query, data_set, dr_feature, mutation_code, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert type(result["mutation"]["gene"]["entrez"]) is int
        assert result["mutation"]["mutationCode"] == mutation_code
        assert result["tag"]["name"] == dr_tag_name


def test_driverResults_query_with_passed_data_set_feature_mutation_code_entrez_and_tag(
    client,
    common_query,
    data_set,
    dr_feature,
    mutation_code,
    dr_tag_name,
    gene_entrez,
    gene_hgnc,
    dr_mutation,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
                "tag": [dr_tag_name],
                "entrez": [gene_entrez],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) == 1
    for result in results:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert result["tag"]["name"] == dr_tag_name
        assert result["mutation"]["name"] == dr_mutation
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["gene"]["hgnc"] == gene_hgnc
        assert result["mutation"]["mutationCode"] == mutation_code
        assert result["mutation"]["mutationType"]["name"] == "driver_mutation"
        assert result["mutation"]["mutationType"]["display"] == "Driver Mutation"


def test_driverResults_query_with_passed_data_set_feature_tag_and_mutation(
    client,
    common_query,
    data_set,
    dr_feature,
    dr_mutation,
    dr_tag_name,
    gene_entrez,
    gene_hgnc,
    mutation_code,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "feature": [dr_feature],
                "mutation": [dr_mutation],
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) == 1
    for result in results:
        assert result["dataSet"]["name"] == data_set
        assert result["feature"]["name"] == dr_feature
        assert result["mutation"]["name"] == dr_mutation
        assert result["tag"]["name"] == dr_tag_name
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["gene"]["hgnc"] == gene_hgnc
        assert result["mutation"]["mutationCode"] == mutation_code
        assert result["mutation"]["mutationType"]["name"] == "driver_mutation"
        assert result["mutation"]["mutationType"]["display"] == "Driver Mutation"


def test_driverResults_query_with_passed_data_set_entrez_feature_mutation_code_and_tag(
    client, common_query, dr_feature, gene_entrez, mutation_code, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "mutationCode": [mutation_code],
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert type(result["dataSet"]["name"]) is str
        assert result["feature"]["name"] == dr_feature
        assert result["mutation"]["gene"]["entrez"] == gene_entrez
        assert result["mutation"]["mutationCode"] == mutation_code
        assert result["tag"]["name"] == dr_tag_name


def test_driverResults_query_with_passed_min_p_value(
    client, common_query, data_set, gene_entrez, dr_feature, min_p_value, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minPValue": min_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["pValue"] >= min_p_value


def test_driverResults_query_with_passed_min_p_value_and_min_log10_p_value(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    min_log10_p_value,
    min_p_value,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minLog10PValue": min_log10_p_value,
                "minPValue": min_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["pValue"] >= min_p_value


def test_driverResults_query_with_passed_min_log10_p_value(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    min_log10_p_value,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minLog10PValue": min_log10_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["log10PValue"] >= min_log10_p_value


def test_driverResults_query_with_passed_max_p_value(
    client, common_query, data_set, gene_entrez, dr_feature, max_p_value, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "maxPValue": max_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["pValue"] <= max_p_value


def test_driverResults_query_with_passed_max_p_value_and_max_log10_p_value(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    max_log10_p_value,
    max_p_value,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "maxLog10PValue": max_log10_p_value,
                "maxPValue": max_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["pValue"] <= max_p_value


def test_driverResults_query_with_passed_max_log10_p_value(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    max_log10_p_value,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "maxLog10PValue": max_log10_p_value,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["log10PValue"] <= max_log10_p_value


def test_driverResults_query_with_passed_min_fold_change(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    min_fold_change,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minFoldChange": min_fold_change,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["foldChange"] >= min_fold_change


def test_driverResults_query_with_passed_min_fold_change_and_min_log10_fold_change(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    min_log10_fold_change,
    min_fold_change,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "maxLog10FoldChange": min_log10_fold_change,
                "minFoldChange": min_fold_change,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["foldChange"] >= min_fold_change


def test_driverResults_query_with_passed_min_log10_fold_change(
    client,
    common_query,
    data_set,
    gene_entrez,
    dr_feature,
    min_log10_fold_change,
    dr_tag_name,
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minLog10FoldChange": min_log10_fold_change,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["log10FoldChange"] >= min_log10_fold_change


def test_driverResults_query_with_passed_min_n_mut(
    client, common_query, data_set, gene_entrez, dr_feature, min_n_mut, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minNumMutants": min_n_mut,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["numMutants"] >= min_n_mut


def test_driverResults_query_with_passed_min_n_wt(
    client, common_query, data_set, gene_entrez, dr_feature, min_n_wt, dr_tag_name
):
    response = client.post(
        "/api",
        json={
            "query": common_query,
            "variables": {
                "dataSet": [data_set],
                "entrez": [gene_entrez],
                "feature": [dr_feature],
                "minNumWildTypes": min_n_wt,
                "tag": [dr_tag_name],
            },
        },
    )
    json_data = json.loads(response.data)
    page = json_data["data"]["driverResults"]
    results = page["items"]
    assert isinstance(results, list)
    assert len(results) > 0
    for result in results[0:2]:
        assert result["numWildTypes"] >= min_n_wt
