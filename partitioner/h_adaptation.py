import numpy as np
from pymoab import core
from pymoab import types
from pymoab import topo_util
from helpers import geometric as geo


class HAdaptation:

    def __init__(self, filename):
        self.mb = core.Core()
        self.root_set = self.mb.get_root_set()

        self.load_mesh(filename)

        self.error_tag = self.mb.tag_get_handle(
            "error", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

        self.node_pressure_tag = self.mb.tag_get_handle(
            "node_pressure", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

        self.ref_degree_tag = self.mb.tag_get_handle(
            "ref_degree", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

        self.degree_id_tag = self.mb.tag_get_handle(
            "ref_degree", 1, types.MB_TYPE_DOUBLE, types.MB_TAG_SPARSE, True)

        self.hanging_nodes_tag = self.mb.tag_get_handle(
            "hanging_nodes", 1, types.MB_TYPE_HANDLE, types.MB_TAG_MESH, True)

        self.full_edges_tag = self.mb.tag_get_handle(
            "full_edges", 1, types.MB_TYPE_HANDLE, types.MB_TAG_MESH, True)

        self.hang_nodes = set()

    def load_mesh(self, filename):
        print('bla', filename)
        self.mb.load_file(filename)
        self.mtu = topo_util.MeshTopoUtil(self.mb)
        # print(len(self.all_volumes))

    def init_id_degree(self):
        for vol in self.all_volumes:
            value = np.array([0.0])
            self.mb.tag_set_data(self.degree_id_tag, vol, value)

    def create_full_edges(self):
        self.full_edges_set = set()
        for ent in self.all_volumes:
            full_edges = self.mb.get_adjacencies(ent, 1, True)
            self.full_edges_set = self.full_edges_set | set(full_edges)
            # full_edge_meshset = self.mb.create_meshset()
            # self.mb.add_entities(full_edge_meshset, full_edges)
            # self.mb.tag_set_data(self.full_edges_tag, ent, full_edge_meshset)

    def create_half_node(self, full_edge, deg_id=0):
        nodes = self.mb.get_adjacencies(full_edge, 0)
        nodes_crds = self.mb.get_coords(nodes).reshape([2, 3])
        coord_half_node = (nodes_crds[0] + nodes_crds[1]) / 2.0
        half_node = self.mb.create_vertices(coord_half_node)
        self.mtu.construct_aentities(half_node)
        self.hang_nodes = self.hang_nodes | set(half_node)
        self.mb.tag_set_data(self.degree_id_tag, half_node, deg_id)

        return half_node

    def neighbour_treat(self, elem):
        edges = self.mb.get_adjacencies(elem, 1, 1)
        full_edges = self.full_edges_set & set(edges)
        for full_edge in full_edges:
            half_node = self.create_half_node(full_edge)
            neighbour = self.mtu.get_bridge_adjacencies(elem, 1, 2)
            nodes = self.mb.get_adjacencies(neighbour, 0)
            new_nodes = np.append(nodes, half_node)
            new_nodes_crds = self.mb.get_coords(new_nodes).reshape(
                             [len(new_nodes), 3])
            indices = geo._counterclock_sort(new_nodes_crds)
            new_nodes = new_nodes[indices]
            new_neighbour = self.mb.create_element(types.MBPOLYGON, new_nodes)
            self.mb.delete_entities(neighbour)
            self.update_list([neighbour], [new_neighbour])

    def update_list(self, old_elems, new_elems):
        for an_old in old_elems:
            self.adapt_list.remove(an_old)

        for a_new in new_elems:
            self.adapt_list.append(a_new)

    def partitionate(self, elem):
        self.neighbour_treat(elem)

    def adapt(self):
        self.all_volumes = self.mb.get_entities_by_dimension(self.root_set, 2)
        self.adapt_list = list(self.all_volumes)
        self.create_full_edges()
        self.init_id_degree()
