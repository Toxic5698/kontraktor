from django.contrib.auth.models import User

from base.models import ContractType, ContractSubject
from documents.models import DocumentSection, DocumentParagraph
from operators.models import Operator


def initial_creation():
    # operator
    Operator.objects.create(
        name="Demo operator s.r.o.",
        address="Procesní 4, Brno",
        id_number="45242455",
        bank_number="45242/435",
        acting_person="Daemonem, ředitelem",
        web="http://www.samoset.cz",
        email="admin@samoset.cz",
        phone_number="45245235",
    )

    user = User.objects.create(
        username="Aneta Demová",
        email="demo@samoset.cz",
    )
    # contract type
    dilo = ContractType.objects.create(type="DILO", name="Smlouva o dílo", vat=15)
    koupe = ContractType.objects.create(type="KOUPE", name="Kupní smlouva", vat=21)
    # contract subject
    subjects = {
        "DVERE": "pouze dveře",
        "PODLAHA": "pouze podlaha",
        "DVERE_PODLAHA": "dveře i podlaha",
        "ZBOZI": "zboží",
        "STAVBA": "stavební práce",
    }
    for code, name in subjects.items():
        ContractSubject.objects.create(code=code, name=name)

    # contract sections dílo
    sections = {
        "I": "Základní ustanovení",
        "II": "Záruka za jakost a vady díla",
        "III": "Sankce",
        "IV": "Reklamační řád",
        "V": "Závěrečná jednání",
    }
    for num, text in enumerate(sections.values(), 1):
        DocumentSection.objects.create(priority=num, name=text, contract_type=dilo)

    # contract paragraphs dílo
    cores = {
        "11": "Zhotovitel se touto smlouvou zavazuje provést na svůj náklad a nebezpečí pro objednatele dílo spočívající v dodávce a montáži předmětu smlouvy v místě plnění a nejpozději v den termínu plnění. Objednatel se touto smlouvou zavazuje poskytnout zhotoviteli potřebnou součinnost a provedené dílo převzít a zaplatit jeho cenu.",
        "12": "Cena díla je smluvní a objednatel se ji zavazuje uhradit dle sjednaných platebních podmínek.",
        "13": "Zhotovitel není zavázán k zahájení díla do doby uhrazení zálohy objednatelem, pokud se tak byly dohodnuty platební podmínky. O dobu prodlení objednatele se zaplacením zálohy se prodlužuje termín pro dokončení díla, pokud byla záloha sjednána. Pokud objednatel neuhradí zálohu ani do 10 dnů po lhůtě splatnosti zálohové faktury, je zhotovitel oprávněn od této smlouvy odstoupit.",
        "14": "V případě, že objednatel neposkytne zhotoviteli potřebnou součinnost či nesplní ve sjednaných termínech podmínky nezbytné pro řádné a včasné plnění závazků zhotovitelem, zavazuje se uhradit zhotoviteli skutečné náklady, které zhotoviteli vzniknou v souvislosti s nesplněním či porušením závazků a povinností objednatele a které by zhotovitel při řádném jednání objednatele nevynaložil. Současně se o dobu prodlení objednatele s poskytnutím potřebné součinnosti či se plněním podmínek pro řádné a včasné plnění závazků zhotovitele prodlužuje termín plnění pro dokončení díla.",
        "15": "Zhotovitel upozorní objednatele bez zbytečného odkladu na nevhodnou povahu věci, kterou mu objednatel k provedení díla předal, nebo příkazu, který mu objednatel dal. To neplatí, nemohl-li nevhodnost zjistit ani při vynaložení potřebné péče. Překáží-li nevhodná věc nebo příkaz v řádném provádění díla, zhotovitel je v nezbytném rozsahu přeruší až do výměny věci, nebo změny příkazu. Trvá-li objednatel na provádění díla s použitím předané věci nebo podle daného příkazu, má zhotovitel právo požadovat, aby tak objednatel učinil písemně. Lhůta pro dokončení díla se prodlužuje o dobu přerušením vyvolanou. Zhotovitel má právo na úhradu nákladů spojených s přerušením díla nebo s použitím nevhodných věcí do doby, kdy jejich nevhodnost mohla být zjištěna. Trvá-li objednatel na provedení díla podle zřejmě nevhodného příkazu nebo s použitím zřejmě nevhodné věci i po zhotovitelově upozornění, může zhotovitel od smlouvy odstoupit. Zachová-li se zhotovitel podle tohoto bodu smlouvy, nemá objednatel práva z vady díla vzniklé pro nevhodnost věci nebo příkazu.",
        "16": "Objednatel má právo kontrolovat provádění díla. Zjistí-li objednatel, že zhotovitel porušuje svou povinnost, může požadovat, aby zhotovitel zajistil nápravu a prováděl dílo řádným způsobem. Neučiní-li tak zhotovitel ani v přiměřené době, může objednatel od smlouvy odstoupit, vedl-li by postup zhotovitele nepochybně k podstatnému porušení smlouvy.",
        "17": "Objednatel je povinen připravit místo k provedení díla podle dodacích a montážních podmínek. Při zahájení montáže bude proveden zápis do předávacího protokolu o stavu staveniště a jeho připravenosti.",
        "18": "Dílo je provedeno, je-li dokončeno a předáno. Dokončením díla se rozumí, že je předvedena jeho způsobilost sloužit svému účelu. Objednatel převezme dokončené dílo s výhradami nebo bez výhrad. O převzetí bude vyhotoven písemný zápis.",
        "19": "Provádí-li se dílo postupně a lze-li jednotlivé části (stupně) odlišit, může být předáno a převzato i po částech. Převzetím díla nabývá objednatel vlastnické právo k věci a přechází na něho nebezpečí škody na věci. V případě, že objednatel neposkytne potřebnou součinnost a věci určené k provedení díla budou uloženy na místě jejich montáže, přechází nebezpečí škody na nich na objednatele dnem jejich uložení na místě montáže, o čemž zhotovitel vyhotoví dodací list a ten bude podepsán objednatelem i zhotovitelem.",
        "21": "Zhotovitel dává objednateli záruku za jakost díla v délce 24 měsíců. Záruční doba začíná běžet předáním díla objednateli.",
        "22": "Práva objednatele ze záruky se řídí reklamačním řádem zhotovitele a příslušnými ustanoveními občanského zákoníku.",
        "23": "Má-li dílo při předání vadu, zakládá to povinnost zhotovitele z vadného plnění.",
        "24": "Objednatel umožní zhotoviteli přístup na místo montáže (provedení díla) k odstranění vad a nedodělků i poté, co dílo převzal. V případě, že objednatel tuto součinnost neposkytne ani po druhém návrhu termínu, má se za to, že objednatel s vadami souhlasí a zaniká tak odpovědnost zhotovitele za jejich odstranění.",
        "25": "Objednatel bere na vědomí, že u dýhovaných dveří a zárubní SAPELI se jedná o přírodní materiál s různorodostí v celé škále. Vystouplé struktury a barevné rozdíly nemohou být považovány za vadu, neboť vznikají přírodní rozdílností dřeva a jeho charakteristickými vlastnostmi. Z toho důvodu reklamace na barevnost těchto výrobků budou považovány za neoprávněné.",
        "31": "V případě prodlení s provedením díla ve sjednaném termínu, uhradí zhotovitel objednateli smluvní pokutu ve výši 0,05 % z ceny díla bez DPH za každý den prodlení.",
        "32": "V případě prodlení se zaplacením ceny díla včetně zálohy na tuto cenu, zaplatí objednatel zhotoviteli smluvní pokutu ve výši 0,1 % z dlužné částky za každý den prodlení.",
        "33": "V případě, že objednatel neposkytne potřebnou součinnost spočívající ve stavební připravenosti pro montáž dveří a zárubní a nezajistí odpovídající prostor pro uložení věcí určených k montáži na místě provádění díla, zaplatí zhotoviteli náklady vynaložené na uskladnění věcí ve výši 10,- Kč za den a 1 ks až do doby, kdy objednatel nedostatky bránící provedení montáže odstraní a zhotovitel bude moci plnit řádně svoje závazky.",
        "34": "V případě, že objednatel odstoupí od této smlouvy v době kratší než 8 týdnů před termínem montáže, je povinen zaplatit zhotoviteli náhradu vynaložených nákladů na provedení díla ve výši 70 % z ceny díla bez DPH.",
        # # podlaha začátek
        # "41": "V případě podlahového topení nesmí teplota na povrchu podlahy přesáhnout 27 °C na nášlapné vrstvě. Spuštění podlahového topení po nivelaci by se mělo provádět pozvolna.",
        # "42": "Po instalaci podlah by se měla teplota v místnosti pohybovat v běžných hodnotách teplot od 16 - 25°C po celou dobu životnosti podlahy.",
        # "43": "Pokud nejsou místnosti klimatizované, v letních měsících je potřeba zajistit, aby nedopadaly přímé sluneční paprsky na podlahu.",
        # "44": "Po pokládce obdrží objednatel návod k údržbě podlahy a doporučení vhodných čistících prostředků, které je důležité používat. Používání agresivních nebo nedoporučených čističů vede k nevratnému poškození nášlapné vrstvy. Dbejte pokynů výrobce krytiny.",
        # "45": "Veškeré nohy nábytku, které jsou pohyblivé (zejména stolů, židlí), by měly být ošetřené funkčními ochrannými prvky.",
        # "46": "Pro ochranu podlahy před mechanickým poškozením by měly být používány vhodné čistící zóny.",
        # "47": "Další pokyny pro údržbu jsou uvedeny v návodech ke konkrétnímu typu podlah.",
        #
        # "51": "Stavební připravenost není splněna pokud podklad dosahuje následujících hodnot vlkosti dle druhu podkladu: Cementový potěr, beton > Kamenná nebo keramická dlažba 5,0 %, Lité podlahy na bázi cementu 5,0 %, Syntetické lité podlahy 4,0 %, Paropropustná textílie 5,0 %, PVC,linoleum, guma, korek 3,5 %, Dřevěné podlahy, parkety, laminát 2,5 %; Potěr na bázi síranu vápenatého (anhydrit) > Kamenná nebo keramická dlažba - 0,5 %, Lité podlahy na bázi cementu - Nelze provádět, Syntetické lité podlahy - 0,5 %, Paropropustná textílie - 1,0 %, PVC,linoleum, guma, korek - 0,5 %, Dřevěné podlahy, parkety, laminát - 0,5 %. V případě že je v podkladu podlahové vytápění je potřeba u cementu dále hodnotu ponížit o 0,5 % a u anhydritu o 0,2 %.",
        # "52": "V případě anhydritové podlahy objednatel zajistí stržení vrchního syntru až na plnivo. V opačném případě je zhotovitel oprávněn účtovat vícepráce za odstranění syntru na anhydritu po vytvrdnutí s diamanty v ceně 210,- až 240,- Kč/m2.",
        # "53": "Je-li součástí potěru podlahové vytápění zajistí objednatel nátopnou zkoušku, o níž bude proveden zápis do stavebního deníku.",
        # "54": "Podlahové topení je nutné minimálně 4 hodiny před započetím montáže úplně vypnout. Pokud je podlahové topení jediný zdroj tepla v místnostech, kde by měla proběhnout montáž, zajistí objednatel jiný zdroj tepla (přímotopy) k zajištění teploty vhodné pro montáž (obvykle v rozmezí mezi 16 až 25 °C).",
        # "55": "Objednatel je povinen zajistit zdroj elektrické energie (220 V maximálně 10 metrů od místa montáže) a vody.",
        # "56": "Pevnosti cementového a anhydritového potěru musí být větší jak 1 MPa v odtrhu.",
        # "57": "Uzná-li zhotovitel za nutné udělat sondu do podkladu nebo další měření, je o tom povinen informovat objednatele a dohodnout se na realizaci, úhradě nákladů a případně změny termínu dokončení díla.",
        # "58": "V průběhu montáže zajistí objednatel, že nebudou v prostorách montáže probíhat žádné jiné práce ani se pohybovat další osoby.",
        # "59": "Za skryté vady vlhkosti a vady konstrukční v podkladu, které způsobí poškození krytiny a mechanické poškození nenese zhotovitel odpovědnost.",
        # # podlaha konec
        #
        # # dodací podmínky na dveře doplnit
        #
        #     # montáž
        # "d51": "Dveře a zárubně je možné montovat výhradně do suchých prostor s relativní vlhkostí 40 – 50 %, s podmínkou dostatečně proschlého zdiva a omítky (při vyšší vlhkosti montážní pěna tuto vlhkost přijme a následně dojde k prohnutí zárubně). Minimální teplota pro montáž je stanovena +10°C. Montáž zárubní a osazení dveří by měla být úplně poslední operací stavby po začištění a podlahách.",
        # #
        # reklamační řád
        "41": "Objednatel je povinen reklamaci uplatnit bez zbytečného odkladu poté, co zjistí, že je dílo nebo jeho část vadné. Zhotovitel neodpovídá za zvětšení rozsahu poškození, pokud objednatel dílo užívá, ačkoliv o vadě ví. Uplatní-li objednatel vůči zhotoviteli vadu oprávněně, neběží lhůta pro uplatnění reklamace po dobu (záruční lhůta), po kterou je dílo nebo jeho část v opravě a objednatel je nemůže užívat.",
        "42": "Zhotovitel je povinen vydat objednateli písemné potvrzení, ve kterém uvede datum a místo uplatnění reklamace, charakteristiku vytýkané vady, objednatelem požadovaný způsob vyřízení reklamace a způsob jakým bude objednatel informován o jejím vyřízení.",
        "43": "Reklamace včetně odstranění vady musí být vyřízena bez zbytečného odkladu, nejpozději do 30 dnů ode dne uplatnění reklamace, pokud se zhotovitel s objednatelem nedohodnou na delší lhůtě.",
        "44": "Objednatel je povinen převzít si reklamované části díla do 30 dnů ode dne, kdy měla být reklamace nejpozději vyřízena, po této době je zhotovitel oprávněn účtovat si přiměřené skladné či dílo svépomocně prodat na účet objednatele. O tomto postupu musí zhotovitel objednatele předem upozornit a poskytnout mu přiměřenou dodatečnou lhůtu k převzetí díla.",
        "45": "Za podstatnou vadu se nepovažuje, tj. objednatel není oprávněn uplatnit právo na odstoupení od smlouvy dle předchozího odstavce či slevu z kupní ceny, pokud má dílo vady, jež jsou podmíněny přirozenými vlastnostmi výrobních materiálů (zejména vady estetické u díla s povrchem z přírodních materiálů) a jež nemají vliv na funkčnost díla a jeho řádné užívání.",
        "46": "Zhotovitel nenese odpovědnost za vady: a) je-li vada na věci v době převzetí a pro takovou vadu je sjednána sleva z kupní ceny; b) jde-li o použité zboží a vada odpovídá míře používání nebo opotřebení, které mělo dílo při převzetí objednatelem; c) vada vznikla na věci opotřebením způsobeným obvyklým užíváním, nebo vyplývá-li to z povahy věci (např. uplynutím životnosti); d) je způsobena objednatelem a vznikla nesprávným užíváním, skladováním, nesprávnou údržbou, zásahem objednatele či mechanickým poškozením; e) vzniklé v důsledku nevhodného prostředí s vyšší vlhkosti nebo kolísající teplotou, pokud není dílo pro takové podmínky určeno; f) vzniknuvší v důsledku vnější události mimo vliv zhotovitele.",
        "47": "Za vadu rovněž nelze považovat: a) rozdílnou barevnost rámečků a barevnost povrchu na zárubních a dveřích; b) rozdílnou barevnost a kresbu dýhy jednotlivých dveří, zárubní, jejich prvků, když v obou případech se jedná o vlastnosti charakteristické pro přírodní materiál; c) délkové napojení dýhy na obložce; d) rozdílnou barevnost u použitých přírodních nebo umělých materiálů v případě, že je nutná jejich kombinace z technologických důvodů v rámci jednoho výrobku nebo více výrobků tvořících komplet; e) dodání dílo nebo jeho provedení dodané na základě objednatelem potvrzené chybné závazné nabídky nebo objednatelem potvrzené chyby v kupní smlouvě.",
        "48": "Ve sporných případech vad díla způsobených relativní vlhkostí vzduchu (vysokou i nízkou) se za rozhodné považuje měření vlhkosti poškozené věci kalibrovaným vlhkoměrem. V případě, že vlhkost konstrukce dveří nebo zárubní se pohybuje mimo rozmezí 6-10 %, má se za to, že dílo nebo jeho část bylo vystaveno nevhodným vlhkostním podmínkám a může docházet k deformacím, za které zhotovitel nenese odpovědnost.",
        "49": "V případě, že dojde mezi zhotovitelem a objednatelem ke vzniku sporu, který se nepodaří vyřešit výše uvedeným způsobem, může objednatel podat návrh na mimosoudní řešení takového sporu určenému subjektu mimosoudního řešení spotřebitelských sporů, kterým je Česká obchodní inspekce, Ústřední inspektorát - oddělení ADR, Štěpánská 15, 120 00 Praha 2, e-mail: adr@coi.cz, web: adr.coi.cz.",
        "51": "Smluvní strany se zavazují, že v případě, kdy dojde k podstatnému snížení možnosti plnění této smlouvy jednou ze stran, se smluvní strany dohodnou na novém znění této smlouvy, které bude odpovídat aktuálním možnostem plnění předmětu této smlouvy smluvními stranami. V případě, že nebude možné se dohodnout na změně této smlouvy, je smluvní strana postižená změnou okolností dle výše uvedeného oprávněna od této smlouvy odstoupit, aniž by měla druhá smluvní strana nárok na náhradní plnění nebo náhradu škody.",
        "52": "Tato smlouva nabude účinnosti dnem podpisu smluvními stranami za podmínky. Smluvní strany se dohodly, že podpis smlouvy lze uskutečnit i elektronicky.",
        "53": "Právní vztahy, které nejsou v této smlouvě výslovně upraveny, se řídí příslušnými ustanoveními občanského zákoníku.",
        "54": "Smluvní strany prohlašují, že tato smlouva byla sepsána podle jejich pravé, svobodné a vážné vůle, a že souhlasí s jejím obsahem a zněním.",
    }

    for num, text in cores.items():
        cc = DocumentParagraph.objects.create(
            priority=num[1],
            document_section=DocumentSection.objects.get(priority=num[0], contract_type=dilo),
            text=text,
            contract_type=dilo,
            document_type="contract",
            created_by=user,
        )

    # contact sections koupě
    sections = {
        "I": "Základní ustanovení",
        "II": "Záruka za jakost",
        "III": "Sankce",
        "IV": "Reklamační řád",
        "V": "Závěrečná jednání",
    }
    for num, text in enumerate(sections.values(), 1):
        DocumentSection.objects.create(
            priority=num,
            name=text,
            contract_type=koupe,
            created_by=user,
        )

    # contract cores koupě
    cores = {
        "11": "Prodávající se zavazuje, že kupujícímu odevzdá věci movité, jejichž druh, množství a kupní cena jsou specifikovány výše a umožnit kupujícímu nabýt vlastnické právo k nim, nejpozději v den termínu plnění dle této smlouvy. Kupující se zavazuje, že věci movité od prodávajícího převezme a zaplatí sjednanou kupní cenu dle platebních podmínek uvedených v této smlouvě.",
        "12": "Náklady spojené s odevzdáním v místě plnění nese prodávající a náklady spojené s převzetím věcí movitých nese kupující.",
        "13": "V případě, že se smluvní strany dohodly na platbě před předáním, má prodávající právo předat předmět koupě až po jejím zaplacení, a to do 3 dnů po připsání zálohy na účet prodávajícího nebo složení zálohy na pokladně prodávajícího. Prodávající se při prodlení kupujícího se zaplacením zálohy nedostává do prodlení se splněním termínu předání předmětu koupě kupujícímu za dobu od sjednaného termínu plnění do konce 3 dne po zaplacení zálohy.",
        "14": "Vlastnické právo přechází na kupujícího převzetím předmětu koupě. Nebezpečí škody na předmětu koupě přechází na kupujícího jeho převzetím. Stejný následek má, nepřevezme-li kupující předmět koupě, ač mu s ním prodávající umožnil nakládat. Předá-li prodávající předmět koupě dopravci pro přepravu ke kupujícímu v místě plnění, přechází nebezpečí škody na předmětu koupě na kupujícího předáním předmětu koupě dopravci.",
        "15": "Škoda na předmětu koupě, vzniklá po přechodu nebezpečí škody na kupujícího, nemá vliv na povinnosti kupujícího zaplatit kupní cenu, ledaže prodávající škodu způsobil porušením svých povinností.",
        "16": "V případě, že kupující uhradí prodávajícímu kupní cenu v plné výši jednorázově při podpisu této kupní smlouvy, poskytne mu prodávající slevu z kupní ceny ve výši 2 % z kupní ceny bez DPH.",
        "21": "Prodávající se zavazuje, že předmět koupě bude způsobilý pro obvyklý účel po dobu 24 měsíců. Záruční doba běží od odevzdání předmětu koupě kupujícímu.",
        "22": "Kupující bere na vědomí, že u předmětu koupě vyrobeného z přírodních materiálů (zejména u dýhovaných dveří a zárubní SAPELI) se jedná o přírodní materiál s různorodostí v celé škále. Vystouplé struktury a barevné rozdíly nemohou být považovány za vadu, neboť vznikají přírodní rozdílností dřeva a jeho charakteristickými vlastnostmi. Z toho důvodu reklamace na barevnost těchto výrobků budou považovány za neoprávněné.  Prodávající výslovně upozorňuje, že u sukatých dýh jsou všechny vady dřeva, které se projevují nerovností povrchu nebo vypadnutím dřevní hmoty, vyspraveny tmelem tak, aby nebyla zásadně porušena celistvost povrchu. Barva tmele se volí dle převládající barvy suku nebo dýhy.",
        "23": "V ostatním se podmínky uplatnění práva z vad předmětu koupě použije reklamační řád prodávajícího a občanský zákoník.",
        "31": "Kupující potvrdí převzetí předmětu koupě na dodacím listu vystaveném prodávajícím. V případě, že kupující bude v prodlení s převzetím předmětu koupě, uchová prodávající předmět koupě pro kupujícího způsobem přiměřeným okolnostem a je oprávněn předmět koupě zadržet, dokud mu kupující neuhradí účelně vynaložené náklady spojené s uchováním předmětu koupě, a to ve výši 10,- Kč za 1 den a kus předmětu koupě (dveře, zárubeň, balení podlah) a za dobu ode dne následujícího po dni, v němž měl kupující předmět koupě převzít, do dne, kdy předmět koupě od prodávajícího skutečně převezme.",
        "32": "V případě, že se kupující dostane do prodlení se zaplacením kupní ceny, může prodávající požadovat zaplacení smluvní pokuty ve výši 0,1 % z dlužné částky za každý den prodlení.",
        "33": "V případě, že se prodávající dostane do prodlení se předáním předmětu koupě, může kupující požadovat zaplacení smluvní pokuty ve výši 0,05 % z kupní ceny za každý den prodlení.",
        "34": "V případě, že prodávající od této kupní smlouvy odstoupí z důvodu neposkytnutí součinnosti ze strany kupujícího ani po písemné výzvě, je kupující povinen zaplatit prodávajícímu smluvní pokutu ve výši 70 % z kupní ceny předmětu koupě.",
        "35": "Smluvní strany nemají právo na náhradu škody vzniklé z porušení povinnosti, ke kterému se smluvní pokuta vztahuje.",
        # reklamační řád
        "41": "Kupující je povinen reklamaci uplatnit bez zbytečného odkladu poté, co zjistí, že předmět koupě nebo jeho část je vadný. Prodávající neodpovídá za zvětšení rozsahu poškození, pokud kupující předmět koupě užívá, ačkoliv o vadě ví. Uplatní-li kupující vůči prodávajícímu vadu oprávněně, neběží lhůta pro uplatnění reklamace po dobu (záruční lhůta), po kterou je předmět koupě nebo jeho část v opravě a kupující jej nemůže užívat.",
        "42": "Prodávající je povinen vydat kupujícímu písemné potvrzení, ve kterém uvede datum a místo uplatnění reklamace, charakteristiku vytýkané vady, kupujícím požadovaný způsob vyřízení reklamace a způsob jakým bude kupující informován o jejím vyřízení.",
        "43": "Reklamace včetně odstranění vady musí být vyřízena bez zbytečného odkladu, nejpozději do 30 dnů ode dne uplatnění reklamace, pokud se prodávající s kupujícím nedohodnou na delší lhůtě.",
        "44": "Kupující je povinen převzít si reklamované části předmětu koupě do 30 dnů ode dne, kdy měla být reklamace nejpozději vyřízena, po této době je prodávající oprávněn účtovat si přiměřené skladné či předmět koupě svépomocně prodat na účet kupujícího. O tomto postupu musí prodávající kupujícího předem upozornit a poskytnout mu přiměřenou dodatečnou lhůtu k převzetí předmětu koupě.",
        "45": "Za podstatnou vadu se nepovažuje, tj. kupující není oprávněn uplatnit právo na odstoupení od smlouvy dle předchozího odstavce či slevu z kupní ceny, pokud má předmět koupě vady, jež jsou podmíněny přirozenými vlastnostmi výrobních materiálů (zejména vady estetické u předmětu koupě s povrchem z přírodních materiálů) a jež nemají vliv na funkčnost předmětu koupě a jeho řádné užívání.",
        "46": "Prodávající nenese odpovědnost za vady: a) je-li vada na věci v době převzetí a pro takovou vadu je sjednána sleva z kupní ceny; b) jde-li o použité zboží a vada odpovídá míře používání nebo opotřebení, které měl předmět koupě při převzetí kupujícím; c) vada vznikla na věci opotřebením způsobeným obvyklým užíváním, nebo vyplývá-li to z povahy věci (např. uplynutím životnosti); d) je způsobena kupujícím a vznikla nesprávným užíváním, skladováním, nesprávnou údržbou, zásahem kupujícího či mechanickým poškozením; e) vzniklé v důsledku nevhodného prostředí s vyšší vlhkosti nebo kolísající teplotou, pokud není předmět koupě pro takové podmínky určen; f) vzniknuvší v důsledku vnější události mimo vliv prodávajícího.",
        "47": "Za vadu rovněž nelze považovat: a) rozdílnou barevnost rámečků a barevnost povrchu na zárubních a dveřích; b) rozdílnou barevnost a kresbu dýhy jednotlivých dveří, zárubní, jejich prvků, když v obou případech se jedná o vlastnosti charakteristické pro přírodní materiál; c) délkové napojení dýhy na obložce; d) rozdílnou barevnost u použitých přírodních nebo umělých materiálů v případě, že je nutná jejich kombinace z technologických důvodů v rámci jednoho výrobku nebo více výrobků tvořících komplet; e) dodání předmět koupě nebo jeho provedení dodané na základě kupujícím potvrzené chybné závazné nabídky nebo kupujícím potvrzené chyby v kupní smlouvě.",
        "48": "Ve sporných případech vad předmětu koupě způsobených relativní vlhkostí vzduchu (vysokou i nízkou) se za rozhodné považuje měření vlhkosti poškozené věci kalibrovaným vlhkoměrem. V případě, že vlhkost konstrukce dveří nebo zárubní se pohybuje mimo rozmezí 6-10 %, má se za to, že předmět koupě nebo jeho část bylo vystaveno nevhodným vlhkostním podmínkám a může docházet k deformacím, za které prodávající nenese odpovědnost.",
        "49": "V případě, že dojde mezi prodávajícím a kupujícím ke vzniku sporu, který se nepodaří vyřešit výše uvedeným způsobem, může kupující podat návrh na mimosoudní řešení takového sporu určenému subjektu mimosoudního řešení spotřebitelských sporů, kterým je Česká obchodní inspekce, Ústřední inspektorát - oddělení ADR, Štěpánská 15, 120 00 Praha 2, e-mail: adr@coi.cz, web: adr.coi.cz.",
        "51": "Smluvní strany se zavazují, že v případě, kdy dojde k podstatnému snížení možnosti plnění této smlouvy jednou ze stran, se smluvní strany dohodnou na novém znění této smlouvy, které bude odpovídat aktuálním možnostem plnění předmětu této smlouvy smluvními stranami. V případě, že nebude možné se dohodnout na změně této smlouvy, je smluvní strana postižená změnou okolností dle výše uvedeného oprávněna od této smlouvy odstoupit, aniž by měla druhá smluvní strana nárok na náhradní plnění nebo náhradu škody.",
        "52": "Tato smlouva nabude účinnosti dnem podpisu smluvními stranami za podmínky. Smluvní strany se dohodly, že podpis smlouvy lze uskutečnit i elektronicky.",
        "53": "Právní vztahy, které nejsou v této smlouvě výslovně upraveny, se řídí příslušnými ustanoveními občanského zákoníku.",
        "54": "Smluvní strany prohlašují, že tato smlouva byla sepsána podle jejich pravé, svobodné a vážné vůle, a že souhlasí s jejím obsahem a zněním.",
    }
    for num, text in cores.items():
        cc = DocumentParagraph.objects.create(
            priority=num[1],
            document_section=DocumentSection.objects.get(priority=num[0], contract_type=koupe),
            contract_type=koupe,
            document_type="contract",
            text=text,
            created_by=user,
        )
    p_cores_default = {
        "3": "Záruční doba je obvykle 24 měsíců od předání.",
        "4": "Pokud není přílohou této nabídky zaměření, jsou množstevní a cenové údaje pouze orientační a mohou se změnit po provedení zaměření.",
    }
    p_cores_dilo = {
        "2": "Zahájení montáže je možné zpravidla 15 až 20 týdnů od uzavření smlouvy a zaplacení zálohové faktury."
    }
    p_cores_koupe = {
        "2": "Dodání předmětu nabídky je možné zpravidla 15 až 20 týdnů od uzavření smlouvy a zaplacení zálohové faktury."
    }

    for num, text in p_cores_default.items():
        cc = DocumentParagraph.objects.create(
            priority=num,
            document_type="proposal",
            text=text,
            created_by=user,
        )

    for num, text in p_cores_dilo.items():
        cc = DocumentParagraph.objects.create(
            priority=num,
            document_type="proposal",
            text=text,
            contract_type=dilo,
            created_by=user,
        )

    for num, text in p_cores_koupe.items():
        cc = DocumentParagraph.objects.create(
            priority=num,
            document_type="proposal",
            text=text,
            contract_type=koupe,
            created_by=user,
        )

    # # default attachments not working
    # with open('default_attachment.txt', 'w') as file:
    #     file.write(
    #         'Tato příloha je vzor přílohy, která je přiřazena automaticky při vzniku dokumentu, což mohou být např. '
    #         'obchodní podmínky nebo podmínky používání. Takže už nemusíte myslet na to je k nabídce či smlouvě vždy'
    #         'přiložit.')
    #
    # default_attachment = DefaultAttachment.objects.create(
    #     tag="Obchodní podmínky Demo s.r.o.",
    #     file_name=file.name,
    #     purpose="both",
    #     file=file,
    # )
    # default_attachment.subject.add(ContractSubject.objects.all())
    # default_attachment.contract_type.add(ContractType.objects.all())

    return Operator.objects.filter()
