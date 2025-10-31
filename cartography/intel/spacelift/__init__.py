import logging

import neo4j
import requests

from cartography.config import Config
from cartography.intel.spacelift.account import sync_account
from cartography.intel.spacelift.runs import sync_runs
from cartography.intel.spacelift.spaces import sync_spaces
from cartography.intel.spacelift.stacks import sync_stacks
from cartography.intel.spacelift.workerpools import sync_worker_pools
from cartography.intel.spacelift.workers import sync_workers
from cartography.stats import get_stats_client
from cartography.util import merge_module_sync_metadata
from cartography.util import timeit

logger = logging.getLogger(__name__)
stat_handler = get_stats_client(__name__)


@timeit
def start_spacelift_ingestion(neo4j_session: neo4j.Session, config: Config) -> None:
    """
    Perform ingestion of Spacelift data.
    :param neo4j_session: Neo4j session for database interface
    :param config: A cartography.config object
    :return: None
    """
    if not config.spacelift_api_token or not config.spacelift_api_endpoint:
        logger.info("Spacelift API configuration not found - skipping this module.")
        return

    logger.info("Starting Spacelift ingestion")

    # Set up common job parameters
    common_job_parameters = {
        "UPDATE_TAG": config.update_tag,
    }

    # Create authenticated session for Spacelift API
    spacelift_session = requests.Session()
    spacelift_session.headers.update(
        {
            "Authorization": f"Bearer {config.spacelift_api_token}",
        }
    )

    account_id = sync_account(
        neo4j_session,
        config.spacelift_api_endpoint,
        common_job_parameters,
    )

    common_job_parameters["SPACELIFT_ACCOUNT_ID"] = account_id
    common_job_parameters["account_id"] = account_id

    sync_spaces(
        neo4j_session,
        spacelift_session,
        config.spacelift_api_endpoint,
        account_id,
        common_job_parameters,
    )

    sync_stacks(
        neo4j_session,
        spacelift_session,
        config.spacelift_api_endpoint,
        account_id,
        common_job_parameters,
    )

    sync_worker_pools(
        neo4j_session,
        spacelift_session,
        config.spacelift_api_endpoint,
        account_id,
        common_job_parameters,
    )

    sync_workers(
        neo4j_session,
        spacelift_session,
        config.spacelift_api_endpoint,
        account_id,
        common_job_parameters,
    )

    # Note: Users are synced as part of runs sync (derived from run.triggeredBy)
    sync_runs(
        neo4j_session,
        spacelift_session,
        config.spacelift_api_endpoint,
        account_id,
        common_job_parameters,
    )

    merge_module_sync_metadata(
        neo4j_session,
        group_type="Spacelift",
        group_id=account_id,
        synced_type="SpaceliftData",
        update_tag=config.update_tag,
        stat_handler=stat_handler,
    )

    logger.info("Completed Spacelift ingestion")
