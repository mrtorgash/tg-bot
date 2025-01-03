# Телеграм-бот для проведения анкетирования

Этот бот предназначен для проведения анкетирования среди **ограниченного списка пользователей** в Telegram. Собранные ответы сохраняются в файл формата CSV для дальнейшего анализа.

## Функционал

*   **Авторизация пользователей:** Бот проверяет, входит ли пользователь в список разрешенных для прохождения анкетирования.
*   **Проведение анкеты:** Пользователь отвечает на последовательность вопросов, которые заранее заданы в коде бота.
*   **Сохранение ответов:** Ответы каждого пользователя сохраняются в CSV файл.
*   **Простота использования:** Бот интуитивно понятен и не требует сложных команд.

## Как использовать

1.  **Настройка:**
    *   Установите необходимые библиотеки(requiments.txt).
    *   Заполните список авторизованных пользователей в коде бота.
    *   Отредактируйте вопросы анкеты в коде.
    *   Укажите путь к файлу для сохранения ответов CSV (иначе все будет в дирректории проекта).
    *   Замените `<TOKEN>` на токен вашего бота.
2.  **Запуск:**
    *   Запустите скрипт Python (`python main.py`).
3.  **Работа с ботом:**
    *   Откройте Telegram и найдите вашего бота.
    *   Запустите бота командой `/start`.
    *   Следуйте инструкциям бота, отвечая на вопросы анкеты.
4.  **Результаты:**
    *   После прохождения анкеты, ответы будут сохранены в CSV файл, который вы указали в настройках.

## Комментарии
Бот которого я разработал с целью шутки. 

Идеи для развития.
1. **Поменять формат хранения файлов**
2. **Равзернуть бота на сервере**
3. **Улучшить систему логгирования**
4. **Создать .env file**
