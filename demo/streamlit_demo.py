import json
from typing import List, Optional, Any

import streamlit as st
import pandas as pd
import numpy as np
import os
from model import Classifier, Regressor, Preprocessor

# Wide mode by default
st.set_page_config(layout="wide")

# Path to program dir
program_dir = os.path.dirname(os.path.abspath(__file__))

# Constants
TARGET_NAME = 'Кол-во дней'

RESULT_PATH = 'result.xlsx'
TASKS_PATH = 'tasks.json'
COLUMNS_PATH = 'columns.json'
OBJECTS_PATH = 'objects.json'
CLASSIFER_PATH = 'classifier.pkl'
REGRESSOR_PATH = 'regressor.pkl'
PREPROCESSOR_PATH = 'attr.csv'

N_HEAD_RECORDS = 20


TASKS_ERROR_TEXT = "Данные о проверяемых этапах отсутствуют.\nПроверьте файл 'tasks.json' и обновите страницу."
OBJECTS_ERROR_TEXT = "Данные об объектах отсутствуют.\nПроверьте файл 'objects.json' и обновите страницу."
COLUMNS_ERROR_TEXT = "Данные об проверяемых колонках.\nПроверьте файл 'columns.json' и обновите страницу."

TITLE_TEXT = "Модель прогнозирования сдвига сроков сдачи"

preprocessor = Preprocessor(path_to_attr=os.path.join(program_dir, PREPROCESSOR_PATH))
classifer = Classifier(os.path.join(program_dir, CLASSIFER_PATH))
regressor = Regressor(os.path.join(program_dir, REGRESSOR_PATH))


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


def get_predictions(df: pd.DataFrame,
                    t_selected: List[str],
                    o_selected: List[str]) -> pd.DataFrame:
    if not len(t_selected):
        t_selected = task_choices
    if not len(o_selected):
        o_selected = object_choices
    df = df.astype({'Кодзадачи': 'string'})

    # left.write(t_selected)
    # left.write(o_selected)

    # Фильтр по запросу пользователя
    filtered = df.loc[df['obj_key'].isin(o_selected)]
    # left.write(filtered)
    # left.write(df.dtypes)

    filtered = filtered.astype({"Кодзадачи": 'string'})
    t_choices = [c.split(" ", 1)[0] for c in t_selected]
    # left.write(t_choices)
    filtered = filtered.loc[filtered['Кодзадачи'].isin(t_choices)]
    # left.write(filtered)

    # step 1: Get features from dataset
    # TODO
    features = preprocessor.add_features(filtered)

    # left.write(features)

    # step 2: Get classified model
    # TODO
    classified = classifer.predict(features)
    features['pred_prev'] = classified
    #
    # left.write(classified)
    # left.write(features)

    # step 3: Get regression predictions
    regressed = regressor.predict(features)
    filtered[TARGET_NAME] = regressed
    index_changed = classified == 0
    # left.write(index_changed.shape)
    # left.write(np.arange(len(index_changed))[index_changed])
    # index_changed = np.where(classified == 0)[0]

    if sum(index_changed) != 0:
        filtered.loc[filtered[classified == 0].index.values, TARGET_NAME] = 0

    return filtered


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
    dataframe['date_report'] = selected_date

    predictions = get_predictions(dataframe, selected_tasks, selected_objects)

    save_path = os.path.join(program_dir, RESULT_PATH)
    predictions.to_excel(save_path)
    right.write(predictions.head(N_HEAD_RECORDS))

    with open(save_path, 'rb') as file:
        btn = right.download_button(
            label="Скачать результат",
            data=file,
            file_name=RESULT_PATH,
        )


    return predictions

st.markdown('<h1 style="text-align: center;">Модель прогнозирования сдвига сроков сдачи критических этапов капитального строительства</h1>', unsafe_allow_html=True)
left, right = st.columns(2)

left.markdown('<h2 style="text-align: center;">Загруженные данные</h2>', unsafe_allow_html=True)
right.markdown('<h2 style="text-align: center;">Предсказанные данные</h2>', unsafe_allow_html=True)
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
st.sidebar.markdown('## Как использовать:')
st.sidebar.markdown('1. Выберите файл для загрузки.')
st.sidebar.markdown('2. Дождитесь, пока таблица загрузится полностью: загруженные данные станут яркими, фигура человека сверху справа закончит бежать.')
st.sidebar.markdown('3. Пока идет загрузка, вы можете выбрать параметры фильтрации: 1 или несколько. Для того, чтобы выбрать все варианты, оставьте фильтр пустым.')
st.sidebar.markdown('4. Нажмите на кнопку `Получить прогноз`.')
st.sidebar.markdown('5. Дождитесь полного предсказания модели: фигура человека в правом верхнем углу закончит бежать.')
st.sidebar.markdown('6. Нажмите на кнопку `Скачать результат`.')

if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    left.write(dataframe.head(N_HEAD_RECORDS))
