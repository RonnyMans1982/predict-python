# Test performance for thesis
import time
import unittest

from django.test import TestCase

from core.core import calculate
from core.hyperopt_wrapper import calculate_hyperopt
from core.tests.test_prepare import split_single, add_default_config
from encoders.encoding_container import EncodingContainer, BOOLEAN
from encoders.label_container import LabelContainer, DURATION, REMAINING_TIME, NEXT_ACTIVITY
from utils.tests_utils import bpi_log_filepath


@unittest.skip("performance test not needed normally")
class TestClassPerf(TestCase):
    @staticmethod
    def get_job():
        json = dict()
        json["clustering"] = "noCluster"
        json["split"] = split_single()
        json["split"]["original_log_path"] = bpi_log_filepath
        json["method"] = "randomForest"
        json["encoding"] = EncodingContainer(BOOLEAN, prefix_length=20)
        json["type"] = "classification"
        json['label'] = LabelContainer(DURATION)
        return json

    @staticmethod
    def calculate_helper(job):
        start_time = time.time()
        calculate(job)
        print("Total for %s %s seconds" % (job['method'], time.time() - start_time))

    @staticmethod
    def calculate_helper_hyperopt(job):
        start_time = time.time()
        calculate_hyperopt(job)
        print("Total for %s %s seconds" % (job['method'], time.time() - start_time))

    def test_class_randomForest(self):
        job = self.get_job()
        add_default_config(job)
        self.calculate_helper(job)

    def ne_randomForest(self):
        job = self.get_job()
        job['label'] = LabelContainer(NEXT_ACTIVITY)
        add_default_config(job)
        self.calculate_helper(job)

    def test_class_knn(self):
        job = self.get_job()
        job['method'] = 'knn'
        add_default_config(job)
        self.calculate_helper(job)

    def test_class_decision(self):
        job = self.get_job()
        job['method'] = 'decisionTree'
        add_default_config(job)
        self.calculate_helper(job)

    def test_class_hyperopt(self):
        job = self.get_job()
        job['label'] = LabelContainer(NEXT_ACTIVITY)
        job['hyperopt'] = {'use_hyperopt': True, 'max_evals': 10, 'performance_metric': 'f1score'}
        add_default_config(job)
        self.calculate_helper_hyperopt(job)


@unittest.skip("performance test not needed normally")
class RegPerf(TestCase):
    @staticmethod
    def get_job():
        json = dict()
        json["clustering"] = "noCluster"
        json["split"] = split_single()
        json["split"]["original_log_path"] = bpi_log_filepath
        json["method"] = "randomForest"
        json["encoding"] = EncodingContainer(BOOLEAN, prefix_length=20)
        json["prefix_length"] = 20
        json["type"] = "regression"
        json["padding"] = 'no_padding'
        json['label'] = LabelContainer(REMAINING_TIME)
        return json

    @staticmethod
    def calculate_helper(job):
        start_time = time.time()
        calculate(job)
        print("Total for %s %s seconds" % (job['method'], time.time() - start_time))

    @staticmethod
    def calculate_helper_hyperopt(job):
        start_time = time.time()
        calculate_hyperopt(job)
        print("Total for %s %s seconds" % (job['method'], time.time() - start_time))

    def test_reg_randomForest(self):
        job = self.get_job()
        add_default_config(job)
        self.calculate_helper(job)

    def test_reg_linear(self):
        job = self.get_job()
        job['method'] = 'linear'
        add_default_config(job)
        self.calculate_helper(job)

    def test_reg_lasso(self):
        job = self.get_job()
        job['method'] = 'lasso'
        add_default_config(job)
        self.calculate_helper(job)

    def test_reg_hyperopt(self):
        job = self.get_job()
        job['hyperopt'] = {'use_hyperopt': True, 'max_evals': 10, 'performance_metric': 'rmse'}
        add_default_config(job)
        self.calculate_helper_hyperopt(job)
