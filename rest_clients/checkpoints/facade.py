from my_codegen.rest_client.client import ApiClient

from .access_passes import AccessPasses
from .checkpoints import Checkpoints
from .files import Files
from .pass_status import PassStatus
from .probe import Probe
from .project import Project
from .report import Report
from .visit_sessions import VisitSessions


class CheckpointsFacade:
    def __init__(self, client: ApiClient):
        self._client = client

        self.accessPasses = AccessPasses(self._client)
        self.checkpoints = Checkpoints(self._client)
        self.files = Files(self._client)
        self.passStatus = PassStatus(self._client)
        self.probe = Probe(self._client)
        self.project = Project(self._client)
        self.report = Report(self._client)
        self.visitSessions = VisitSessions(self._client)
