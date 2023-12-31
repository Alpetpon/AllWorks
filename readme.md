# Описание проекта

Данный проект представляет собой телеграм-бота на Python, использующего библиотеку aiogram для обработки сообщений и команд от пользователей. Бот реализует в себе помощника по поиску работы на базе разных билиотек  и включает следующие модули:

- main.py: Точка входа, содержит код для запуска бота и инициализации всех остальных модулей.
- config.py: Файл с конфигурационными параметрами, такими как токен бота.
- text.py: Модуль с текстами, используемыми ботом. Содержит приветствия, сообщения об ошибках и другие текстовые данные для бота. 
- kb.py: Модуль с клавиатурами, используемыми ботом. Содержит все статические и динамически генерируемые клавиатуры через функции.
- utils.py: Модуль с различными функциями. Содержит функции для рассылки, генерации резюме и изображений через API и другие полезные функции.
- handlers.py: Основной модуль с функциями-обработчиками с декораторами (фильтрами) для обработки команд и сообщений от пользователей.
- set_meny.py: Модуль отвечающий за меню в боте
- lexicon_ru: Модуль отвечающий за конфигурацию языка в боте
- requriments.txt: Модуль для хранения используемых библиотек и их версий

# Информация о боте 

- Назавание: AllWorks 
- user name: @@AllWorksOfficial_Bot
- Ссылка на бота: t.me/AllWorksOfficial_Bot

# Инфрмация по разработке 

- Для разработки бдуем использовать библиотеки из файла requirements.txt + новые  и стабильные версии  необходимых библиотек
- При разработке используем версию Python 3.10 и выше, чтобы не было конфликтов в коде 

Для запуска бота необходимо установить необходимые библиотеки, выполнив следующую команду:
```
pip install -r requirements.txt
```

Then, you need to create a file called `config.py` and add the following code:

Можем запустить бота, выполнив следующую команду:
```
python main.py
```

Теперь бот будет запущен, и вы сможете начать использовать его, отправляя ему сообщения или команды.


