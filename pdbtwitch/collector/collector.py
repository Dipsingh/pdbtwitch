import requests
import pandas as pd
from textwrap import dedent
from pdbtwitch.config.config import environment
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Panel, Tabs, Button
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from bokeh.models import ColorBar, PrintfTickFormatter, LabelSet, Select, CustomJS
from bokeh.models import DataTable, TableColumn


class PeeringData():

    def __init__(self):
        self.id_no = 0
        self.org_id = 0
        self.df = self.get_peeringdb_data()

    def get_peeringdb_data(self):
        session = requests.session()
        asn_no = environment.env.get('asn')
        asn_query = dedent(environment.env.get('asn_api'))
        net_query = dedent(environment.env.get('net_api'))
        r = session.get(asn_query.format(asn_no=asn_no))
        if r.status_code == 200:
            org_data = r.json().get('data')[0]
            self.id_no = org_data['id']
            self.org_id = org_data['org_id']
            r = session.get(net_query.format(id_no=self.id_no))
            if r.status_code == 200:
                df = pd.DataFrame.from_dict(r.json().get('data'))
                return df

        return pd.DataFrame()

    def get_agg_speed(self):
        """
        :return:
        """
        agg_gps = self.df['speed'].sum() / 1000
        return agg_gps

    def get_unique_org_peerings(self):
        unique_orgs = self.df['name'].unique().size
        return unique_orgs

    def get_total_peerings(self):
        total_peerings = self.df['id'].size
        return total_peerings

    def get_is_rs_peer(self):
        return self.df.loc[self.df.is_rs_peer].shape[0]

    def plot_data_table(self):
        source = ColumnDataSource(self.df)
        columns = [
            TableColumn(field="name", title="IX Name"),
            TableColumn(field="asn", title="ASN"),
            TableColumn(field="ipaddr6", title="IPv6 Addr"),
            TableColumn(field="ipaddr4", title="IPv4 Addr"),
            TableColumn(field="speed", title="Speed"),
            TableColumn(field="is_rs_peer", title="RS Peer"),
            TableColumn(field="status", title="Status"),
        ]
        data_table = DataTable(source=source, columns=columns, width=800, height=280)
        return column(data_table)

    def plot_peering_summary(self):
        unique_org = self.get_unique_org_peerings()
        total_peering = self.get_total_peerings()
        rs_peers_count = self.df.loc[self.df.is_rs_peer].shape[0]
        ops_peers_count = self.df.loc[self.df.operational].shape[0]
        categories = ['Unique IX', 'Total Peers', 'RS Peers', 'Operational Peers']
        counts = [unique_org, total_peering, rs_peers_count, ops_peers_count]
        source = ColumnDataSource(dict(x=['Unique IX', 'Total Peers', 'RS Peers', 'Operational Peers'],
                                       y=[unique_org, total_peering, rs_peers_count, ops_peers_count]))
        p = figure(x_range=categories, plot_height=400, plot_width=600, title="Public IX Peering Summary",
                   toolbar_location=None, tools="")
        p.vbar(x=categories, top=counts, width=0.7)
        p.xgrid.grid_line_color = None
        p.yaxis.axis_label = 'Count'
        p.y_range.start = 0
        labels = LabelSet(x='x', y='y', text='y', level='glyph',
                          x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')

        p.add_layout(labels)
        return column(p)

    def plot_aggregate_capacity(self):
        agg_cap = self.get_agg_speed()
        categories = ['Aggregate Peering Capacity']
        counts = [agg_cap]
        source = ColumnDataSource(dict(x=['Aggregate Peering Capacity'],
                                       y=[agg_cap]))
        p1 = figure(x_range=categories, plot_height=400, plot_width=300, title="Aggregate Peering Capacity",
                    toolbar_location=None, tools="")
        p1.vbar(x=categories, top=counts, width=0.3)
        p1.xgrid.grid_line_color = None
        p1.yaxis.axis_label = 'Gbps'
        p1.y_range.start = 0
        labels = LabelSet(x='x', y='y', text='y', level='glyph',
                          x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')
        p1.add_layout(labels)
        return p1
