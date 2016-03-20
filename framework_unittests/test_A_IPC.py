from unittest import TestCase
from server.ipc import IPC
from server.serverproxy import ServerProxy
import time
from typing import List
from threading import Timer, Event


class TestIPC(TestCase):

    ipc_server = None

    @classmethod
    def setUpClass(cls):
        #  starts the IPC server in the same process
        t = Timer(0.0, TestIPC.start_ipc_server)
        t.start()  # but in other thread
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        TestIPC.ipc_server.shutdown()

    def test_exist_stop_event(self):
        """ tests if the stop event still exist in the BaseManager
        if not the stop methods has to be improved
        """
        print(TestIPC.ipc_server._server_object.stop_event)
        assert isinstance(TestIPC.ipc_server._server_object.stop_event, Event)

    @staticmethod
    def start_ipc_server():
        TestIPC.ipc_server = IPC()
        TestIPC.ipc_server.start_ipc_server(DummyServer, True)

    def test_proxy_object(self):

        ipc_client = IPC()
        ipc_client.connect(False)
        server_proxy = ipc_client.get_server_proxy()

        rep = server_proxy.get_test_results()
        #  print(rep)
        assert rep[1].text == "test"

        DummyServer.testList.append("test1")
        server_proxy.start_test("", "")
        #  print(DummyServer.testList)
        testss = server_proxy.get_tests()
        #  print(testss)
        assert len(testss) == 3
        assert testss[0] == "test1"  # wäre der Server in einem anderen Prozess gestartet, wäre 'test1' nicht vorhanden
        assert testss[1] == "test2"
        assert testss[2] == "test3"


class DummyObject(object):
    def __init__(self, input_text):
        self.text = input_text


class DummyServer(ServerProxy):
    testList = []

    @classmethod
    def start_test(cls, router_id, test_id):
        DummyServer.testList.append("test2")
        cls.testList.append("test3")
        pass

    @classmethod
    def get_running_tests(cls) -> []:
        pass

    @classmethod
    def get_routers(cls) -> []:
        return ["lol"]

    @classmethod
    def get_test_results(cls) -> []:
        d = DummyObject("test")
        return [id(d), d]

    @classmethod
    def get_tests(cls) -> []:
        return cls.testList

    @classmethod
    def get_firmwares(cls) -> []:
        pass

    @classmethod
    def stop(cls) -> []:
        pass

    @classmethod
    def update_router_info(cls, router_ids, update_all):
        pass

    @classmethod
    def get_router_by_id(cls, router_id) -> []:
        pass

    @classmethod
    def sysupdate_firmware(cls, router_ids, update_all) -> []:
        pass

    @classmethod
    def sysupgrade_firmware(cls, router_ids, upgrade_all, n) -> []:
        pass

    @classmethod
    def stop_all_tasks(cls):
        pass

    @classmethod
    def setup_web_configuration(cls, router_ids, setup_all: bool, wizard: bool):
        pass

    @classmethod
    def reboot_router(cls, router_ids, reboot_all: bool, configmode: bool):
        pass

    @classmethod
    def get_server_version(cls) -> str:
        pass

    @classmethod
    def get_routers_task_queue_size(cls, router_id: int) -> [str]:
        pass

    @classmethod
    def start_test_set(cls, router_id: int, test_set_name: str) -> bool:
        pass

    @classmethod
    def delete_test_results(cls) -> int:
        pass

    @classmethod
    def control_switch(cls, router_ids: List[int], switch_all: bool, on_or_off: bool):
        pass

    @classmethod
    def register_tty(cls, tty_name: str = ''):
        pass
