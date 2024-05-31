from neem_pycram_interface.neem_pycram_interface import PyCRAMNEEMInterface
from neem_pycram_interface.neem_segmentor import NEEMSegmentor, run_event_detectors
from unittest import TestCase

from pycram.ros.viz_marker_publisher import VizMarkerPublisher
from pycram.world import World


class TestNEEMSegmentor(TestCase):
    ns: NEEMSegmentor
    viz_mark_publisher: VizMarkerPublisher

    @classmethod
    def setUpClass(cls):
        pni = PyCRAMNEEMInterface('mysql+pymysql://newuser:password@localhost/test')
        cls.ns = NEEMSegmentor(pni)
        cls.viz_mark_publisher = VizMarkerPublisher()

    @classmethod
    def tearDownClass(cls):
        cls.viz_mark_publisher._stop_publishing()
        if World.current_world is not None:
            World.current_world.exit()

    def test_detect_contacts_from_neem_motion_replay(self):
        self.ns.detect_contacts_from_neem_motion_replay(17)

    def test_event_logger(self):
        run_event_detectors()

