# ccb-db-ufd

Репозиторий команды **Click Clack Boom** на хакатоне **Цифровой прорыв. Сезон ИИ. УФО**

## Описание задачи

Интеграция ИИ и ML алгоритмов на
цифровую площадку строительства. С
помощью искусственного интеллекта
отслеживание хода выполнения
календарно-сетевого графика ОКС на всех
этапах жизненного цикла проекта, а также
предсказательный анализ варианта
развития событий при наступлении предполагаемых рисков.

## Содержание репозитория

- В папке `./demo/` содержится код запуска демонстрации проекта.
- Файлы модели содержатся на гугл
  диске [ [ссылка](https://drive.google.com/drive/folders/1Lus6H4BIwl84cLMAkCFTg979xBv1Y5K9?usp=sharing) ].
  При сборке docker контейнера веса автоматически подгружаются.
- Резлультаты по тестовому датасету:
    - В файле `Тест_with_result.xlsx` содержится результаты предсказания по критическим
      этапам строительства
    - В файле `Тест_with_result_full.xlsx` содержатся результаты предсказания по всем
      этапам строительства
- Есть docker файл `Dockerfile` для локального запуска приложения через docker
- Есть docker-comspose файл `docker-compose.yaml` для локального запуска приложения через
  docker-compose
- В файле `requirements.txt` необходимые зависимости
- В папке `./notebooks/` содержится jupyter ноутбук с анализом данных, тестами предположений и кодом обучения моделей


## Начало работы

### Подготовка окружения

- Устанавливаем `python 3.8`
    - Windows

      Устанавливаем через [официальный установщик](https://www.python.org/downloads/)

    - Linux

        ```bash
        sudo apt install python3.8
        ```

- Устанавливаем `make`
    - Windows:

      Устанавливаем [chocolatey](https://chocolatey.org/install) и устанавливаем `make` с
      помощью команды:

        ```powershell
        choco install make
        ```

    - Linux:

        ```bash
        sudo apt install build-essential
        ```

- Устанавливаем [poetry](https://python-poetry.org/docs/#installation)
    - Windows

      Используйте [официальные инструкции](https://python-poetry.org/docs/#windows-powershell-install-instructions)
      или команду `powershell`

        ```powershell
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
        ```

    - Linux

        ```bash
        make poetry-download
        ```
- Устанавливаем требуемые пакеты с помощью команды
    ```bash
    make poetry-install
    ```
- Устанавливаем Docker Engine и Docker Compose согласно официальной инструкции для вашей
  платформы:
    - [Docker Engine](https://docs.docker.com/engine/install/)
    - [Docker Compose](https://docs.docker.com/compose/install/)

## Запуск системы

- Для запуска системы введите команду
    ```bash
    make docker-start
    ```
  После этого у вас соберется докер образ и запустится контейнер, на котором запущен
  Streamlit.
  Попасть на него можно по адресу http://localhost:5000/