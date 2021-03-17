from log_analyzer import SampleLoggerAnalyzer
import unittest
import datetime
import filecmp
import os
#Test cases to test Calulator methods
#You always create  a child class derived from unittest.TestCase
class TestSampleLoggerAnalyzer(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
    maxDiff = 2000
    def setUp(self):
        self.SampleLoggerAnalyzer = SampleLoggerAnalyzer()

    def tearDown(self):
        del self.SampleLoggerAnalyzer
    #Each test method starts with the keyword test_



    def test_process_log(self):
        """Перед тестированием необходимо очистить папку C:\\Users\\user\PycharmProjects\homework1\\reports_unit_test_process_log"""


        self.SampleLoggerAnalyzer.config = {
            "REPORT_SIZE": 1000,
            "REPORT_DIR": "./reports_unit_test_process_log",
            "LOG_DIR": "./log_unit_test_process_log",
            "LOG_NAME_TEMPLATE": "nginx-access-ui.log-[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]",
            "LOG_NAME_EXTENSION": "log-",
            "LOG_NAME_DATE_EXTENSION": "%Y%m%d",
            "REPORT_NAME_TEMPLATE": "report-[0-9][0-9][0-9][0-9].[0-1][0-9].[0-3][0-9]",
            "REPORT_NAME_DATE_EXTENSION": "%Y.%m.%d",
            "REPORT_TEMPLATE_NAME": "report.html",
            "LOGGER_FILE": "SampleLoggerAnalyzerLog.log",
            "ERROR_PERCENTAGE": 0.5

        }
        if os.path.exists(self.SampleLoggerAnalyzer.config["REPORT_DIR"]+'/'+'report-2017.06.29.html'):
            os.remove(self.SampleLoggerAnalyzer.config["REPORT_DIR"]+'/'+'report-2017.06.29.html')
        result = self.SampleLoggerAnalyzer.process_file('nginx-access-ui.log-20170629',
                                                        datetime.datetime.strptime('20170629',
                                                                                   self.SampleLoggerAnalyzer.config[
                                                                                       "LOG_NAME_DATE_EXTENSION"]))

        result_cmp = filecmp.cmp('./reports_unit_test_process_file/report-2017.06.29.html',
                                 './sample_report/report-2017.06.29.html')
        self.assertEqual(result and result_cmp, True)



    def test_init_logger(self):
        self.SampleLoggerAnalyzer.config["LOGGER_FILE"]='sample_logger'
        self.assertTrue(self.SampleLoggerAnalyzer.init_logger())



    def test_process_config_name_argv(self):
        #['C:/Users/user/PycharmProjects/homework1/log_analyzer.py']
        self.assertEqual(self.SampleLoggerAnalyzer.process_config_name_argv(
            ['C:/Users/user/PycharmProjects/homework1/log_analyzer.py','--config','test']), 'test')



    def test_find_last_log(self):
        #self.SampleLoggerAnalyzer.config["LOG_DIR"] = 'C:\\Users\\user\PycharmProjects\homework1\log_unit_test' ##Если запускать
        # через PyCharms на моей машине
        self.SampleLoggerAnalyzer.config["LOG_DIR"] = './log_unit_test' ##Если запускать через консоль
        self.SampleLoggerAnalyzer.config["LOG_NAME_TEMPLATE"] = 'nginx-access-ui.log-[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]'
        self.SampleLoggerAnalyzer.config["LOG_NAME_EXTENSION"] = 'log-'
        self.SampleLoggerAnalyzer.config["LOG_NAME_DATE_EXTENSION"] = '%Y%m%d'
        self.assertEqual(self.SampleLoggerAnalyzer.find_last_log(),
                         ('nginx-access-ui.log-20170629',datetime.datetime.strptime('20170629',
                          self.SampleLoggerAnalyzer.config["LOG_NAME_DATE_EXTENSION"] )))



    def test_check_logs_existance(self):
        self.SampleLoggerAnalyzer.config["REPORT_DIR"]='./reports_unit_test' ##Если запускать
        # через PyCharms на моей машине
        #self.SampleLoggerAnalyzer.config["REPORT_DIR"] = './reports_unit_test' ##Если запускать через консоль
        self.assertEqual(self.SampleLoggerAnalyzer.check_logs_existance('report-2018.06.30.html'), True)



    def test_process_file(self):
        """Перед тестированием необходимо очистить папку C:\\Users\\user\PycharmProjects\homework1\\reports_unit_test_process_file"""
        self.SampleLoggerAnalyzer.config = {
            "REPORT_SIZE": 1000,
            "REPORT_DIR": "./reports_unit_test_process_file",
            "LOG_DIR": "./log_unit_test_process_file",
            "LOG_NAME_TEMPLATE": "nginx-access-ui.log-[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]",
            "LOG_NAME_EXTENSION": "log-",
            "LOG_NAME_DATE_EXTENSION": "%Y%m%d",
            "REPORT_NAME_TEMPLATE": "report-[0-9][0-9][0-9][0-9].[0-1][0-9].[0-3][0-9]",
            "REPORT_NAME_DATE_EXTENSION": "%Y.%m.%d",
            "REPORT_TEMPLATE_NAME": "report.html",
            "LOGGER_FILE": "SampleLoggerAnalyzerLog.log",
            "ERROR_PERCENTAGE": 0.5

        }
        if os.path.exists(self.SampleLoggerAnalyzer.config["REPORT_DIR"]+'/'+'report-2017.06.29.html'):
            os.remove(self.SampleLoggerAnalyzer.config["REPORT_DIR"]+'/'+'report-2017.06.29.html')
        result = self.SampleLoggerAnalyzer.process_file('nginx-access-ui.log-20170629',datetime.datetime.strptime('20170629',
                          self.SampleLoggerAnalyzer.config["LOG_NAME_DATE_EXTENSION"] ))
        result_cmp=filecmp.cmp('./reports_unit_test_process_file/report-2017.06.29.html','./sample_report/report-2017.06.29.html')
        self.assertEqual(result and result_cmp, True)



    def test_process_log_line(self):
        self.SampleLoggerAnalyzer.log_stats = {}
        self.SampleLoggerAnalyzer.process_log_line('1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET'
                                                   ' /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200'
                                                   ' 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770"'
                                                   ' "-" 0.133')
        self.assertEqual(self.SampleLoggerAnalyzer.log_stats, {'/api/1/photogenic_banners/list/?server_name=WIN7RB4':
                                    {'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4',
                                     'count': 1, 'time_sum': 0.133, 'time_max': 0.133, 'times': [0.133]}})

    def test_add_url(self):
        self.SampleLoggerAnalyzer.log_stats = {}
        self.SampleLoggerAnalyzer.add_url('/api/1/photogenic_banners/list/?server_name=WIN7RB4', ['1.99.174.176',
                                           '3b81f63526fa8', '-', '[29/Jun/2017:03:50:22 +0300]',
                                            '"GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1"',
                                            '200', '12', '"-"', '"Python-urllib/2.7"', '"-"',
                                            '"1498697422-32900793-4708-9752770"', '"-"', '0.133'])

        self.assertEqual(self.SampleLoggerAnalyzer.log_stats, {'/api/1/photogenic_banners/list/?server_name=WIN7RB4':
                                                                   {
                                                                       'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4',
                                                                       'count': 1, 'time_sum': 0.133, 'time_max': 0.133,
                                                                       'times': [0.133]}})

    def test_update_url(self):

        self.SampleLoggerAnalyzer.log_stats={'/api/1/photogenic_banners/list/?server_name=WIN7RB4': {
            'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4', 'count': 1, 'time_sum': 0.133,
            'time_max': 0.133, 'times': [0.133]}}
        self.SampleLoggerAnalyzer.update_url('/api/1/photogenic_banners/list/?server_name=WIN7RB4', ['1.99.174.176',
                                           '3b81f63526fa8', '-', '[29/Jun/2017:03:50:22 +0300]',
                                            '"GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1"',
                                            '200', '12', '"-"', '"Python-urllib/2.7"', '"-"',
                                            '"1498697422-32900793-4708-9752770"', '"-"', '0.133'])
        self.assertEqual(self.SampleLoggerAnalyzer.log_stats, {'/api/1/photogenic_banners/list/?server_name=WIN7RB4':
            {
                    'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4',
                    'count': 2, 'time_sum': 0.266,
                    'time_max': 0.133, 'times': [0.133, 0.133]}})

    def test_form_report(self):
        self.SampleLoggerAnalyzer.config = {
            "REPORT_SIZE": 1000,
            "REPORT_DIR": "./sample_report",
            "LOG_DIR": "./sample_report",
            "LOG_NAME_TEMPLATE": "nginx-access-ui.log-[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]",
            "LOG_NAME_EXTENSION": "log-",
            "LOG_NAME_DATE_EXTENSION": "%Y%m%d",
            "REPORT_NAME_TEMPLATE": "report-[0-9][0-9][0-9][0-9].[0-1][0-9].[0-3][0-9]",
            "REPORT_NAME_DATE_EXTENSION": "%Y.%m.%d",
            "REPORT_TEMPLATE_NAME": "report.html",
            "LOGGER_FILE": "SampleLoggerAnalyzerLog.log",
            "ERROR_PERCENTAGE": 1

        }
        self.SampleLoggerAnalyzer.lines_counter = 5
        self.SampleLoggerAnalyzer.form_report("testing.html", [
            {"url": "/api/v2/internal/html5/phantomjs/queue/?wait=1m", "count": 97, "time_sum": 5828.255000000002,
             "time_max": 60.414, "count_perc": 0.001, "time_perc": 0.089, "time_avg": 60.085, "time_med": 60.078},
            {"url": "/api/v2/internal/gpmd_plan_report/queue/?wait=1m&worker=5", "count": 49, "time_sum": 2948.896,
             "time_max": 60.46, "count_perc": 0.001, "time_perc": 0.045, "time_avg": 60.182, "time_med": 60.17},
            {"url": "/api/v2/internal/gpmd_plan_report/queue/?wait=1m&worker=2", "count": 49,
             "time_sum": 2947.8660000000004, "time_max": 60.316, "count_perc": 0.001, "time_perc": 0.045,
             "time_avg": 60.161, "time_med": 60.152},
            {"url": "/api/v2/internal/gpmd_plan_report/queue/?wait=1m&worker=4", "count": 49,
             "time_sum": 2947.7260000000006, "time_max": 60.432, "count_perc": 0.001, "time_perc": 0.045,
             "time_avg": 60.158, "time_med": 60.138},
            {"url": "/api/v2/internal/gpmd_plan_report/queue/?wait=1m&worker=1", "count": 49,
             "time_sum": 2947.2000000000003, "time_max": 60.27, "count_perc": 0.001, "time_perc": 0.045,
             "time_avg": 60.147, "time_med": 60.13}])
        result_cmp = filecmp.cmp('./sample_report/testing.html',
                                 './sample_report/report_test.html')
        self.assertTrue(result_cmp)



    def test_calculate_relative_values(self):
        self.SampleLoggerAnalyzer.lines_counter=10
        self.SampleLoggerAnalyzer.request_time_sum=5
        self.assertEqual(
            self.SampleLoggerAnalyzer.calculate_relative_values(('/api/1/photogenic_banners/list/?server_name=WIN7RB4',
                                                                 {
                                                                     'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4',
                                                                     'count': 2, 'time_sum': 0.266,
                                                                     'time_max': 0.133, 'times': [0.133, 0.133]})),
            {'url': '/api/1/photogenic_banners/list/?server_name=WIN7RB4', 'count': 2, 'time_sum': 0.266,
             'time_max': 0.133, 'count_perc': 0.2, 'time_perc': 0.053, 'time_avg': 0.133, 'time_med': 0.133})

    
    def test_copy_config(self):
        self.SampleLoggerAnalyzer.copy_config('sample_logger_unit_test.ini')
        self.assertEqual(self.SampleLoggerAnalyzer.config,
                 {'REPORT_SIZE': '1', 'REPORT_DIR': '2', 'LOG_DIR': '3', 'LOG_NAME_TEMPLATE': '4',
                  'LOG_NAME_EXTENSION': '5', 'LOG_NAME_DATE_EXTENSION': '6', 'REPORT_NAME_TEMPLATE': '7',
                  'REPORT_NAME_DATE_EXTENSION': '8', 'REPORT_TEMPLATE_NAME': '9', 'LOGGER_FILE': '10',
                  'ERROR_PERCENTAGE': '11'}
                 )

# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()