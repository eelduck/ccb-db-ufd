import json
from typing import List, Optional, Any

import streamlit as st
import pandas as pd
import os
from model import Classifier, Regressor, Preprocessor

# Wide mode by default
st.set_page_config(layout="wide")

# Path to program dir
program_dir = os.path.dirname(os.path.abspath(__file__))

# Constants
TASKS_PATH = 'tasks.json'
COLUMNS_PATH = 'columns.json'
OBJECTS_PATH = 'objects.json'
CLASSIFER_PATH = 'classifier.pkl'
REGRESSOR_PATH = 'regressor.pkl'
PREPROCESSOR_PATH = 'attr.csv'

TASKS_ERROR_TEXT = "Данные о проверяемых этапах отсутствуют.\nПроверьте файл 'tasks.json' и обновите страницу."
OBJECTS_ERROR_TEXT = "Данные об объектах отсутствуют.\nПроверьте файл 'objects.json' и обновите страницу."
COLUMNS_ERROR_TEXT = "Данные об проверяемых колонках.\nПроверьте файл 'columns.json' и обновите страницу."

preprocessor = Preprocessor(path_to_attr=PREPROCESSOR_PATH)
classifer = Classifier(CLASSIFER_PATH)
regressor = Regressor(REGRESSOR_PATH)

# Load dropdown menus
def load_json(path: str, program_dir: str, error_text: str) -> Any:
    with open(os.path.join(program_dir, path), 'r') as f:
        out = json.load(f)
    if out is None or not len(out):
        st.error(error_text)
    return out


tasks = load_json(TASKS_PATH, program_dir, TASKS_ERROR_TEXT)
objects = load_json(OBJECTS_PATH, program_dir, OBJECTS_ERROR_TEXT)
columns = load_json(COLUMNS_PATH, program_dir, COLUMNS_ERROR_TEXT)


def get_predictions(df: pd.DataFrame, tasks_choices: list[str], object_choices: list[str]) -> pd.DataFrame:
    out = df.loc[df['obj_key'].isin(object_choices)]
    # right.write(out)
    out = out.astype({"Кодзадачи": 'string'})
    t_choices = [c.split(" ", 1) for c in tasks_choices]
    out = out.loc[out['Кодзадачи'].isin(t_choices)]


    # step 1: Get features from dataset
    # TODO


    # step 2: Get classified model
    # TODO

    # step 3: Get predictions
    # predictions = predictor.predict(df, tasks_choices)
    # df_prediction = pd.DataFrame(data=list(zip(tasks_choices, predictions)),
    #                              columns=['Название этапа', 'Предсказание'])
    right.write(out.dtypes)
    right.write(out)

    return out


def process_selected() -> Optional[List[str]]:
    """ Обработка выбранных пользователем этапов"""
    if uploaded_file is None:
        st.error("Необходимо загрузить файл с данными")
        return
    if dataframe is None or not isinstance(dataframe, pd.DataFrame):
        st.error("Ошибка с загрузкой датасета в pd.DataFrame")
        return
    df_columns = dataframe.columns
    if not set(columns).issubset(set(df_columns)):
        st.error(f"В тестовом файле отсутствует одна из необходимых колонок")
        return
    predictions = get_predictions(dataframe, task_choices, object_choices)
    right.table(predictions)


left, right = st.columns(2)
# Боковая панель
st.sidebar.markdown('## Параметры')
# Этапы
task_choices = [f"{s['code']} {s['name']}" for s in tasks]
selected_tasks = st.sidebar.multiselect('Выберите нужный этап', task_choices)
# Объекты
object_choices = list(objects)
selected_objects = st.sidebar.multiselect('Выберите id нужного объекта', object_choices)
# Дата отчета
selected_date = st.sidebar.date_input("Введите дату отчета")
# Загрузка файла
uploaded_file = st.sidebar.file_uploader("Загрузите набор данных", type=['xlsx'])
# Получить прогноз
st.sidebar.button('Получить прогноз', on_click=process_selected)

if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    left.write(dataframe.head(5))
