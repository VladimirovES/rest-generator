from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from rest_client.client import ApiClient
from .models import IssuesForReportFilterSchema, SearchIssuesByField


class Local:

    def __init__(self, client: ApiClient):
        self._client = client

    def list_issues_for_report(
        self,
        project_oid: str,
        domain: str,
        payload: IssuesForReportFilterSchema,
        paginated: Optional[bool] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Получение замечаний для отчёта
        """
        with allure.step(
            "List Issues For Report (POST /local/projects/{project_oid}/issues_for_report)"
        ):
            path = f"/local/projects/{project_oid}/issues_for_report"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "domain": domain,
                    "paginated": paginated,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def list_issues_filter_data(
        self,
        project_oid: str,
        domain: str,
        payload: SearchIssuesByField,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:
        """
        Получение вариантов фильтрации замечания по его полям
        """
        with allure.step(
            "List Issues Filter Data (POST /local/projects/{project_oid}/filter_issues_by_field)"
        ):
            path = f"/local/projects/{project_oid}/filter_issues_by_field"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "domain": domain,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return [item for item in r_json] if expected_status == HTTPStatus.OK else r_json
