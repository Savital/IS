# Information Security

Лабораторные работы:

* lab1 Привязка к характеристикам компьютера (лицензирование);
* lab2 Создание модели Энигмы;
* lab3 Шифрование с открытым ключом;
* lab4 Шифрование с симметричным ключом;
* lab5 Создание электронной подписи;
* lab6 Сжатие данных.

##Лабораторная работа 1

###ТЗ: 

* Защитить программу от неавторизованного доступа, используя проверку по CPUID.
* Две части:
    * Инсталлер, который вычисляет лицензию
    * Программа, в которой содержится проверка суммы
* Инсталлер генерирует файл лицензии основанный на md5 хэше из /proc/cpuinfo, который дожен быть расположен в той же дирректории, что и программа
* Программа генерирует текущий cpuinfo md5 хэш и сравнивает с тем, который в файле.

###Защита:

####Порядок внедрения средств защиты
 * аналитическое обследование автоматизированных систем, которые планируется защищать
    * выявить уровни конфиденциальности информации (что)
    * установить уровни полномочий (кто)
    * установить правила разграничения доступа (как)
    * создание модели нарушителя
 * проектирование системы защиты информации
    * выбор методов
    * оформление документации
 * создание системы
    * тестирование
    * ...
 * прием в эксплуатацию
 * эксплуатация
 * развитие

####Защита ПО от "несанкционированного" копирования (категории)
#####1. Внутренняя самозащита.
 * пассивные:
    * парольные замки
    * ограничения по времени использования, по дате
    * наблюдение
 * активные:
    * искажение программы
    * "вирусы" (в хорошем смысле)
#####2. Видимая самозащита.
 * активные:
    * различные сигналы
    * информация о владельце
#####3. Идентификация.
 * корреляционный и частотный анализ
 * различные виды избыточности и внедренных ошибок
#####4. Информационные средства
 * пассивные:
    * водяные знаки на лицензии, голографические наклейки
    * реестр ПО
#####5. составляющие систем
 * изменение формата записи
 * специальные методы разметки (дискета со специальным размером кластера или поврежденным сектором)
 * уникальные метки
#####6. специальная аппаратура
 * использование данных процессора
 * использование серийных номеров
 * аппаратные средства защиты: токены и электронные ключи
#####7. изменение функций
 * перегрузка прерываний
 * переименование дисков
#####8. запрос дополнительной информации
 * пароль
 * персональные данные
#####9. шифрование
 * симметричное
 * с открытым ключом
#####10. проверка сигнатур
 * характеристики ПК
 * каталоги / реестр
 * привязка к уникальному электронному ключу
#####11. защита от автоматизированного подбора
 * ограничение числа попыток
 * капча
 * монитор активности
 
Как своеобразный способ можно упомянуть также документирование.

####Параметры

Можно выделить два типа средств (параметров): 
 * постоянные 
 * переменные 
 
Постоянные параметры: почти всегда аппаратные средства.

Критерии оценки при выборе параметров:
 * уникальность
 * неизменность
 * доступность
 
####Методы:
 * Самый легкообходимый метод - использование Get*** в WinApi. GetWindowsDirection ... GetCurrentHWProfile
 * Windows Management Instrumentation. Используется язык запросов WQL: Select * From Win32_Bios
 * В случае линуксов: привязка к /proc, например /proc/cpuinfo
 * В случае маков придётся использовать sysctl -a hw

-------------------------------------------------------------

## Лабораторная работа 2

###ТЗ:

* Создать электронный аналог Энигмы
* 3 ротора и рефлектор. 
    * Если Reflect(A)=B, то Reflect(B)=A. 
    * Одна машина используется и для шифрования и для расшифровки. 
    * Ключом является положение трёх роторов.
    * Чтобы использовать многоалфавитность, роторы нужно поворачивать. 
    * Вначале проворачивается первый ротор, спустя 256 символов аски - поворачивается второй, и снова начинает поворачиваться первый...
* Цель - продемонстрировать на трёх произвольных файлах: пустом, однобайтовом, и .ехе/архиве/пдфке

###Защита:

-------------------------------------------------------------

## Лабораторная работа 3

###ТЗ:

* Разработать ...

-------------------------------------------------------------

## Лабораторная работа 4

###ТЗ:

* Разработать ...

###Защита:

-------------------------------------------------------------

## Лабораторная работа 5

###ТЗ:

 * Создать электронную подпись
    * штатными средствами системы 
    * библиотечными средствами
 
Например:
(C# - Cryptography.DSACryptoServiceProvider, DSASignatureFormater, CreateSignature)

###Защита:

 * Электронная подпись
 * Подпись (простая):
    * жёстко связана с документом
    * добровольное согласие
    * удостоверяет, что её поставил автор (аутентичность)
    * подтверждает неизменность
    * неотказуемость

Алгоритм создания электронной подписи включает два этапа:
1. вычисление хеша
2. создание собственно подписи

На обоих шагах можно использовать целое семейство алгоритмов.

 * Исходное сообщение М. 
 * Вычисляется хеш-преобразование. 
 * Выполняется шифрование (например РСА, потребуется ключ). 
 * Зашифрованный хеш и будет подписью С.

Расшифровка: 
 * подпись С и сообщение М'. 
 * Вычисляется хеш от М'. 
 * Расшифровывается подпись С (с помощью ключа), 
 * получается исходный хеш. 
 * Вычисленный хеш сравнивается с расшифрованным, если не равны - исходное сообщение != переданному.

В случае РСА, закрытый ключ используется для расшифровки, открытый - для шифрования. 
Цель РСА в чистом виде - спрятать информацию.
Здесь же нужно проверить целостность сообщений - ключи меняются местами, создаваемая подпись шифруется закрытым и расшифровывается открытым.

ЭлЦифПодп - 1-ФЗ.
2011 год - 63-ФЗ, Электронная подпись.

Может быть три вида подписи - ???
 * простая, 
 * усиленная 
 * (неквалифицированная, квалифицированная). Квалифицированная создается с использованием сертификата, выпущенного сертифицированным удостоверяющим центром.

Процедуры создания ЭП - СредстваКриптографическойЗащитыИнформации. 

Как правило - часть ОС (CryptoAPI, создаёт CryptoServiceProvider) и доступны всем программам. 

Фактически, CSP - внедрённая в ОС библиотека, также подписываемая; ОС - контролирует подпись этой библиотеки.

Децентрализованная схема - субъекты хранят закрытые ключи и обмениваются открытыми, чтобы проверять целостность передаваемых данных. 

Алгоритм PrettyGoodPrivacy. Проблема - нет арбитров, удостоверяющих правильность подписей, есть поле для подлога.

Централизованная схема - есть арбитр, который сохраняет открытые ключи. 

PublicKeyInfrastructure. В ответ на присланный открытый ключ выдаётся сертификат открытого ключа, соответствующего закрытому.

Центр сертификации - Удостоверяющий центр, Certificate Authority. Стандарт X.509 задаёт формат сертификата и обмена УЦ с субъектом-владельцем. 

Формат предусматривает хранение информации о версии и алгоритме хеширования и шифрования, информацию о подписанте 
(ФИО, должность, организация, etc.), срок действия сертификата (~2 года), 
информацию про удостоверяющий центр и полномочия, которыми он наделил получателя сертификата (подпись, шифрование).

Удостоверяющий центр выпускает сертификат на открытый ключ. 

Закрытый ключ - святая святых и во внешние миры ходить не должен.
Ключевой параметр сертификата - срок действия. 

Сертификат можно отозвать до его "протухания". 

Списки отозванных сертификатов (C. revocation list) - список сертификатов, которые прекратили действие досрочно. 

Эти файлы также публикуются УЦ.

-------------------------------------------------------------

## Лабораторная работа 6

###ТЗ:

 * ...


###Защита:
