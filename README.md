# ccb-db-ufd
Репозиторий команды **Click Clack Boom** на хакатоне **Цифровой прорыв. Сезон ИИ. УФО**

## Описание задачи
TODO

## Начало работы
### Подготовка окружения
- Устанавливаем `python 3.10-dev`
    - Windows

        Устанавливаем через [официальный установщик](https://www.python.org/downloads/)

    - Linux

        ```bash
        sudo apt install python3.10-dev
        ```

- Устанавливаем `make`
    - Windows:

        Устанавливаем [chocolatey](https://chocolatey.org/install) и устанавливаем `make` с помощью команды:

        ```powershell
        choco install make
        ```

    - Linux:

        ```bash
        sudo apt install build-essential
        ```

- Устанавливаем [poetry](https://python-poetry.org/docs/#installation)
    - Windows

        Используйте [официальные инструкции](https://python-poetry.org/docs/#windows-powershell-install-instructions) или команду `powershell`

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
- Устанавливаем Docker Engine и Docker Compose согласно официальной инструкции для вашей платформы:
  - [Docker Engine](https://docs.docker.com/engine/install/)
  - [Docker Compose](https://docs.docker.com/compose/install/)
## Запуск системы
- Для запуска системы введите команду
    ```bash
    make docker-start
    ```
  После этого у вас соберется докер образ и запустится контейнер, на котором запущен Streamlit. 
  Попасть на него можно по адресу http://localhost:5000/