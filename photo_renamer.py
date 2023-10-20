#!/usr/bin/python3.10
# -*- coding: utf-8 -*-

import os
from PIL import Image
import pathlib
import shutil
import random
from datetime import datetime

# Выбр профиля
# lss_linux
# lsv_windows
profile = 'lss_linux'

### НАСТРОЙКИ ###
# Настройки в зависимости от профиля
if profile == 'lss_linux':
    # Исходная директория
    inputPath = '/home/in2thevoid/Документы/git/photo_renamer/input'
    # Целевая директория
    outputPath = '/home/in2thevoid/Документы/git/photo_renamer/output/'
    # Путь для файла логирования
    logFilePath = '/home/in2thevoid/Документы/git/photo_renamer/log.txt'

if profile == 'lsv_windows':
    # Исходная директория
    inputPath = 'C:\\Users\\Admin\\Desktop\\photo_renamer\\input\\'
    # Целевая директория
    outputPath = 'C:\\Users\\Admin\\Desktop\\photo_renamer\\output\\'
    # Путь для файла логирования
    logFilePath = 'C:\\Users\\Admin\\Desktop\\photo_renamer\\log.txt'

# Общие настройки
# Сухой запуск (генерирует план действий, но не производит копирование)
dryRun = False
# Счистить целевую директорию?
cleanOutputFolder = True

# Настройки замены
noExifReplace1 = [' ','_']
noExifReplace2 = [':','.']
exifReplace1 = [' ','_']
exifReplace2 = [':','.']

# Инициализация стартовых параметров
#noExifFileCopyNumber = 0

# функция логирования и вывода
def logging(message):
    now = datetime.now()
    outputMessage = now.strftime("%d/%m/%Y %H:%M:%S") + " " + message
    print(outputMessage)
   #  logFile = open(logFilePath, "a")
    logFile.write(outputMessage + '\n')
   #  logFile.close()

# Функция получения даты создания фото из EXIF
def get_date_taken(path, extension):
    #global noExifFileCopyNumber
    try:
        exif = Image.open(path)._getexif()
        if not exif:
            # В файле не указана exif дата
            logging('У файла ' + path + ' отсутсвует EXIF дата')
            noExifFileDate = os.path.getmtime(path)
            noExifFileDt = datetime.fromtimestamp(noExifFileDate)
            noExifFileCopyNumber = 0
            initialNoExifFilename = outputPath + str(noExifFileDt) + '_NO_EXIF_DATA'
            noExifFileName = initialNoExifFilename
            logging('Предлагаемое имя ' + initialNoExifFilename + extension) 
            while True:
                # Рекурсивно проверяем, существует ли такой noexif файл
                logging('Проверяю имя:' + noExifFileName + '_('+ str(noExifFileCopyNumber) + ')' + extension)
                if os.path.isfile((noExifFileName.replace(noExifReplace1[0], noExifReplace1[1]).replace(noExifReplace2[0], noExifReplace2[1]) + '_('+ str(noExifFileCopyNumber) + ')') + extension):
                    # Файл noexif существует, переименовываем
                    logging('Файл' + noExifFileName.replace(noExifReplace1[0], noExifReplace1[1]).replace(noExifReplace2[0], noExifReplace2[1]) + '_('+ str(noExifFileCopyNumber) + ')' + extension + ' существует, генерируем новое имя')
                    noExifFileCopyNumber = noExifFileCopyNumber + 1
                    logging('Проверяю имя ' + noExifFileName.replace(noExifReplace1[0], noExifReplace1[1]).replace(noExifReplace2[0], noExifReplace2[1]) + '_('+ str(noExifFileCopyNumber) + ')' + extension)
                else:
                    # Файл noexif не существует, имя подобрано, возвращаем его
                    noExifFilenameToReturn = (str(noExifFileDt) + '_NO_EXIF_DATA_(' + str(noExifFileCopyNumber) + ')').replace(noExifReplace1[0], noExifReplace1[1]).replace(noExifReplace2[0], noExifReplace2[1])
                    logging('Имя noexif файла подобрано: ' + noExifFilenameToReturn)
                    return noExifFilenameToReturn 
                    break
        if exif:
            # Возвращаем exif дату
            return exif[36867].replace(exifReplace1[0], exifReplace1[1]).replace(exifReplace2[0], exifReplace2[1])
    except:
        # Ошибка обработки файла
        logging('Не получилось обработать ' + path)
        return 'ERROR'

# Рекурсивная функция проверки существования файла
def recursive_file_check(fileName, extension):
    fileCopyNumber = 0
    initialFileName = fileName
    while True:
        # Проверяем, существует ли такой целевой файл
        if os.path.isfile(fileName + extension):
            # Файл существует, переименовываем
            logging('Файл ' + fileName + extension + ' существует, генерируем новое имя')
            fileName = initialFileName + '_(' + str(fileCopyNumber) + ')'
            fileCopyNumber = fileCopyNumber + 1
        else:
            # Файл не существует, имя подобрано
            return fileName + extension
            break

# Инициализация лога
logFile = open(logFilePath, "w")
now = datetime.now()
logFile.write(now.strftime("%d/%m/%Y %H:%M:%S") + " Начата запись лога. Сухой запуск: " + str(dryRun) + '\n')
logFile.close()

# Открываем логфайл на дозапись
logFile = open(logFilePath, "a")

# Получаем список файлов на вход в объект inputFolder
inputFolder = pathlib.Path(inputPath)

# Очистка целевой директории
if cleanOutputFolder and not(dryRun):
    logging('Очистка целевой директории ' + outputPath)
    try:
        shutil.rmtree(outputPath)
    except:
        logging('Ошибка очистки целевой директории. Возможно, её не существует?')
    try:
        logging('Создание целевой директории ' + outputPath)
        os.mkdir(outputPath) 
    except:
        logging('Ошибка создания целевой директории')

# Цикл для файлов на вход
for inputFile in inputFolder.rglob("*"):
    fullInputFilePath = str(inputFile)
    fileExtension = pathlib.Path(fullInputFilePath).suffix
    # Проверяем, директория или файл
    if os.path.isdir(fullInputFilePath):
        # Это директория, пропускаем
        logging('Найдена директория: ' + fullInputFilePath)
    else:
        # Это файл, обрабатываем
        exifDate = (get_date_taken(fullInputFilePath, fileExtension))
        
        # Получаем новое имя
        logging('Найден файл: ' + fullInputFilePath + ' EXIF Date:' + exifDate)
        newName = recursive_file_check(outputPath + exifDate, fileExtension)
        logging('Целевое имя: ' + newName)

        # Копируем
        if not(dryRun):
            shutil.copyfile(inputFile, newName)

# Закрываем логфайл
logFile.close()