import email
from typing import List
from unicodedata import name
from fastapi import APIRouter
from catalogs.counterparty.models import Counterparty, CounterpartyOut
from catalogs.entity.models import Entity, EntityNestedOut
from catalogs.business_type.models import BusinessType
from catalogs.document_type.models import DocumentType
from catalogs.enum_types.models import ProcessStatusType, RouteStatusType, StepType
from catalogs.user.models import User
from core.db import database, SessionLocal
from sqlalchemy import select, insert, tuple_, join

initRouter = APIRouter()
session = SessionLocal()

@initRouter.get('/createBT')
def create_BusinessType():
    typeList = []
    typeList.append(BusinessType(name = 'АО', full_name = 'Акционерное Общество'))
    typeList.append(BusinessType(name = 'ТОО', full_name = 'Товарищество с ограниченной ответственностью'))
    typeList.append(BusinessType(name = 'ИП', full_name = 'Индивидуальный предприниматель'))
    typeList.append(BusinessType(name = 'ФизЛицо', full_name = 'Физическое лицо'))
    typeList.append(BusinessType(name = 'ГП', full_name = 'Государственное предприятие'))
    session.add_all(typeList)
    session.commit()
    return {'status': 'done'}

@initRouter.get('/createAllTypes')
def create_types():
    typeList = []
    typeList.append(ProcessStatusType(name = 'подписан', description = 'Подписан'))
    typeList.append(ProcessStatusType(name = 'отклонен', description = 'Отклонен'))
    typeList.append(ProcessStatusType(name = 'отменен', description = 'Отменен'))
    typeList.append(ProcessStatusType(name = 'в работе', description = 'В работе'))
    typeList.append(ProcessStatusType(name = 'черновик', description = 'Черновик'))

    typeList.append(RouteStatusType(name = 'согласован', description = 'Согласован'))
    typeList.append(RouteStatusType(name = 'отклонен', description = 'Отклонен'))

    typeList.append(StepType(name = 'линейное', description = 'Линейное'))
    typeList.append(StepType(name = 'параллельное', description = 'Параллельное'))

    session.add_all(typeList)
    session.commit()
    return {'status': 'done'}

@initRouter.get('/get_entityList',response_model=List[EntityNestedOut])
def get_entityList():
    query = select(Entity)
    session = SessionLocal()
    result = session.execute(query)
    resultAll = result.scalars().all()
    return resultAll

@initRouter.get('/getCounterpartyList',response_model=List[CounterpartyOut])
def getCounterpartyList():
    query = select(Counterparty)
    session = SessionLocal()
    result = session.execute(query)
    resultAll = result.scalars().all()
    return resultAll

# @initRouter.get('/createCounterpartyList')
# def get_entityList():
#     f = open("demofile.txt", "r")
#     for x in f:
#         print(x)
#     query = select(Entity)
#     session = SessionLocal()
#     result = session.execute(query)
#     resultAll = result.scalars().all()
#     return resultAll


@initRouter.get('/createAdmin')
def create_AdminUser():
    typeList = []
    typeList.append(User(name = 'Admin', email = 'admin@email.com', is_active = True, is_company = False))
    session.add_all(typeList)
    session.commit()
    return {'status': 'done'}

@initRouter.get('/createDT')
def create_DocumentType():
    typeList = []
    typeList.append(DocumentType(name = "ЗаявкаНаРасходованиеДенежныхСредств", description = "Заявка на расходование денежных средств"))
    typeList.append(DocumentType(name = "ЭлектронноеПисьмоИсходящее", description = "Электронное письмо исходящее"))
    typeList.append(DocumentType(name = "ЭСФ", description = "Электронный счет-фактура"))
    typeList.append(DocumentType(name = "АвизоПрочее", description = "Авизо по прочим операциям"))
    typeList.append(DocumentType(name = "АктОбОказанииПроизводственныхУслуг", description = "Акт об оказании производственных услуг"))
    typeList.append(DocumentType(name = "АктСверкиВзаиморасчетов", description = "Акт сверки взаиморасчетов"))
    typeList.append(DocumentType(name = "ВводНачальныхОстатков", description = "Ввод начальных остатков"))
    typeList.append(DocumentType(name = "ВводНачальныхОстатковОС", description = "Ввод начальных остатков по ОС"))
    typeList.append(DocumentType(name = "ВводНачальныхОстатковПоЗарплате", description = "Ввод начальных остатков по зарплате"))
    typeList.append(DocumentType(name = "ВводСведенийОПлановыхУдержанияхРаботниковОрганизаций", description = "Ввод сведений о плановых удержаниях сотрудников организаций"))
    typeList.append(DocumentType(name = "ВводСведенийОРеглУчетеПлановыхНачисленийРаботниковОрганизаций", description = "Ввод сведений о регл. учете плановых начислений сотрудников организаций"))
    typeList.append(DocumentType(name = "ВозвратЗарплатыРаботниковОрганизаций", description = "Возврат зарплаты сотрудников организации"))
    typeList.append(DocumentType(name = "ВозвратТоваровОтПокупателя", description = "Возврат ТМЗ от покупателя"))
    typeList.append(DocumentType(name = "ВозвратТоваровПоставщику", description = "Возврат ТМЗ поставщику"))
    typeList.append(DocumentType(name = "Встреча", description = "Встреча"))
    typeList.append(DocumentType(name = "ВыработкаНМА", description = "Выработка НМА"))
    typeList.append(DocumentType(name = "ВыработкаОС", description = "Выработка ОС"))
    typeList.append(DocumentType(name = "ГТДИмпорт", description = "ГТД по импорту"))
    typeList.append(DocumentType(name = "ДвижениеНЗП", description = "Движение незавершенного производства"))
    typeList.append(DocumentType(name = "ДепонированиеЗаработнойПлаты", description = "Депонирование заработной платы"))
    typeList.append(DocumentType(name = "Доверенность", description = "Доверенность"))
    typeList.append(DocumentType(name = "ДокументРасчетовСКонтрагентом", description = "Документ расчетов с контрагентом (ручной учет)"))
    typeList.append(DocumentType(name = "ЗакрытиеДтКтЗадолженности", description = "Закрытие Дт/Кт задолженности"))
    typeList.append(DocumentType(name = "ЗакрытиеМесяца", description = "Закрытие месяца"))
    typeList.append(DocumentType(name = "ЗапланированноеВзаимодействие", description = "Запланированное взаимодействие"))
    typeList.append(DocumentType(name = "ЗарплатаКВыплатеОрганизаций", description = "Зарплата к выплате организаций"))
    typeList.append(DocumentType(name = "ЗаявлениеНаПредоставлениеВычетовИПН", description = "Заявление на предоставление вычетов ИПН"))
    typeList.append(DocumentType(name = "ЗаявлениеОВвозеТоваровИУплатеКосвенныхНалогов", description = "Заявление о ввозе товаров и уплате косвенных налогов"))
    typeList.append(DocumentType(name = "ИзменениеГрафиковАмортизацииОС", description = "Изменение графиков амортизации ОС"))
    typeList.append(DocumentType(name = "ИзменениеПараметровНачисленияАмортизацииНМА", description = "Изменение параметров начисления амортизации НМА"))
    typeList.append(DocumentType(name = "ИзменениеПараметровНачисленияАмортизацииОС", description = "Изменение параметров начисления амортизации ОС"))
    typeList.append(DocumentType(name = "ИзменениеСостоянияОС", description = "Изменение состояния ОС"))
    typeList.append(DocumentType(name = "ИзменениеСпособовОтраженияРасходовПоАмортизацииНМА", description = "Изменение способа отражения расходов по амортизации НМА"))
    typeList.append(DocumentType(name = "ИзменениеСпособовОтраженияРасходовПоАмортизацииОС", description = "Изменение способа отражения расходов по амортизации ОС"))
    typeList.append(DocumentType(name = "ИЛПеречислениеПолучателям", description = "ИЛ перечисление получателям"))
    typeList.append(DocumentType(name = "ИнвентаризацияДенежныхСредств", description = "Инвентаризация денежных средств"))
    typeList.append(DocumentType(name = "ИнвентаризацияНЗП", description = "Инвентаризация незавершенного производства"))
    typeList.append(DocumentType(name = "ИнвентаризацияОС", description = "Инвентаризация ОС"))
    typeList.append(DocumentType(name = "ИнвентаризацияТоваровНаСкладе", description = "Инвентаризация ТМЗ на складе"))
    typeList.append(DocumentType(name = "ИПНЗаявлениеНаПредоставлениеВычета", description = "Заявление на предоставление вычета по ИПН (до 2018)"))
    typeList.append(DocumentType(name = "ИсполнительныйЛист", description = "Исполнительный лист"))
    typeList.append(DocumentType(name = "КадровоеПеремещениеОрганизаций", description = "Кадровое перемещение организации"))
    typeList.append(DocumentType(name = "КассоваяСмена", description = "Кассовая смена"))
    typeList.append(DocumentType(name = "КомандировкиОрганизаций", description = "Командировки организации"))
    typeList.append(DocumentType(name = "КомплектацияНоменклатуры", description = "Комплектация ТМЗ"))
    typeList.append(DocumentType(name = "КомплектацияОС", description = "Комплектация ОС"))
    typeList.append(DocumentType(name = "КорректировкаДолга", description = "Корректировка долга"))
    typeList.append(DocumentType(name = "КорректировкаСтоимостиСписанияТоваров", description = "Корректировки стоимости списания товаров"))
    typeList.append(DocumentType(name = "МодернизацияОС", description = "Модернизация ОС"))
    typeList.append(DocumentType(name = "НачислениеЗарплатыРаботникамОрганизаций", description = "Начисление зарплаты сотрудникам организации"))
    typeList.append(DocumentType(name = "ОПВВозвратВзносов", description = "Пенсионные взносы возврат из фондов"))
    typeList.append(DocumentType(name = "ОПВПеречислениеВФонды", description = "Пенсионные взносы перечисление в фонды"))
    typeList.append(DocumentType(name = "ОперацияБух", description = "Операция"))
    typeList.append(DocumentType(name = "ОплатаОтПокупателяПлатежнойКартой", description = "Оплаты от покупателя платежными картами"))
    typeList.append(DocumentType(name = "ОприходованиеТоваров", description = "Оприходование ТМЗ"))
    typeList.append(DocumentType(name = "ОтражениеЗарплатыВБухучете", description = "Отражение зарплаты в бух. учете (интеграция с ЗУП 3)"))
    typeList.append(DocumentType(name = "ОтражениеЗарплатыВРеглУчете", description = "Отражение зарплаты в регл. учете"))
    typeList.append(DocumentType(name = "ОтражениеНалоговойОтчетностиВРеглУчете", description = "Отражение налоговой отчетности в регл. учете"))
    typeList.append(DocumentType(name = "ОтчетОРозничныхПродажах", description = "Отчет о розничных продажах"))
    typeList.append(DocumentType(name = "ОтчетПроизводстваЗаСмену", description = "Отчет производства за смену"))
    typeList.append(DocumentType(name = "ПакетОбменСБанками", description = "Пакет прямого обмена с банками"))
    typeList.append(DocumentType(name = "Партия", description = "Партия (ручной учет)"))
    typeList.append(DocumentType(name = "ПередачаНМА", description = "Передача НМА"))
    typeList.append(DocumentType(name = "ПередачаОС", description = "Передача ОС"))
    typeList.append(DocumentType(name = "ПередачаТоваров", description = "Передача ТМЗ"))
    typeList.append(DocumentType(name = "ПеремещениеОС", description = "Перемещение ОС"))
    typeList.append(DocumentType(name = "ПеремещениеТоваров", description = "Перемещение ТМЗ"))
    typeList.append(DocumentType(name = "ПереоценкаВнеоборотныхАктивов", description = "Переоценка внеоборотных активов"))
    typeList.append(DocumentType(name = "ПисьмоОбменСБанками", description = "Письмо с банком"))
    typeList.append(DocumentType(name = "ПлатежноеПоручениеВходящее", description = "Платежное поручение (входящее)"))
    typeList.append(DocumentType(name = "ПлатежноеПоручениеИсходящее", description = "Платежное поручение (исходящее)"))
    typeList.append(DocumentType(name = "ПлатежныйОрдерПоступлениеДенежныхСредств", description = "Платежный ордер (поступление денежных средств)"))
    typeList.append(DocumentType(name = "ПлатежныйОрдерСписаниеДенежныхСредств", description = "Платежный ордер (списание денежных средств)"))
    typeList.append(DocumentType(name = "ПоступлениеДопРасходов", description = "Поступление доп. расходов"))
    typeList.append(DocumentType(name = "ПоступлениеИзПереработки", description = "Поступление из переработки"))
    typeList.append(DocumentType(name = "ПоступлениеНМА", description = "Поступление НМА"))
    typeList.append(DocumentType(name = "ПоступлениеТоваровУслуг", description = "Поступление ТМЗ и услуг"))
    typeList.append(DocumentType(name = "ПрекращениеПредоставленияВычетовИПН", description = "Прекращение предоставления вычетов ИПН"))
    typeList.append(DocumentType(name = "ПриемНаРаботуВОрганизацию", description = "Прием на работу в организацию"))
    typeList.append(DocumentType(name = "ПринятиеКУчетуНМА", description = "Принятие к учету НМА"))
    typeList.append(DocumentType(name = "ПринятиеКУчетуОС", description = "Принятие к учету ОС"))
    typeList.append(DocumentType(name = "ПриходныйКассовыйОрдер", description = "Приходный кассовый ордер"))
    typeList.append(DocumentType(name = "РасходныйКассовыйОрдер", description = "Расходный кассовый ордер"))
    typeList.append(DocumentType(name = "РасчетНалоговПриПоступленииАктивовУслуг", description = "Расчет налогов при поступлении активов и услуг"))
    typeList.append(DocumentType(name = "РасчетПениОПВиСО", description = "Расчет пени по взносам и отчислениям"))
    typeList.append(DocumentType(name = "РасчетСНиСО", description = "Расчет налогов, взносов и отчислений сотрудников организаций"))
    typeList.append(DocumentType(name = "РасчетУдержанийРаботниковОрганизаций", description = "Расчет удержаний сотрудников организаций"))
    typeList.append(DocumentType(name = "РеализацияТоваровУслуг", description = "Реализация ТМЗ и услуг"))
    typeList.append(DocumentType(name = "РеализацияУслугПоПереработке", description = "Реализация услуг по переработке"))
    typeList.append(DocumentType(name = "РегистрацияНДСЗаНерезидента", description = "Регистрация НДС за нерезидента"))
    typeList.append(DocumentType(name = "РегистрацияПрочихДоходовВЦеляхНалогообложения", description = "Регистрация прочих доходов в целях налогообложения"))
    typeList.append(DocumentType(name = "РегистрацияПрочихОперацийПоПриобретеннымТоварамВЦеляхНДС", description = "Регистрация прочих операций по приобретенным товарам (работам, услугам) в целях НДС"))
    typeList.append(DocumentType(name = "РегистрацияПрочихОперацийПоРеализованнымТоварамВЦеляхНДС", description = "Регистрация прочих операций по реализованным товарам (работам, услугам) в целях НДС"))
    typeList.append(DocumentType(name = "РегистрацияРазовыхУдержанийРаботниковОрганизаций", description = "Регистрация разовых удержаний сотрудников организации"))
    typeList.append(DocumentType(name = "РегламентированныйОтчет", description = "Регламентированная отчетность"))
    typeList.append(DocumentType(name = "РеструктуризацияОС", description = "Реструктуризация ОС"))
    typeList.append(DocumentType(name = "АвансовыйОтчет", description = "Авансовый отчет"))
    typeList.append(DocumentType(name = "СОВозвратОтчислений", description = "Социальное страхование возврат из фондов"))
    typeList.append(DocumentType(name = "СообщениеОбменСБанками", description = "Сообщение обмена с банками"))
    typeList.append(DocumentType(name = "СОПеречислениеВФонды", description = "Социальное страхование перечисление в фонды"))
    typeList.append(DocumentType(name = "СНТ", description = "Электронная сопроводительная накладная на товары"))
    typeList.append(DocumentType(name = "СписаниеНМА", description = "Списание НМА"))
    typeList.append(DocumentType(name = "СписаниеОС", description = "Списание ОС"))
    typeList.append(DocumentType(name = "СписаниеТоваров", description = "Списание ТМЗ"))
    typeList.append(DocumentType(name = "Сторнирование", description = "Сторнирование"))
    typeList.append(DocumentType(name = "СчетНаОплатуПокупателю", description = "Счет на оплату покупателю"))
    typeList.append(DocumentType(name = "СчетФактураВыданный", description = "Счет-фактура (выданный)"))
    typeList.append(DocumentType(name = "СчетФактураПолученный", description = "Счет-фактура (полученный)"))
    typeList.append(DocumentType(name = "ТелефонныйЗвонок", description = "Телефонный звонок"))
    typeList.append(DocumentType(name = "ТребованиеНакладная", description = "Требование-накладная"))
    typeList.append(DocumentType(name = "УвольнениеИзОрганизаций", description = "Увольнение из организации"))
    typeList.append(DocumentType(name = "УдалитьКорректировкаЗаписейРегистров", description = "(не используется) Корректировка записей регистров"))
    typeList.append(DocumentType(name = "УдержаниеИПНиОПВНУ", description = "Удержание ИПН, ОПВ и ВОСМС по налоговому учету"))
    typeList.append(DocumentType(name = "УстановкаПорядкаЗакрытияПодразделений", description = "Установка порядка подразделений для закрытия счетов"))
    typeList.append(DocumentType(name = "УстановкаСоответствияСчетовБУиНУ", description = "Установка соответствия счетов БУ и НУ"))
    typeList.append(DocumentType(name = "УстановкаЦенНоменклатуры", description = "Установка цен номенклатуры"))
    typeList.append(DocumentType(name = "ЧекККМ", description = "Розничная продажа (чек)"))
    typeList.append(DocumentType(name = "ЭлектронноеПисьмоВходящее", description = "Электронное письмо входящее"))
    typeList.append(DocumentType(name = "ЭлектронныйАктВыполненныхРабот", description = "Электронный акт выполненных работ"))
    typeList.append(DocumentType(name = "ЭлектронныйДокументВС", description = "Электронный документ ВС"))
    typeList.append(DocumentType(name = "СопоставлениеСНТиФНО", description = "Сопоставление СНТ с ФНО 328.00"))
    session.add_all(typeList)
    session.commit()
    return {'status': 'done'}