from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

import cartography.intel.entra.groups
from cartography.intel.entra.groups import sync_entra_groups
from cartography.intel.entra.users import load_users
from cartography.intel.entra.users import transform_users
from tests.data.entra.groups import MOCK_ENTRA_GROUPS
from tests.data.entra.groups import MOCK_GROUP_MEMBERS
from tests.data.entra.groups import TEST_CLIENT_ID
from tests.data.entra.groups import TEST_CLIENT_SECRET
from tests.data.entra.groups import TEST_TENANT_ID
from tests.data.entra.users import MOCK_ENTRA_USERS
from tests.integration.util import check_nodes
from tests.integration.util import check_rels

TEST_UPDATE_TAG = 1234567890


def mock_get_group_members_side_effect(
    client, group_id: str
) -> tuple[list[str], list[str]]:
    """
    Mock side effect function to return member user IDs and subgroup IDs for a given group.
    """
    members = MOCK_GROUP_MEMBERS[group_id]
    user_ids = [o.id for o in members if o.odata_type == "#microsoft.graph.user"]
    group_ids = [o.id for o in members if o.odata_type == "#microsoft.graph.group"]
    return user_ids, group_ids


@patch.object(
    cartography.intel.entra.groups,
    "get_entra_groups",
    new_callable=AsyncMock,
    return_value=MOCK_ENTRA_GROUPS,
)
@patch.object(
    cartography.intel.entra.groups,
    "get_group_members",
    new_callable=AsyncMock,
    side_effect=mock_get_group_members_side_effect,
)
@pytest.mark.asyncio
async def test_sync_entra_groups(mock_get_members, mock_get_groups, neo4j_session):
    """Ensure groups and relationships load"""
    # Load users first for membership relationships
    load_users(
        neo4j_session,
        transform_users(MOCK_ENTRA_USERS),
        TEST_TENANT_ID,
        TEST_UPDATE_TAG,
    )

    await sync_entra_groups(
        neo4j_session,
        TEST_TENANT_ID,
        TEST_CLIENT_ID,
        TEST_CLIENT_SECRET,
        TEST_UPDATE_TAG,
        {"UPDATE_TAG": TEST_UPDATE_TAG, "TENANT_ID": TEST_TENANT_ID},
    )

    expected_nodes = {
        ("11111111-1111-1111-1111-111111111111", "Security Team"),
        ("22222222-2222-2222-2222-222222222222", "Developers"),
    }
    assert (
        check_nodes(neo4j_session, "EntraGroup", ["id", "display_name"])
        == expected_nodes
    )

    expected_rels = {
        ("11111111-1111-1111-1111-111111111111", TEST_TENANT_ID),
        ("22222222-2222-2222-2222-222222222222", TEST_TENANT_ID),
    }
    assert (
        check_rels(
            neo4j_session,
            "EntraGroup",
            "id",
            "EntraTenant",
            "id",
            "RESOURCE",
            rel_direction_right=False,
        )
        == expected_rels
    )

    expected_membership = {
        (
            "ae4ac864-4433-4ba6-96a6-20f8cffdadcb",
            "11111111-1111-1111-1111-111111111111",
        ),
        (
            "11dca63b-cb03-4e53-bb75-fa8060285550",
            "11111111-1111-1111-1111-111111111111",
        ),
    }
    assert (
        check_rels(
            neo4j_session,
            "EntraUser",
            "id",
            "EntraGroup",
            "id",
            "MEMBER_OF",
        )
        == expected_membership
    )

    expected_group_membership = {
        ("11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222")
    }
    assert (
        check_rels(
            neo4j_session,
            "EntraGroup",
            "id",
            "EntraGroup",
            "id",
            "MEMBER_OF",
            rel_direction_right=False,
        )
        == expected_group_membership
    )
