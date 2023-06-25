from copy import deepcopy

import pandas as pd
import numpy as np
import pickle
from lightautoml.automl.presets.tabular_presets import TabularAutoML


# hello
class Preprocessor:
    def __init__(self, path_to_attr: str):
        self.attr = pd.read_csv(path_to_attr,
                                sep=';',
                                parse_dates=['date_report'],
                                index_col=0) \
            .rename(columns={'Код ДС': 'obj_key'})

    def add_features(self, df):

        data = deepcopy(df)
        for col in ["ДатаНачалаЗадачи", "ДатаОкончанияЗадачи", "ДатаначалаБП0", "ДатаокончанияБП0", "date_report"]:
            data[col] = pd.to_datetime(data[col])

        data = pd.merge(data, self.attr, on=['obj_key', 'date_report'], how='left')
        data = data.dropna(subset=['Кодзадачи'])
        data["Статуспоэкспертизе"] = data["Статуспоэкспертизе"].fillna(0)
        data["состояние площадки"] = data["состояние площадки"].fillna("Свободна, передана")
        data["НазваниеЗадачи"] = data["НазваниеЗадачи"].fillna("unknow")
        data["Экспертиза"] = data["Экспертиза"].fillna("unknow")
        data["diff_start"] = (((data["ДатаначалаБП0"] - data["ДатаНачалаЗадачи"]).dt.days).fillna(0)).astype(np.int32)
        data["diff_end"] = (((data["ДатаокончанияБП0"] - data["ДатаОкончанияЗадачи"]).dt.days).fillna(0)).astype(np.int32)
        data["early_start"] = (data["diff_start"] > 0).astype(np.uint8)
        data["start_on_time"] = (data["diff_start"] == 0).astype(np.uint8)
        data["late_end"] = (data["diff_end"] < 0).astype(np.uint8)
        data["end_on_time"] = (data["diff_end"] == 0).astype(np.uint8)
        data["is_known_Генпроектировщик"] = data["Генпроектировщик"].isna().astype(np.uint8)
        data["is_known_Генподрядчик"] = data["Генподрядчик"].isna().astype(np.uint8)
        data["is_known_Площадь"] = data["Площадь"].isna().astype(np.uint8)
        data["encoded_amount_Площадь"] = np.digitize(
            data["Площадь"],
            bins=[
                data["Площадь"].quantile(q)
                for q in np.arange(0.0, 1.0, 0.1)
            ]
        )
        data["is_known_Кол-во рабочих"] = data["Кол-во рабочих"].isna().astype(np.uint8)
        data["encoded_amount_Кол-во рабочих"] = np.digitize(
            data["Кол-во рабочих"],
            bins=[
                data["Кол-во рабочих"].quantile(q)
                for q in np.arange(0.0, 1.0, 0.1)
            ]
        )
        # data = pd.get_dummies(data=data, columns=["состояние площадки"], drop_first=True, dtype=np.uint8)
        data["specific_area1"] = data["Площадь"] / data["Кол-во рабочих"]
        data.loc[data['specific_area1'] == np.inf, 'specific_area1'] = 0.0
        data["specific_area2"] = data["Площадь"] / data["Генподрядчик"]
        data.loc[data['specific_area2'] == np.inf, 'specific_area2'] = 0.0

        data["speed1"] = 100 / (data["ДатаокончанияБП0"] - data["ДатаначалаБП0"]).dt.days.fillna(0)
        data["speed2"] = 100 / (data["ДатаОкончанияЗадачи"] - data["ДатаНачалаЗадачи"]).dt.days.fillna(0)
        data["spped3"] = data["ПроцентЗавершенияЗадачи"] / (data["date_report"] - data["ДатаНачалаЗадачи"]).dt.days.fillna(0)
        data["reserve"] = (data["ДатаОкончанияЗадачи"] - data["date_report"]).dt.days
        data["no_reserve"] = (data["reserve"] < 0).astype(np.int8)

        data["time_task_plan"] = (((data["ДатаокончанияБП0"] - data["ДатаначалаБП0"]).dt.days).fillna(0)).astype('int')
        data["time_task_fact"] = (((data["ДатаОкончанияЗадачи"] - data["ДатаНачалаЗадачи"]).dt.days).fillna(0)).astype('int')
        data["diff_time_plan_fact"] = data["time_task_fact"] - data["time_task_plan"]

        # Считаем средние значения плана по контракту и сравниваем каждое значение со средним (в срезе по этопу)
        avg_time_task_plan = data.groupby(["Кодзадачи", "НазваниеЗадачи"])["time_task_plan"].mean().reset_index().rename(columns={"time_task_plan": "avg_time_task_plan"})
        data = data.merge(avg_time_task_plan[["Кодзадачи", "НазваниеЗадачи", "avg_time_task_plan"]], how='left', on=["Кодзадачи", "НазваниеЗадачи"])
        data["diff_avg_time_plan"] = data["time_task_plan"] - data["avg_time_task_plan"]

        # Считаем средние значения факта по контракту и сравниваем каждое значение со средним (в срезе по этопу)
        avg_time_task_fact = data.groupby(["Кодзадачи", "НазваниеЗадачи"])["time_task_fact"].mean().reset_index().rename(columns={"time_task_fact": "avg_time_task_fact"})
        data = data.merge(avg_time_task_fact, how='left', on=["Кодзадачи", "НазваниеЗадачи"])
        data["diff_avg_time_fact"] = data["time_task_fact"] - data["avg_time_task_fact"]


        # Считаем средние значения факта по контракту и сравниваем каждое значение со средним (в срезе по этопу)
        avg_time_task_fact = data.groupby(["Кодзадачи", "НазваниеЗадачи"])["diff_time_plan_fact"].mean().reset_index().rename(columns={"diff_time_plan_fact": "avg_diff_time_plan_fact"})
        data = data.merge(avg_time_task_fact, how='left', on=["Кодзадачи", "НазваниеЗадачи"])
        data["diff_avg_time_plan_fact"] = data["diff_time_plan_fact"] - data["avg_diff_time_plan_fact"]

        # Удаляем временые колонки
        data = data.drop(columns=['time_task_plan', 'time_task_fact' ,'avg_time_task_fact', 'avg_time_task_plan', 'diff_time_plan_fact', 'avg_diff_time_plan_fact'])
        return data


class Classifier:
    def __init__(self, path: str, threshold: float = 0.01):
        self.threshold = threshold

        with open(path, 'rb') as handle:
            self.model = pickle.load(handle)

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        pred_test_reg = self.model.predict(df).data[:,0]
        pred_test_reg = (pred_test_reg > self.threshold).astype(int)
        return pred_test_reg


class Regressor:
    def __init__(self, path: str):
        with open(path, 'rb') as handle:
            self.model = pickle.load(handle)

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        pred_test_reg = self.model.predict(df).data.astype(int)
        return pred_test_reg
