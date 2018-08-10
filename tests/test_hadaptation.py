import pytest
import unittest
from unittest import mock
from partitioner import h_adaptation
from partitioner.h_adaptation import HAdaptation


class TestHAdaptation(unittest.TestCase):

    def setUp(self):
        self.file_path = 'tests/mesh_for_tests/pressure_field.vtk'
        self.ha = HAdaptation(self.file_path)

    def test_load_mesh(self):
        file_path = 'tests/mesh_for_tests/pressure_field.vtk'
        path = 'partitioner.h_adaptation.HAdaptation.load_mesh'
        with mock.patch(path, spec=True) as mocked_load:
            hb = HAdaptation(self.file_path)
            mocked_load.assert_called_with(file_path)


    def test_if_took_all_volumes(self):
        self.assertEqual(len(self.ha.all_volumes), 91)
