# LIDC-Unet

# Нарисовать структуру программы

1. Программа должна состоять из модулей: 
  - главный модуль;
  - модуль сегментации;
  - модуль комбинирования и обработки данных;
  - модуль с функциями ввода/вывода.

2. Модули должны быть максимально независимыми.
3. Необходимо обозначить ошибки и исключения.
4. Обязательная валидация данных.

# Модули подробно (wip):

...

# Опыт использования программы

1. Пользователь выбирает файл (файлы?) с результатами гибридного исследования.
2. После подтверждения программа выполняет алгоритмы.
3. Пользователь получает окно с результатами работы алгоритма:
   - изображение КТ;
   - маска сегмнтов;
   - совмещённое изображение ОФЭКТ/КТ;
   - текстовые поля с количеством РФП в каждом сегменте и общим количеством
