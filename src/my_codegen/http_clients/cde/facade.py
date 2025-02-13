from typing import Optional

from endpoints.accesssetting_client import AccessSetting
from endpoints.approvalprocesses_client import ApprovalProcesses
from endpoints.approvalprocesstemplates_client import ApprovalProcessTemplates
from endpoints.entities_client import Entities
from endpoints.folders_client import Folders
from endpoints.issues_client import Issues
from endpoints.permissions_client import Permissions
from endpoints.rolegroups_client import RoleGroups
from endpoints.users_client import Users


class CdeApi:
    def __init__(self, auth_token: Optional[str] = None):
        self.accesssetting = AccessSetting(auth_token)
        self.approvalprocesses = ApprovalProcesses(auth_token)
        self.approvalprocesstemplates = ApprovalProcessTemplates(auth_token)
        self.entities = Entities(auth_token)
        self.folders = Folders(auth_token)
        self.issues = Issues(auth_token)
        self.permissions = Permissions(auth_token)
        self.rolegroups = RoleGroups(auth_token)
        self.users = Users(auth_token)
