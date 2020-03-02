from socket import socket
import typing as ty
import pytest as pt
import reapy as rpr
from reapy import reascript_api as RPR
from IPy import IP
from ..connections import jack_backend as bck
import mock
from warnings import warn
import jack
from random import randint


class MonkeyTrack():
    def __init__(
        self,
        id: ty.Union[str, int] = None,
        project: ty.Optional[rpr.Project] = None
    ) -> None:
        self.id = id
        self.project = project

    def __repr__(self) -> str:
        return f'(MediaTrack id={self.id}, project={self.project})'

    def __eq__(self, other: object) -> bool:
        # print('cmp called')
        if not isinstance(other, MonkeyTrack):
            # raise RuntimeError('not equal')
            return False
        if other.id == self.id:
            return True
        # raise RuntimeError('not equal')
        return False


class MonkeyProject():
    def __init__(self, id: ty.Optional[str] = None, index: int = -1) -> None:
        self.id = id
        self.index = index
        self.name = 'defaultname'

    def __repr__(self) -> str:
        return f'(ReaProject id={self.id}, index={self.index}'

    def make_current_project(self) -> ty.ContextManager:
        class CM:
            def __enter__(self) -> None:
                return None

            def __exit__(self, exc_type, exc_val, exc_tb):
                return

        return CM()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MonkeyProject):
            return False
        if self.id == other.id:
            return True
        if self.name == other.name:
            return True
        return False


class MonkeyJackPort:
    def __init__(self, name: str, uuid: str = 'basic_uuid') -> None:
        self.name = name
        self.uuid = uuid


def get_test_data(
) -> ty.Tuple[bck._HostInfo, bck._HostInfo, ty.List[bck._RTrackPort], ty.
              List[bck._RTrackPort]]:
    master: bck._HostInfo = dict(
        host='localhost',
        reaper_in_ports=[
            dict(idx=0, name='system:midi_capture_1'),
            dict(idx=1, name='system:midi_capture_2'),
            dict(idx=2, name='MIDI Input 3'),
            dict(idx=3, name='MIDI Input 4'),
            dict(idx=4, name='MIDI Input 5'),
        ],
        jack_in_ports=[
            dict(
                name='MIDI Input 1',
                connection=dict(host='system', name='midi_capture_1')
            ),
            dict(
                name='MIDI Input 2',
                connection=dict(host='system', name='midi_capture_2')
            ),
            dict(
                name='MIDI Input 3',
                connection=dict(host='REAPER', name='MIDI Output 6')
            ),
            dict(
                name='MIDI Input 4',
                connection=dict(host='192.168.2.2', name='midi_from_slave_1')
            ),
        ],
        in_tracks=[
            rpr.Track(
                id='slave_track_1', project=rpr.Project(id='slave_project_1')
            )
        ],
        reaper_out_ports=[
            dict(idx=0, name='system:midi_playback_1'),
            dict(idx=1, name='system:midi_playback_2'),
            dict(idx=2, name='MIDI Output 3'),
            dict(idx=3, name='MIDI Output 4'),
            dict(idx=4, name='MIDI Output 5'),
            dict(idx=5, name='MIDI Output 6'),
            dict(idx=6, name='MIDI Output 7'),
        ],
        jack_out_ports=[
            dict(
                name='MIDI Output 1',
                connection=dict(host='system', name='midi_playback_1')
            ),
            dict(
                name='MIDI Output 2',
                connection=dict(host='system', name='midi_playback_2')
            ),
            dict(
                name='MIDI Output 3',
                connection=dict(host='192.168.2.2', name='midi_to_slave_1')
            ),
            dict(
                name='MIDI Output 4',
                connection=dict(host='192.168.2.2', name='midi_to_slave_2')
            ),
            dict(
                name='MIDI Output 5',
                connection=dict(host='192.168.2.2', name='midi_to_slave_3')
            ),
            dict(
                name='MIDI Output 6',
                connection=dict(host='REAPER', name='MIDI Input 3')
            ),
        ],
        out_tracks=[
            dict(
                track=rpr.Track(
                    id='master_track_1',
                    project=rpr.Project(id='master_project')
                ),
                slave=dict(
                    host='192.168.2.2',
                    track=rpr.Track(
                        id='slave_track_2',
                        project=rpr.Project(id='slave_project_2')
                    )
                )
            ),
            dict(
                track=rpr.Track(
                    id='master_track_2',
                    project=rpr.Project(id='master_project')
                ),
                slave=dict(
                    host='192.168.2.2',
                    track=rpr.Track(
                        id='slave_track_3',
                        project=rpr.Project(id='slave_project_2')
                    )
                )
            ),
            dict(
                track=rpr.Track(
                    id='master_track_3',
                    project=rpr.Project(id='master_project')
                ),
                slave=dict(
                    host='192.168.2.2',
                    track=rpr.Track(
                        id='slave_track_4',
                        project=rpr.Project(id='slave_project_3')
                    )
                )
            ),
            dict(
                track=rpr.Track(
                    id='master_track_4',
                    project=rpr.Project(id='master_project')
                ),
                slave=dict(
                    host='localhost',
                    track=rpr.Track(
                        id='slave_track_1',
                        project=rpr.Project(id='slave_project_1')
                    )
                )
            ),
        ],
    )
    slave: bck._HostInfo = dict(
        host='192.168.2.2',
        reaper_in_ports=[
            dict(idx=0, name='system:midi_capture_1'),
            dict(idx=1, name='system:midi_capture_2'),
            dict(idx=2, name='system:midi_capture_3'),
            dict(idx=3, name='system:midi_capture_4'),
            dict(idx=4, name='MIDI Input 5'),
        ],
        jack_in_ports=[
            dict(
                name='MIDI Input 1',
                connection=dict(host='system', name='midi_capture_1')
            ),
            dict(
                name='MIDI Input 2',
                connection=dict(host='system', name='midi_capture_2')
            ),
            dict(
                name='MIDI Input 3',
                connection=dict(host='system', name='midi_capture_3')
            ),
            dict(
                name='MIDI Input 4',
                connection=dict(host='system', name='midi_capture_4')
            ),
        ],
        in_tracks=[
            rpr.Track(
                id='slave_track_2', project=rpr.Project(id='slave_project_2')
            ),
            rpr.Track(
                id='slave_track_3', project=rpr.Project(id='slave_project_2')
            ),
            rpr.Track(
                id='slave_track_4', project=rpr.Project(id='slave_project_3')
            )
        ],
        reaper_out_ports=[
            dict(idx=0, name='system:midi_playback_1'),
            dict(idx=1, name='MIDI Output 2'),
        ],
        jack_out_ports=[
            dict(
                name='MIDI Output 1',
                connection=dict(host='system', name='midi_playback_1')
            )
        ],
        out_tracks=[],
    )
    midi_outs: ty.List[bck._RTrackPort] = [
        dict(
            host='localhost',
            track=rpr.Track(
                id='master_track_1', project=rpr.Project(id='master_project')
            ),
            port=dict(idx=2, name='MIDI Output 3'),
        ),
        dict(
            host='localhost',
            track=rpr.Track(
                id='master_track_2', project=rpr.Project(id='master_project')
            ),
            port=dict(idx=3, name='MIDI Output 4'),
        ),
        dict(
            host='localhost',
            track=rpr.Track(
                id='master_track_3', project=rpr.Project(id='master_project')
            ),
            port=dict(idx=4, name='MIDI Output 5'),
        ),
        dict(
            host='localhost',
            track=rpr.Track(
                id='master_track_4', project=rpr.Project(id='master_project')
            ),
            port=dict(idx=5, name='MIDI Output 6'),
        ),
    ]
    midi_ins: ty.List[bck._RTrackPort] = [
        dict(
            host='localhost',
            track=rpr.Track(
                id='slave_track_1', project=rpr.Project(id='slave_project_1')
            ),
            port=dict(idx=2, name='MIDI Input 3')
        ),
        dict(
            host='192.168.2.2',
            track=rpr.Track(
                id='slave_track_2', project=rpr.Project(id='slave_project_2')
            ),
            port=dict(idx=0, name='system:midi_capture_1'),
        ),
        dict(
            host='192.168.2.2',
            track=rpr.Track(
                id='slave_track_3', project=rpr.Project(id='slave_project_2')
            ),
            port=dict(idx=1, name='system:midi_capture_2'),
        ),
        dict(
            host='192.168.2.2',
            track=rpr.Track(
                id='slave_track_4', project=rpr.Project(id='slave_project_3')
            ),
            port=dict(idx=2, name='system:midi_capture_3'),
        ),
    ]
    return master, slave, midi_outs, midi_ins


def monkey_connect(self, *args, **kwargs) -> None:
    pass


def monkey_get_out_tracks(
    t_master: bck._HostInfo
) -> ty.Tuple[ty.List[rpr.Track], ty.List[rpr.Track], ty.List[str]]:
    m_tracks: ty.List[rpr.Track] = []
    s_tracks: ty.List[rpr.Track] = []
    s_hosts: ty.List[str] = []
    for track in t_master['out_tracks']:
        m_tracks.append(track['track'])
        s_tracks.append(track['slave']['track'])
        s_hosts.append(track['slave']['host'])
    out = m_tracks, s_tracks, s_hosts
    return out


class MonkeyClient:
    def __init___(self, port, host='localhost'):
        self.port, self.host = port, host

    def request(self, function, input=None):
        return 'monkey_client_request'


def test_parce_port_name(monkeypatch):
    class Port:
        def __init__(self, name: str) -> None:
            self.name = name

    port = Port('REAPER:MIDI Output 3')
    assert bck.parce_port_name(port) == ('REAPER', 'MIDI Output 3')
    port.name = 'my_strange port name:'
    with pt.raises(bck.PortNameError, match='strange port name'):
        bck.parce_port_name(port)


def get_jack_ports_test_data(
) -> ty.Tuple[ty.List[bck._JMidiPort], ty.List[bck._JMidiPort]]:
    in_ports = [
        bck._JMidiPort(
            name='MIDI Input 1',
            connection=bck._JConnection(host='system', name='midi_capture_1')
        ),
        bck._JMidiPort(
            name='MIDI Input 2',
            connection=bck._JConnection(host='REAPER', name='MIDI Out 2')
        )
    ]
    out_ports = [
        bck._JMidiPort(
            name='MIDI Out 1',
            connection=bck._JConnection(host='system', name='midi_playback_1')
        ),
        bck._JMidiPort(
            name='MIDI Out 2',
            connection=bck._JConnection(host='REAPER', name='MIDI Input 2')
        )
    ]
    return in_ports, out_ports


def monkey_Client_get_ports(ins: int = 2,
                            outs: int = 2) -> ty.List[MonkeyJackPort]:
    ins = ins
    outs = outs

    def real_func(
        self, name_pattern='', is_midi=False, is_input=False, is_output=False
    ):
        ports = []
        if not is_midi:
            return []
        if is_input:
            for i in range(ins):
                ports.append(MonkeyJackPort(f'REAPER:MIDI Input {i+1}'))
        if is_output:
            for i in range(outs):
                ports.append(MonkeyJackPort(f'REAPER:MIDI Out {i+1}'))
        return ports

    return real_func


def monkey_get_all_connections(
    min: int = 1, max: int = 1, *, from_list: ty.List[str] = []
) -> ty.List[MonkeyJackPort]:
    def_in = MonkeyJackPort('system:midi_capture_1')
    if not from_list:
        return lambda self, port: [def_in] * randint(min, max)

    def func(self, port) -> ty.List[MonkeyJackPort]:
        return [MonkeyJackPort(from_list.pop(0))]

    return func


def test_get_jack_ports_parametrized(monkeypatch):
    t_in_ports, t_out_ports = get_jack_ports_test_data()
    monkeypatch.setattr(
        jack.Client, 'get_ports', monkey_Client_get_ports(ins=2, outs=2)
    )
    monkeypatch.setattr(
        jack.Client, 'get_all_connections',
        monkey_get_all_connections(
            from_list=['system:midi_capture_1', 'REAPER:MIDI Out 2']
        )
    )
    r_ins = bck.get_jack_ports_parametrized(want_output=False)
    assert r_ins == t_in_ports
    monkeypatch.setattr(
        jack.Client, 'get_all_connections',
        monkey_get_all_connections(min=2, max=2)
    )
    r_ins = bck.get_jack_ports_parametrized(want_output=False)
    assert r_ins == []
    r_outs = bck.get_jack_ports_parametrized(want_output=True)
    assert r_outs == []
    monkeypatch.setattr(
        jack.Client, 'get_all_connections',
        monkey_get_all_connections(
            from_list=['system:midi_playback_1', 'REAPER:MIDI Input 2']
        )
    )
    r_outs = bck.get_jack_ports_parametrized(want_output=True)
    assert r_outs == t_out_ports


# @pt.mark.skip
def test_get_jack_ports(monkeypatch):
    test_response = get_jack_ports_test_data()

    def mocked(want_output: bool = False) -> ty.List[bck._JMidiPort]:
        return test_response[1] if want_output else test_response[0]

    monkeypatch.setattr(bck, 'get_jack_ports_parametrized', mocked)
    response = bck.get_jack_ports()
    assert response == test_response


def test_get_host_ports(monkeypatch):
    result = bck.get_host_ports('localhost')


# def test_fill_host_info(monkeypatch):
#     ...


def test_get_connection_task(monkeypatch):
    monkeypatch.setattr(rpr, 'Track', MonkeyTrack)
    monkeypatch.setattr(rpr, 'Project', MonkeyProject)
    t_master, t_slave, t_midi_outs, t_midi_ins = get_test_data()
    r_midi_outs, r_midi_ins = bck.get_connection_task([t_master, t_slave])

    assert t_midi_ins == r_midi_ins
    assert t_midi_outs == r_midi_outs


# @pt.mark.skip
def test_match_host_ports(monkeypatch):
    monkeypatch.setattr(rpr, 'Track', MonkeyTrack)
    monkeypatch.setattr(rpr, 'Project', MonkeyProject)
    t_host = dict(
        host='localhost',
        reaper_in_ports=[
            dict(idx=0, name='system:midi_capture_1'),
            dict(idx=2, name='MIDI Input 3'),
            dict(idx=3, name='MIDI Input 4'),
            dict(idx=4, name='MIDI Input 5'),
        ],
        jack_in_ports=[
            dict(
                name='MIDI Input 1',
                connection=dict(host='system', name='midi_capture_1')
            ),
            dict(
                name='MIDI Input 3',
                connection=dict(host='REAPER', name='MIDI Output 6')
            ),
            dict(
                name='MIDI Input 4',
                connection=dict(host='192.168.2.2', name='midi_from_slave_1')
            ),
        ],
        reaper_out_ports=[
            dict(idx=0, name='system:midi_playback_1'),
            dict(idx=2, name='MIDI Output 3'),
            dict(idx=5, name='MIDI Output 6'),
        ],
        jack_out_ports=[
            dict(
                name='MIDI Output 1',
                connection=dict(host='system', name='midi_playback_1')
            ),
            dict(
                name='MIDI Output 3',
                connection=dict(host='192.168.2.2', name='midi_to_slave_1')
            ),
            dict(
                name='MIDI Output 6',
                connection=dict(host='REAPER', name='MIDI Input 3')
            ),
        ],
    )
    t_output = (
        [
            dict(
                host='localhost',
                port=dict(idx=2, name='MIDI Input 3'),
                dest_host='localhost',
            ),
            dict(
                host='localhost',
                port=dict(idx=3, name='MIDI Input 4'),
                dest_host='192.168.2.2',
            )
        ],
        [
            dict(
                host='localhost',
                port=dict(idx=2, name='MIDI Output 3'),
                dest_host='192.168.2.2',
            ),
            dict(
                host='localhost',
                port=dict(idx=5, name='MIDI Output 6'),
                dest_host='localhost',
            )
        ],
    )
    assert bck.match_host_ports(t_host) == t_output


@mock.patch('reapy.Project')
@mock.patch('reapy.Track')
@mock.patch('reapy.connect')
@mock.patch('session_management.connections.jack_backend.set_track_midi_in')
@mock.patch('session_management.connections.jack_backend.set_track_midi_out')
def test_connect(
    set_track_midi_out, set_track_midi_in, monkey_connect, MonkeyTrack,
    MonkeyProject
):
    warn(UserWarning('TODO: add exception if not enougth system ports'))
    # t_master, t_slave, t_midi_outs, t_midi_ins = get_test_data()
    # task = bck.get_connection_task([t_master, t_slave])
    track = rpr.Track(
        id='slave_track_2', project=rpr.Project(id='slave_project_2')
    )
    task = (
        [
            dict(
                host='192.168.2.2',
                track=track,
                port=dict(idx=2, name='system:midi_capture_3'),
            ),
        ], []
    )
    bck.connect_by_task(task)
    monkey_connect.assert_called_with('192.168.2.2')
    track.project.make_current_project.assert_called()
    set_track_midi_in.assert_called_with(track, 2)

    track = rpr.Track(
        id='master_track_1', project=rpr.Project(id='master_project')
    )

    task = (
        [], [
            dict(
                host='localhost',
                track=rpr.Track(
                    id='master_track_1',
                    project=rpr.Project(id='master_project')
                ),
                port=dict(idx=3, name='MIDI Output 4'),
            ),
        ]
    )
    bck.connect_by_task(task)
    monkey_connect.assert_called_with('localhost')
    track.project.make_current_project.assert_called()
    set_track_midi_out.assert_called_with(track, 3)
