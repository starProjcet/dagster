from dagster.api.snapshot_schedule import sync_get_external_schedule_execution_data_ephemeral_grpc
from dagster.core.host_representation.external_data import ExternalScheduleExecutionData
from dagster.core.test_utils import instance_for_test
from dagster.seven import get_current_datetime_in_utc

from .utils import get_bar_repo_handle


def test_external_schedule_execution_data_api_grpc():
    with instance_for_test() as instance:
        with get_bar_repo_handle() as repository_handle:
            execution_data = sync_get_external_schedule_execution_data_ephemeral_grpc(
                instance, repository_handle, "foo_schedule", None,
            )
            assert isinstance(execution_data, ExternalScheduleExecutionData)
            assert execution_data.run_config == {"fizz": "buzz"}
            assert execution_data.tags == {"dagster/schedule_name": "foo_schedule"}
            assert execution_data.should_execute == True


def test_external_schedule_execution_data_api_never_execute_grpc():
    with instance_for_test() as instance:
        with get_bar_repo_handle() as repository_handle:
            execution_data = sync_get_external_schedule_execution_data_ephemeral_grpc(
                instance, repository_handle, "foo_schedule_never_execute", None,
            )
            assert isinstance(execution_data, ExternalScheduleExecutionData)
            assert execution_data.run_config == {}
            assert execution_data.tags == {}
            assert execution_data.should_execute == False


def test_include_execution_time_grpc():
    with instance_for_test() as instance:
        with get_bar_repo_handle() as repository_handle:
            execution_time = get_current_datetime_in_utc()
            execution_data = sync_get_external_schedule_execution_data_ephemeral_grpc(
                instance, repository_handle, "foo_schedule_echo_time", execution_time,
            )

            assert isinstance(execution_data, ExternalScheduleExecutionData)
            assert execution_data.run_config == {"passed_in_time": execution_time.isoformat()}
            assert execution_data.tags == {"dagster/schedule_name": "foo_schedule_echo_time"}
            assert execution_data.should_execute == True
