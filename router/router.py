from enum import Enum
from firmware.firmware import Firmware
from network.remote_system import RemoteSystem
from router.memory import RAM, Flashdriver


class Mode(Enum):
    """
    The Router can be in two modes: normal and configuration.
    If the mode changes also the ip-address changes.
    """""
    normal = 1
    configuration = 2
    unknown = 3
    off = 4


class Router(RemoteSystem):
    """
    This class represent a Freifunk-Router
    """""

    def __init__(self, id: int, vlan_iface_name: str, vlan_iface_id: int, ip: str, ip_mask: int,
                 config_ip: str, config_ip_mask: int, usr_name: str, usr_password: str, power_socket: int):
        """
        :param id: The id of the Router
        :param vlan_iface_name: The name of the VLAN, which the Router is connected to
        :param vlan_iface_id: The id of the VLAN, which the RemoteSystem is connected to
        :param ip: The IP on which the RemoteSystem is listening in normal-mode
        :param ip_mask: Mask of the IP on which the RemoteSystem is listening in normal-mode
        :param config_ip: The IP on which the RemoteSystem is listening in configuration-mode
        :param config_ip_mask: Mask of the IP on which the RemoteSystem is listening in configuration-mode
        :param usr_name: The user-name that is used via SSH
        :param usr_password: The password that is used via SSH
        :param power_socket: The port on the power_socker where the Router is connected to.
        :return:
        """

        RemoteSystem.__init__(self)

        self._id = id
        self._ip = ip
        self._ip_mask = ip_mask
        self._config_ip = config_ip
        self._config_ip_mask = config_ip_mask
        self._vlan_iface_id = vlan_iface_id
        self._vlan_iface_name = vlan_iface_name
        self._namespace_name = "nsp" + str(self._vlan_iface_id)
        self._usr_name = usr_name
        self._usr_password = usr_password
        self._power_socket = power_socket

        # Optional values
        self._mode = Mode.unknown
        self._model = ""
        self._mac = '00:00:00:00:00:00'
        self._node_name = ""
        self._public_key = ""
        self.network_interfaces = dict()
        self.cpu_processes = list()
        self.sockets = list()
        self._ram = None
        self._flashdriver = None
        self._firmware = Firmware.get_default_firmware()
        self.uci = dict()
        self.bat_originators = list()

    def update(self, new_router) -> None:
        """
        Updates the properties from this router
        :param new_router: router with newer property values
        :return:
        """
        self._model = new_router.model
        self._mac = new_router.mac
        self._mode = new_router.mode
        self._node_name = new_router.node_name
        self._public_key = new_router.public_key
        self.network_interfaces = new_router.network_interfaces
        self.cpu_processes = new_router.cpu_processes
        self.sockets = new_router.sockets
        self._ram = new_router.ram
        self._flashdriver = new_router.flashdriver
        self._firmware = new_router.firmware
        self.uci = new_router.uci
        self.bat_originators = new_router.bat_originators

    @property
    def id(self) -> int:
        """
        ID of the :py:class:`Router`

        :return: ID number as in
        """
        return self._id

    def set_id(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._id = value

    @property
    def ip(self) -> str:
        """
        IP number of the Router. In dependency of the Mode.

        :return: IP of the Router
        """
        if self._mode == Mode.configuration:
            return self._config_ip
        else:
            return self._ip

    @property
    def ip_mask(self) -> int:
        """
        Mask of the IP. In dependency of the Mode.

        :return: Mask of the IP
        """
        if self._mode == Mode.configuration:
            return self._config_ip_mask
        else:
            return self._ip_mask

    @property
    def vlan_iface_id(self) -> int:
        """
        The VLAN_interface_id from Router.

        :return VLAN_interface_id
        """
        return self._vlan_iface_id

    @property
    def vlan_iface_name(self) -> str:
        """
        The name of the VLAN, which the Router is connected to.

        :return: VLAN_iface_name
        """
        return self._vlan_iface_name

    # Optional information

    @property
    def usr_name(self) -> str:
        """
        Username of the admin account on the router.

        :return: Router_user_name
        """
        return self._usr_name

    @property
    def usr_password(self) -> str:
        """
        Password of the admin account on the router

        :return: Router_user_password
        """
        return self._usr_password

    @property
    def node_name(self) -> str:
        """
        Name of the Router, that is seen from the community.

        :return: Router_node_name
        """
        return self._node_name

    @node_name.setter
    def node_name(self, value: str):
        """
        :type value: string
        """
        assert isinstance(value, str)
        self._node_name = value

    @property
    def public_key(self) -> str:
        """
        Public-key of the Router, that is used to communicate with other Freifunk-Routers.

        :return: Router_public_key
        """
        return self._public_key

    @public_key.setter
    def public_key(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._public_key = value

    @property
    def mac(self) -> str:
        """
        The mac of the Router.

        :return: Router_mac
        """
        return self._mac

    @mac.setter
    def mac(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._mac = value

    @property
    def model(self) -> str:
        """
        The model and version of the router.

        :return Router_model
        """
        return self._model

    @model.setter
    def model(self, value: str):
        """
        :type value: str
        """
        assert isinstance(value, str)
        self._model = value

    @property
    def power_socket(self) -> int:
        """
        The port on the power_socker where the Router is connected to.

        :return: The port on the power_socker
        """
        return self._power_socket

    @power_socket.setter
    def power_socket(self, value: int):
        """
        :type value: int
        """
        assert isinstance(value, int)
        self._power_socket = value

    @property
    def firmware(self) -> Firmware:
        """
        The Firmware that flashed on the Router.

        :return: Router_firmware
        """
        return self._firmware

    @firmware.setter
    def firmware(self, value: Firmware):
        """
        :type value: :py:class:`Firmware`
        """
        assert isinstance(value, Firmware)
        self._firmware = value

    @property
    def namespace_name(self) -> str:
        """
        The name of the Namespace, where the VLAN, that is used to communicate to the Router, is encapsulated.

        :return: Router_namespace_name
        """
        return self._namespace_name

    @property
    def mode(self) -> Mode:
        """
        The Mode of the Router.

        :return: Router_mode
        """
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        """
        :type value: Mode
        """
        assert isinstance(value, Mode)
        self._mode = value

    @property
    def ram(self) -> RAM:
        """
        The RAM of the Router.

        :return: Router_ram
        """
        return self._ram

    @ram.setter
    def ram(self, value: RAM):
        """
        :type value: RAM
        """
        assert isinstance(value, RAM)
        self._ram = value

    @property
    def flashdriver(self) -> Flashdriver:
        """
        The Flashdriver of the Router.

        :rtype: Router_flashdriver
        :return:
        """
        return self._flashdriver

    @flashdriver.setter
    def flashdriver(self, value: Flashdriver):
        """
        :type value: Flashdriver
        """
        assert isinstance(value, Flashdriver)
        self._flashdriver = value

    def __str__(self):
        string = "\nRouter: \n"
        string += "ID: " + str(self.id) + "\n"
        string += "MAC: " + self.mac + "\n"
        string += "Model: " + self.model + "\n"
        string += "Node Name: " + self.node_name + "\n"
        string += "Public Key: " + self.public_key + "\n"
        string += "Namespace: " + self.namespace_name + "\n"
        string += "Vlan: " + self.vlan_iface_name + "(" + str(self.vlan_iface_id) + ")\n"
        string += "IP: " + self.ip + "/" + str(self.ip_mask) + "\n"
        string += "Power Socket: " + str(self.power_socket) + "\n"
        string += "User Name: " + self.usr_name + ", Password: " + self._usr_password + "\n"

        string += "\nInterfaces: \n"
        for interface in self.network_interfaces.values():
            string += str(interface) + "\n"

        string += "\nSockets: \n"
        for socket in self.sockets:
            string += str(socket) + "\n"

        string += "\nCPU Processes: \n"
        for cpu_process in self.cpu_processes:
            string += str(cpu_process) + "\n"

        string += "\nMemory: " + str(self.ram) + "\n"

        return string
