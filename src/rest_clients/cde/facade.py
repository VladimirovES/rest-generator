from rest_client.client import ApiClient

from .access_setting import AccessSetting
from .approval_process_templates import ApprovalProcessTemplates
from .approval_processes import ApprovalProcesses
from .checklists import Checklists
from .element_documents import ElementDocuments
from .entities import Entities
from .entity_versions import EntityVersions
from .folders import Folders
from .issues import Issues
from .local import Local
from .model_layers import ModelLayers
from .model_rooms import ModelRooms
from .model_systems import ModelSystems
from .permissions import Permissions
from .role_groups import RoleGroups
from .users import Users


class CdeFacade:
    def __init__(self, client: ApiClient):
        self._client = client

        self.accessSetting = AccessSetting(self._client)
        self.approvalProcessTemplates = ApprovalProcessTemplates(self._client)
        self.approvalProcesses = ApprovalProcesses(self._client)
        self.checklists = Checklists(self._client)
        self.elementDocuments = ElementDocuments(self._client)
        self.entities = Entities(self._client)
        self.entityVersions = EntityVersions(self._client)
        self.folders = Folders(self._client)
        self.issues = Issues(self._client)
        self.local = Local(self._client)
        self.modelLayers = ModelLayers(self._client)
        self.modelRooms = ModelRooms(self._client)
        self.modelSystems = ModelSystems(self._client)
        self.permissions = Permissions(self._client)
        self.roleGroups = RoleGroups(self._client)
        self.users = Users(self._client)
