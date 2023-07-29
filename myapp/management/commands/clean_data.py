from myapp.models import PuestoVotacion, VotantePuestoVotacion, Votante
from django.core.management.base import BaseCommand

DOCUMENTS_TO_KEEP = [
    '91477435',
    '109550913',
    '1095937105',
    '1004857829',
    '91185453',
    '63285370',
    '1098638930',
    '28156332',
    '13541367',
    '1095920162',
    '914937483',
    '63357058',
    '1095959802',
    '1064112330',
    '1095909113',
    '1007962280',
    '1095933105',
    '37552137',
    '28217560',
    '28335979',
    '5565718',
    '91185444',
    '63491750',
    '1065902831',
    '88233331',
    '37897092',
    '4173453',
    '1005156837',
    '10953700',
    '13723244',
    '37512678',
    '1082858308',
    '1098615339',
    '1004822751',
    '105503136',
    '1098619916',
    '93360891',
    '1098707770',
    '63310975',
    '1005156572',
    '91177590',
    '57289977',
    '13822942',
    '37725280',
    '1095923622',
    '13815547',
    '1095924315',
    '30209909',
    '10959917919',
    '91185594',
    '1007427751',
    '28215831',
    '28155166',
    '1101682774',
    '52023556',
    '80374908',
    '1095917825',
    '91527525',
    '1094162527',
    '1095953580',
    '91212247',
    '1098806727',
    '1091518539',
    '1095948289',
    '1099736927',
    '1098869689',
    '1095924725',
    '1095924532',
    '28253247',
    '28156497',
    '28149148',
    '63319825',
    '63511167',
    '91203316',
    '1095912916',
    '37711379',
    '91183208',
    '68448230',
    '63451609',
    '13716741',
    '1235047625',
    '53278045',
    '1101200502',
    '28333413',
    '5645920',
    '28150829',
    '1193580307',
    '1095924960',
    '1095917562',
    '1098633890',
    '13871451',
    '1098686926',
    '13849442',
    '1098804345',
    '28152580',
    '1095939586',
    '1010309',
    '1095915279',
    '1095937105',
    '1095820088',
    '91183207',
    '63336083',
    '91235566',
    '28210330',
    '1098680197',
    '91151801',
    '13543929',
    '1095921409',
    '13355992',
    '1095917609',
    '1095906584',
    '37725236',
    '1005157313',
    '30208075',
    '1095927074',
    '1095922591',
    '1095941616',
    '1101690249',
    '13515446',
    '1095945700',
    '37838300',
    '1095909827',
    '6334889',
    '13837711',
    '28155460',
    '1095936137',
    '63299626',
    '1005371968',
    '1099735351',
    '91209019',
    '1095925533',
    '63515668',
    '91179660',
    '91213093',
    '1095934154',
    '1115735543',
    '100007752',
    '37580912',
    '91341115',
    '37551573',
    '13871113',
    '1095917277',
    '11179039',
    '63341387',
    '1067712115',
    '1005199123',
    '91133713',
    '37747525',
    '28010625',
    '1095996698',
    '1085157007',
    '1102391128',
    '91176755',
    '13703013',
    '13836413',
    '1095437105',
    '1005449257',
    '1095932644',
    '28157116',
    '91341398',
    '28149847',
    '1082873734',
    '1095956359',
    '1095934642',
    '1096219320',
    '73545920',
    '91754612',
    '1005155788',
    '1085096567',
    '1095929787',
    '1098619056',
    '28104596',
    '1095939660',
    '1095939661',
    '1095942565',
    '13842316',
    '138292299',
    '9118601218',
    '1095931485',
    '1098813030',
    '1005343820',
    '1099322027',
    '28155060',
    '1050919480',
    '1065237791',
    '63510692',
    '63492538',
    '91228200',
    '93465787',
    '49651102',
    '63354621',
    '1005235283',
    '13450849',
    '1102392453',
    '1097097570',
    '32848028',
    '79845147',
    '1099373958',
    '4976864',
    '91260216',
    '5684217',
    '52023556',
    '63541531',
    '91180324',
    '1098671738',
    '63296962',
    '37557258',
    '633314421',
    '1095689238',
    '30008639',
    '63315670',
    '1096065435',
    '4378396',
    '1006692192',
    '1003209117',
    '1099302134',
    '1096219320',
    '91481450',
    '60413133',
    '28336642',
    '63479315',
    '1102384979',
    '1007427751',
    '9146542',
    '3020942',
    '91227408',
    '28212937',
    '1007665854',
    '63366490',
    '1095908272',
    '1005065021',
    '91178470',
    '1098750049',
    '1095926881',
    '91056958',
    '91153223',
    '1102725120',
    '1101682774',
    '1095957311',
    '245514901',
    '28157378',
    '1102356884',
    '16587944',
    '37659560',
    '77196159',
    '1016538103',
    '91184081',
    '1004700087',
    '1005156420',
    '1089379005',
    '13061066',
    '1127337507',
    '1095922625',
    '37696467',
    '63559776',
    '3164573225',
    '71255816',
    '1095928690',
    '1098719420',
    '4172783',
    '1095931651',
    '1005331471',
    '91506858',
    '1098655321',
    '91237124',
    '1005235975',
    '63297931',
    '1095931919',
    '28212978',
    '1095933631',
    '91108834',
    '1148709162',
    '63498078',
    '1007665919',
    '1005198783',
    '1099373958',
    '6745772',
    '1095924685',
    '1096946742',
    '9770757',
    '37670678',
    '13512135',
    '1096539693',
    '28155617',
    '91240263',
    '1006599353',
    '302207103',
    '91286084',
    '1005162118',
    '1092358262',
    '63533601',
    '10965382821',
    '301210109',
    '1020804426',
    '37926834',
    '40512505',
    '1075732515',
    '37822542',
    '1098701104',
    '1096062937',
    '91256843',
    '56916494',
    '1098784363',
    '1095836991',
    '1099734997',
    '1010117858',
    '100516982',
    '7629193',
    '1095926483',
    '1095921414',
    '781295',
    '37559668',
    '38921320',
    '63514097',
    '1077608969',
    '1005155795',
    '1095926436',
    '100955283',
    '28150810',
    '28149885',
    '454537447',
    '37550430',
    '63342009',
    '1008416984',
    '40429022',
    '1095580296',
    '5729220',
    '63541876',
    '91509036',
    '1005333030',
    '91178816',
    '1042211787',
    '4342585',
    '13810290',
    '283377',
    '1328988108',
    '1097094344',
    '91446627',
    '91276692',
    '1098644542',
    '1099363630',
    '63304499',
    '63563446',
    '63299531',
    '91218625',
    '1096954047',
    '1098675337',
    '6648845',
    '1349844',
    '31817247',
    '28252351',
    '1095927728',
    '63493100',
    '1095943050',
    '1095908343',
    '1095946698',
    '13819288',
    '570343',
    '1095939509',
    '63497654',
    '5794394',
    '63504867',
    '19428123',
    '1005339136',
    '72178050',
    '1005157309',
    '28155454',
    '12458878',
    '1102385613',
    '63505638',
    '13685541',
    '5746313',
    '1095912315',
    '5670737',
    '1098773934',
    '5727007',
    '1095936142',
    '91180961',
    '1095954141',
    '5605940',
    '3712128',
    '1095907460',
    '13742676',
    '1098711422',
    '28154611',
    '1095920873',
    '1096062937',
    '1095925875',
    '1098607953',
    '63279058',
    '91290744',
    '1098715810',
    '1049898932',
    '1095937664',
    '1095908787',
    '13845039',
    '57464085',
    '21647105',
    '1024602787',
    '1050547734',
    '13822063',
    '4438144',
    '1095939509',
    '13892761',
    '37812519',
    '21523107',
    '1020454943',
    '51797616',
    '28253432',
    '1007617532',
    '5565718',
    '63470048',
    '6739203',
    '91480328',
    '91178890',
    '1095935531',
    '1095921756',
    '1095911778',
    '91207207',
    '5735135',
    '13853823',
    '1100895435',
    '1045420410',
    '130502726',
    '13872827',
    '63540278',
    '30208350',
    '30457890',
    '91481341',
    '1095927104',
    '1095910667',
    '64097451',
    '1095927957',
    '91184841',
    '91175011',
    '28118639',
    '1095957680',
    '1095906742',
    '1005209694',
    '91260389',
    '1095910713',
    '1095940313',
    '1095935001',
    '91182542',
    '91493632',
    '91175838',
    '37253274',
    '55304992',
    '1099371691',
    '1095921722',
    '1095934842',
    '63311543',
    '1007905593',
    '1095907963',
    '17527081',
    '281081790',
    '119315289',
    '28352512',
    '29902159',
    '5669653',
    '1091655149',
    '1095916188',
    '1095926403',
    '53116793',
    '1007366078',
    '1095948071',
    '1095924259',
    '1005322101',
    '22344373',
    '13482918',
    '13895219',
    '63360925',
    '37940611',
    '51670686',
    '1005549146',
    '1095923622',
    '1005655491',
    '63278695',
    '12615142',
    '63238945',
    '91212641',
    '6799194',
    '1095914223',
    '28329523',
    '1095934238',
    '1030662308',
    '1024555797',
    '91297067',
    '1096136458',
    '63537568',
    '1007193450',
    '1095947269',
    '28156404',
    '37316138',
    '1095944375',
    '63272722',
    '1095906503',
    '30209801',
    '1116775719',
    '1695495945',
    '1098788427',
    '91294544',
    '1095994888',
    '1098680915',
    '1005539576',
    '63508246',
    '37656902',
    '5776742',
    '91185235',
    '91280562',
    '63355802',
    '91180630',
    '1095925441',
    '91185031',
    '1095908637',
    '63490285',
    '1005340425',
    '28339433',
    '1094160365',
    '12720241',
    '28151002',
    '91499321',
    '1098634630',
    '60423409',
    '91003682',
    '63303752',
    '91747800',
    '37835861',
    '28156985',
    '91180543',
    '91001902',
    '10991355',
    '37745838',
    '1100889487',
    '85476742',
    '30210053',
    '63494705',
    '1095923989',
    '63559604',
    '25502755',
    '37808843',
    '1095934692',
    '1095920873',
    '1095949429',
    '63543242',
    '30207334',
    '1005563844',
    '60366374',
    '1098662067',
    '91185235',
    '1098680023',
    '1065916550',
    '96126041',
    '91281968',
    '1095929270',
    '5010796',
    '2100194',
    '27837748',
    '1007450962',
    '1116788516',
    '13826414',
    '1095939451',
    '1095920112',
    '63540170',
    '37720566',
    '1098668473',
    '1095915093',
    '37728265',
    '1093792098',
    '37551571',
    '10089204',
    '91463666',
    '1102389611',
    '28148671',
    '37833125',
    '52533690',
    '51806315',
    '21877888',
    '60380088',
    '1095928156',
    '1095910419',
    '1095912227',
    '91178515',
    '1073428504',
    '68251685',
    '28089768',
    '28152027',
    '1095985093',
    '1005199071',
    '1098708929',
    '1095952394',
    '37749401',
    '1095938810',
    '37559760',
    '37550904',
    '1005156618',
    '37550881',
    '37514672',
    '91293152',
    '5786683912',
    '91296335',
    '28155260',
    '91181888',
    '1095929270',
    '1095949429',
    '1098668473',
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group in ALL_GROUP:
            Group.objects.create(name=group)
