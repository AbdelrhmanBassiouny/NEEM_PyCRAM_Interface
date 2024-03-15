from unittest import TestCase

import pandas as pd

from pycram.neems.neem_loader_sqlalchemy import NeemLoader, TaskType, ParticipantType
from pycram.neems.neems_database import *


class TestNeemSqlAlchemy(TestCase):
    nl: NeemLoader

    def setUp(self):
        self.nl = NeemLoader("mysql+pymysql://newuser:password@localhost/test")

    def tearDown(self):
        self.nl.reset()

    def test_sql_like(self):
        tasks = (self.nl.session.query(DulExecutesTask).
                 filter(DulExecutesTask.dul_Task_o.like("%Pour%")).first())
        self.assertIsNotNone(tasks)

    def test_get_task_data(self):
        task_data = self.nl.get_task_data("Pour", use_regex=True)
        self.assertIsNotNone(task_data)

    def test_get_task_data_using_joins(self):
        task_data = self.nl.get_task_data_using_joins("Pour", use_regexp=True)
        self.assertIsNotNone(task_data)

    def test_join_task_participants(self):
        df = (self.nl.select_from(DulExecutesTask).
              join_task_participants()).get_result()
        self.assertIsNotNone(df)

    def test_join_task_participant_types(self):
        df = (self.nl.select_from(DulHasParticipant).
              join_participant_types()).get_result()
        self.assertIsNotNone(df)

    def test_join_task_types(self):
        df = (self.nl.select(DulExecutesTask.dul_Task_o).
              join_task_types()).get_result()
        self.assertIsNotNone(df)

    def test_multi_join(self):
        df = (self.nl.select(TfHeader.stamp, ParticipantType.o.label("particpant")).
              select_from(DulExecutesTask).
              join_task_types().
              join_task_participants().
              join_participant_types().
              join_participant_base_link().
              join_task_time_interval().
              join_tf_on_time_interval().
              join_tf_transfrom().join_neems().join_neems_environment().
              filter_tf_by_base_link().
              filter_by_task_type("Pour", regexp=True)).get_result()
        df.sort_values(by=['stamp'], inplace=True)
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        pd.set_option('display.max_columns', None)
        print(df.head(100))
        self.assertIsNotNone(df)

    def test_get_neem(self):
        neem = self.nl.session.query(Neem).first()
        self.assertIsNotNone(neem)

    def test_get_neem_ids(self):
        neem_ids = self.nl.session.query(Neem._id).all()
        self.assertIsNotNone(neem_ids)
