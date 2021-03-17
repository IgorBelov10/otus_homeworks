#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';


from pathlib import Path
import os
import datetime
import configparser
import sys
import getopt
import gzip
import re
import statistics
import json
import logging
from pathlib import Path
from string import Template


class SampleLoggerAnalyzer:

    validation_list = sorted(['report_size', 'report_dir', 'log_dir', 'log_name_template', 'log_name_extension',
                              'log_name_date_extension'])
    config = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
        "LOG_NAME_TEMPLATE": "nginx-access-ui.log-[0-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]",
        "LOG_NAME_EXTENSION": "log-",
        "LOG_NAME_DATE_EXTENSION": "%Y%m%d",
        "REPORT_NAME_TEMPLATE": "report-[0-9][0-9][0-9][0-9].[0-1][0-9].[0-3][0-9]",
        "REPORT_NAME_DATE_EXTENSION": "%Y.%m.%d",
        "REPORT_TEMPLATE_NAME": "report.html",
        "LOGGER_FILE": "SampleLoggerAnalyzerLog.log",
        "ERROR_PERCENTAGE": 0.5

    }
    log_stats = {}
    error_counter = 0
    lines_counter = 0
    request_time_sum = 0
    log_proceeded_flag = False

    class TemplateClone(Template):
        delimiter = '$table_'

    def __init__(self, config_file_path_arg=None):

        try:
            self.init_logger()
            self.log_proceeded_flag = self.copy_config(self.process_config_name_argv(config_file_path_arg))
            return
        except BaseException:
            logging.error("Exception occurred in __init__", exc_info=True)
            return

    def process_log(self):
        try:

            last_log = self.find_last_log()
            if last_log is not None:
                logging.info(f"Start processing file{last_log[0]}")
                return self.process_file(last_log[0], last_log[1])
        except BaseException:
            logging.error("Exception occurred in process_log", exc_info=True)
            return False

    def init_logger(self):
        try:

            logging.basicConfig(filename=self.config["LOGGER_FILE"], filemode='a',
                                format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S',
                                level=logging.INFO)
            return True
        except BaseException:
            logging.basicConfig(filemode='a',
                                format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S',
                                level=logging.INFO)
            return False

        return

    @staticmethod
    def process_config_name_argv(full_cmd_arguments):
        if full_cmd_arguments is None:
            return None
        argument_list = full_cmd_arguments[1:]
        short_options = ["c:"]
        long_options = ["config="]
        try:
            arguments, values = getopt.getopt(argument_list, short_options, long_options)
            if arguments == []:
                return None
            for current_argument, current_value in arguments:
                return current_value
        except getopt.error as err:
            # Output error, and return with an error code
            logging.exception(str(err))


        return False

    def find_last_log(self):

        logs = {}
        for i in list(f for f in os.listdir(self.config["LOG_DIR"]) if
                      re.search(rf'^{self.config["LOG_NAME_TEMPLATE"]}\.gz$', f) or
                      re.search(rf'^{self.config["LOG_NAME_TEMPLATE"]}$', f)):
            logs[str(i)] = \
                datetime.datetime.strptime(str(i).split('.' + self.config["LOG_NAME_EXTENSION"])[1].split('.')[0],
                                           self.config["LOG_NAME_DATE_EXTENSION"])

        try:
            proceeded_log = max(logs)
        except ValueError:
            logging.error("Логов по данному шаблону не найдено")
            return None

        return proceeded_log, logs[proceeded_log]

    def check_logs_existance(self, report_name):
        """Проверка существования раннее сформированного отчета"""

        if len(list(f for f in os.listdir(self.config["REPORT_DIR"]) if re.search(rf'^{report_name}$', f))) == 0:
            return False
        else:
            return True

    def process_file(self, log_filename, log_time):
        """парсинг файла"""
        try:

            self.error_counter = 0
            self.lines_counter = 0
            self.log_stats = {}
            
            report_name = "report-"+log_time.strftime(self.config["REPORT_NAME_DATE_EXTENSION"]+".html")
            if self.check_logs_existance(report_name):
                logging.info(f"отчет {report_name} уже сформирован.")
                return True
            file = gzip.open(self.config["LOG_DIR"]+'/'+log_filename, mode='rt') if log_filename[-2:] == "gz" \
                else open(self.config["LOG_DIR"]+'/'+log_filename, "rt")


            for log_line in file:
                self.lines_counter += 1
                self.process_log_line(log_line)
                if self.lines_counter % 100000 == 0:
                    logging.info(f"Proceeded {self.lines_counter} lines.")
            #[i for i in self.readlines_file(file)]##изначально код был напиан без использования генератора
            # по сути прикручен генератор герирующий бесполезный лист, но зато сможем читать файл любой длины.
            # К сожалению лекция просмотрена слишком поздно:( Таким образом можн оприкрутить генератор

            file.close()
            self.form_report(report_name, self.form_log_stats_json())
            return True
        except BaseException:
            logging.error("Exception occurred while processing file", exc_info=True)
            return False

    def readlines_file(self,file):
        for log_line in file:

            self.lines_counter += 1
            if self.lines_counter % 100000 == 0:
                logging.info(f"Proceeded {self.lines_counter} lines.")
            yield self.process_log_line(log_line)

    def process_log_line(self, log_line):
        """Обработка одной строки лога"""
        try:
            log_line_list = list(re.findall(r'("[^"]*"|\[[^]]*\]|^\S+|\S+$|[\S]+)', log_line))
            url = log_line_list[4].split(" ")[1]

            if url in self.log_stats:
                 self.update_url(url, log_line_list)

            else:
                 self.add_url(url, log_line_list)
            self.request_time_sum += float(log_line_list[12])
        except BaseException:
            self.error_counter += 1
        return

    def add_url(self, url, log_line_list):
        """Добавление обработанной строки в словарь"""
        self.log_stats[url] = {"url": url, "count": 1, "time_sum": round(float(log_line_list[12]), 3),
                               "time_max": round(float(log_line_list[12]), 3),
                               "times": [round(float(log_line_list[12]), 3)]}
        return

    def update_url(self, url, log_line_list):
        """обновление обработанной строки в словаре"""
        self.log_stats[url]["count"] += 1
        self.log_stats[url]["time_sum"] += round(float(log_line_list[12]), 3)
        if self.log_stats[url]["time_max"] < float(log_line_list[12]):
            self.log_stats[url]["time_max"] = round(float(log_line_list[12]), 3)
        self.log_stats[url]["times"].append(round(float(log_line_list[12]), 3))
        return

    def form_log_stats_json(self):
        return json.dumps(list(map(
            self.calculate_relative_values, sorted(self.log_stats.items(), key=lambda x: x[1]['time_sum'], reverse=True)
            [:self.config["REPORT_SIZE"]])))

    def form_report(self, report_name, json_string):

        st_file = open(self.config["REPORT_TEMPLATE_NAME"], "rt")
        st = st_file.read()
        report_tpl = self.TemplateClone(st)
        st_file.close()
        error_percentage = round(self.error_counter/self.lines_counter, 3)
        logging.info(f'Error percentage:{error_percentage}')
        try:
            if error_percentage > self.config["ERROR_PERCENTAGE"]:
                raise BaseException

            with open(self.config['REPORT_DIR']+'/'+report_name, 'w') as file:
                file.write(report_tpl.substitute(json=str(json_string)))
            file.close()
        except BaseException:
            logging.error(f'Процент ошибочно обработанных строк:{error_percentage}. Выход из программы', exc_info=True)
        return

    def calculate_relative_values(self, log_stats_item):

        log_stats_item[1]["count_perc"] = round(log_stats_item[1]["count"]/self.lines_counter, 3)
        log_stats_item[1]["time_perc"] = round(log_stats_item[1]["time_sum"]/self.request_time_sum, 3)
        log_stats_item[1]["time_avg"] = round(log_stats_item[1]["time_sum"]/log_stats_item[1]["count"], 3)
        log_stats_item[1]["time_med"] = statistics.median(log_stats_item[1]["times"])
        log_stats_item[1].pop("times")
        return log_stats_item[1]

    def copy_config(self, config_file_path):
        """копирования параметров из указанного конфига"""
        if config_file_path is None:
            return True

        try:
            if config_file_path is False:
                raise BaseException
            config = configparser.ConfigParser()
            config.read(config_file_path)
            for i in config['SETTINGS'].keys():
                self.config[str.upper(i)] = config['SETTINGS'][i]
            return True
        except BaseException:
            logging.error("Копирование из конфигурационного файла не пройдено успешно", exc_info=True)
            return False



def process_log(argv):

    logger_cur = SampleLoggerAnalyzer(config_file_path_arg=argv)
    if logger_cur.log_proceeded_flag:
        if logger_cur.process_log():
            print("Последний лог успешно обработан")
        else:
            print("Последний лог обработать не удалось. Подробности в лог файле.")
    else:
        print("Конфигурационный файл не был обработан корректно.")



def main():



    process_log(sys.argv)

    pass


if __name__ == "__main__":
    main()
