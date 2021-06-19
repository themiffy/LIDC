# LIDC-Unet


# Требования

Программа должна:
1. Поддерживать работу с DICOM файлами и обычными графическими форматами (jpeg, png, tiff).
2. Обладать достаточно высокой точностью в определении долей лёгких, для корректного расчёта накопления РФП в них.
3. Выполняться за приемлемое время (никак не больше 5ти секунд, необходимо стремиться к 1 секунде).
4. Графически отображать полученные диагностические характеристики.

# Опыт использования программы

1. Пользователь выбирает файл (файлы?) с результатами гибридного исследования.
2. После подтверждения программа выполняет алгоритмы.
3. Пользователь получает окно с результатами работы алгоритма:
   - изображение КТ;
   - маска сегмнтов;
   - совмещённое изображение ОФЭКТ/КТ;
   - текстовые поля с количеством РФП в каждом сегменте и общим количеством

![alt text](https://github.com/themiffy/LIDC-Unet/blob/main/Frame%201.png)

# Архитектура программы

Для обеспечения возможности модификации кода программы, поддержания внутреннего порядка в программе и повышения её надёжности, принято решение разделить программу на модули и функции внутри них. 

Программа должна состоять из следующих модулей: 
  - главный модуль;
  - модуль загрузки и предобработки данных;
  - модуль сегментации;
  - модуль комбинирования и обработки данных;
  - модуль вывода.

![alt text](https://github.com/themiffy/LIDC-Unet/blob/main/Frame%202.png)
Требования к архитектуре:

   1. Модули должны быть максимально независимыми.
   2. Каждый модуль должен улавливать свои ошибки и исключения и возвращать их для возможности локализации ошибки.
   3. Входные данные на каждом этапе должны быть валидированны.

# Модули подробно (wip):

...
