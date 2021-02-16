from google.cloud import monitoring_v3
from collections import defaultdict


PROJECT_ID = 'hail-vdc'
NAMESPACE_NAME = 'dgoldste'
metrics_uploader = None


def metrics_init(log):
    global metrics_uploader
    if metrics_uploader is None:
        metrics_uploader = Metrics(log, PROJECT_ID, NAMESPACE_NAME)


def add_point(metric_name, value):
    global metrics_uploader
    metrics_uploader.add_point(metric_name, value)


class Metrics:
    def __init__(self, log, project_id, namespace):
        self.log = log
        self.project_id = project_id
        self.namespace = namespace
        self.series = defaultdict(list)

    def add_point(self, metric_name, value):
        self.series[metric_name].append(value)
        if len(self.series[metric_name]) > 5:
            self.push_metrics()

    def push_metrics(self):
        self.series = defaultdict(list)
