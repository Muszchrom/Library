import random

books = [
    {
        "isbn": "8324100671",
        "isbn13": "9788324100671",
        "title": "Pan Tadeusz",
        "description": "Epicki poemat, który opisuje życie szlachty w Polsce podczas okupacji napoleońskiej.",
        "publication_date": "1834-06-30",
        "rating": 4.5,
        "author": {
            "first_name": "Adam",
            "second_name": "Mickiewicz"
        },
        "genres": ["Epopeja", "Poemat", "Historyczna"]
    },
    {
        "isbn": "0143111580",
        "isbn13": "9780143111580",
        "title": "Solaris",
        "description": "Powieść o naukowcach badających tajemniczą planetę, na której pojawiają się ich najgłębsze lęki i pragnienia.",
        "publication_date": "1961-11-01",
        "rating": 5,
        "author": {
            "first_name": "Stanisław",
            "second_name": "Lem"
        },
        "genres": ["Science Fiction", "Filozoficzna"]
    },
    {
        "isbn": "8375080701",
        "isbn13": "9788375080701",
        "title": "Lalka",
        "description": "Realistyczna powieść, która przedstawia złożoność miłości, klasy i kapitalizmu w XIX-wiecznej Polsce.",
        "publication_date": "1890-01-01",
        "rating": 5,
        "author": {
            "first_name": "Bolesław",
            "second_name": "Prus"
        },
        "genres": ["Realizm", "Historyczna"]
    },
    {
        "isbn": "1857546571",
        "isbn13": "9781857546571",
        "title": "Rękopis znaleziony w Saragossie",
        "description": "Kompleksowa narracja łącząca wiele opowieści, badająca motywy przeznaczenia, historii i nadprzyrodzonego.",
        "publication_date": "1804-01-01",
        "rating": 5,
        "author": {
            "first_name": "Jan",
            "second_name": "Potocki"
        },
        "genres": ["Gothic", "Fantasy"]
    },
    {
        "isbn": "0141191762",
        "isbn13": "9780141191762",
        "title": "Sklepy cynamonowe",
        "description": "Zbiór opowiadań, które badają życie i tożsamość w okupowanej Polsce.",
        "publication_date": "1934-01-01",
        "rating": 4.0,
        "author": {
            "first_name": "Bruno",
            "second_name": "Schulz"
        },
        "genres": ["Opowiadania", "Surrealizm"]
    },
    {
        "isbn": "1860497761",
        "isbn13": "9781860497761",
        "title": "Pianista",
        "description": "Pamiętnik ukazujący dramatyczne przeżycia żydowskiego pianisty podczas Holokaustu, podkreślający moc muzyki.",
        "publication_date": "1946-01-01",
        "rating": 4.5,
        "author": {
            "first_name": "Władysław",
            "second_name": "Szpilman"
        },
        "genres": ["Pamiętnik", "Historia"]
    },
    {
        "isbn": "8390326315",
        "isbn13": "9788390326315",
        "title": "Ferdydurke",
        "description": "Satyra na polskie społeczeństwo, która bada kwestie tożsamości, dorosłości i absurdalności życia.",
        "publication_date": "1937-01-01",
        "rating": 4.0,
        "author": {
            "first_name": "Witold",
            "second_name": "Gombrowicz"
        },
        "genres": ["Satyra", "Filozoficzna"]
    },
    {
        "isbn": "8375080589",
        "isbn13": "9788375080589",
        "title": "Rodzina Połanieckich",
        "description": "Powieść ukazująca losy rodziny Połanieckich, ich zmagania i życie w polskim społeczeństwie XIX wieku.",
        "publication_date": "1882-01-01",
        "rating": 4.0,
        "author": {
            "first_name": "Henryk",
            "second_name": "Sienkiewicz"
        },
        "genres": ["Literacka", "Historyczna"]
    },
    {
        "isbn": "8375080589",
        "isbn13": "9788375080589",
        "title": "Polski kompleks",
        "description": "Powieść semi-autobiograficzna badająca psychikę Polaków żyjących w cieniu rządów sowieckich, pełna humoru i tragedii.",
        "publication_date": "1977-01-01",
        "rating": 4.5,
        "author": {
            "first_name": "Tadeusz",
            "second_name": "Konwicki"
        },
        "genres": ["Literacka", "Polityczna"]
    },
    {
        "isbn": "7455651532",
        "isbn13": "9788950888865",
        "title": "Mistrz i Małgorzata",
        "description": "Surrealistyczna opowieść o szatanie, który przybywa do Moskwy, by zdemaskować korupcję i zepsucie w sowieckim społeczeństwie.",
        "publication_date": "1967-01-01",
        "rating": 2.5,
        "author": {
            "first_name": "Michaił",
            "second_name": "Bułhakow"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "7535796112",
        "isbn13": "9789742376621",
        "title": "W pustyni i w puszczy",
        "description": "Historia dwójki dzieci, którzy muszą przetrwać w afrykańskiej dżungli.",
        "publication_date": "1911-01-01",
        "rating": 3.5,
        "author": {
            "first_name": "Henryk",
            "second_name": "Sienkiewicz"
        },
        "genres": ["Adventure"]
    },
    {
        "isbn": "3129307675",
        "isbn13": "9785271153386",
        "title": "Harry Potter i Kamień Filozoficzny",
        "description": "Pierwsza książka z serii o młodym czarodzieju.",
        "publication_date": "1997-01-01",
        "rating": 4.5,
        "author": {
            "first_name": "J.K.",
            "second_name": "Rowling"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "2820460146",
        "isbn13": "9784727851237",
        "title": "Władca Pierścieni",
        "description": "Epicka opowieść o podróży hobbita Froda Bagginsa, który próbuje zniszczyć pierścień władzy.",
        "publication_date": "1954-01-01",
        "rating": 4.0,
        "author": {
            "first_name": "J.R.R.",
            "second_name": "Tolkien"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "1096252541",
        "isbn13": "9789665168976",
        "title": "1984",
        "description": "Historia człowieka, który próbuje zbuntować się przeciwko totalitarnemu rządowi.",
        "publication_date": "1949-01-01",
        "rating": 3.9,
        "author": {
            "first_name": "George",
            "second_name": "Orwell"
        },
        "genres": ["Dystopian Fiction"]
    },
    {
        "isbn": "6224307550",
        "isbn13": "9789067888569",
        "title": "To",
        "description": "Historia dzieci walczących z potworem prześladującym miasto Derry.",
        "publication_date": "1986-01-01",
        "rating": 1.5,
        "author": {
            "first_name": "Stephen",
            "second_name": "King"
        },
        "genres": ["Horror"]
    },
    {
        "isbn": "7404660649",
        "isbn13": "9786002688609",
        "title": "Dziady",
        "description": "Dramat romantyczny, który bada kwestie patriotyzmu, wolności i nieśmiertelności.",
        "publication_date": "1823-01-01",
        "rating": 2.5,
        "author": {
            "first_name": "Adam",
            "second_name": "Mickiewicz"
        },
        "genres": ["Drama"]
    },
    {
        "isbn": "2335689564",
        "isbn13": "9782644668817",
        "title": "Proces",
        "description": "Alegoryczna opowieść o absurdzie biurokracji i bezsilności jednostki.",
        "publication_date": "1925-01-01",
        "rating": 4.0,
        "author": {
            "first_name": "Franz",
            "second_name": "Kafka"
        },
        "genres": ["Philosophical Novel"]
    },
    {
        "isbn": "6992320427",
        "isbn13": "9788043828555",
        "title": "Lalka",
        "description": "Opowieść o niespełnionej miłości i klasowych podziałach w XIX-wiecznej Warszawie.",
        "publication_date": "1890-01-01",
        "rating": 2.5,
        "author": {
            "first_name": "Bolesław",
            "second_name": "Prus"
        },
        "genres": ["Social Novel"]
    },
    {
        "isbn": "6862167809",
        "isbn13": "9788682565610",
        "title": "Opowieść podręcznej",
        "description": "Dystopijna opowieść o społeczeństwie, w którym kobiety są zmuszane do służby jako rodzicielki.",
        "publication_date": "1985-01-01",
        "rating": 5,
        "author": {
            "first_name": "Margaret",
            "second_name": "Atwood"
        },
        "genres": ["Dystopian Fiction"]
    },
    {
        "isbn": "9759248591",
        "isbn13": "9789706693310",
        "title": "Czerwona królowa",
        "description": "Fantasy o dziewczynie, która odkrywa, że ma zdolność manipulowania ludźmi.",
        "publication_date": "2015-01-01",
        "rating": 2.5,
        "author": {
            "first_name": "Victoria",
            "second_name": "Aveyard"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "7225850115",
        "isbn13": "9784512796499",
        "title": "Zabić drozda",
        "description": "Historia rasizmu i niesprawiedliwości w amerykańskim Południu.",
        "publication_date": "1960-01-01",
        "rating": 3,
        "author": {
            "first_name": "Harper",
            "second_name": "Lee"
        },
        "genres": ["Legal Thriller"]
    },
    {
        "isbn": "2577808070",
        "isbn13": "9788721991591",
        "title": "Wichrowe wzgórza",
        "description": "Dramatyczna opowieść o namiętnej i katastrofalnej miłości.",
        "publication_date": "1847-01-01",
        "rating": 1.5,
        "author": {
            "first_name": "Emily",
            "second_name": "Brontë"
        },
        "genres": ["Gothic Novel"]
    },
    {
        "isbn": "1538036697",
        "isbn13": "9787174446504",
        "title": "Czas burzy",
        "description": "Kontynuacja przygód Geralta z Rivii, bohatera znanej serii Wiedźmin.",
        "publication_date": "2018-01-01",
        "rating": 2,
        "author": {
            "first_name": "Andrzej",
            "second_name": "Sapkowski"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "3869020009",
        "isbn13": "9785446884816",
        "title": "Cień wiatru",
        "description": "Historia młodego pisarza, który odkrywa tajemniczą księgarnię, prowadzącą go do mrocznej przeszłości.",
        "publication_date": "2001-01-01",
        "rating": 3,
        "author": {
            "first_name": "Carlos",
            "second_name": "Ruiz Zafón"
        },
        "genres": ["Mystery"]
    },
    {
        "isbn": "2529170921",
        "isbn13": "9785012350132",
        "title": "Dziewczyna z pociągu",
        "description": "Bestsellerowy thriller psychologiczny o kobiecie, która staje się świadkiem szokującego zdarzenia.",
        "publication_date": "2015-01-01",
        "rating": 1.5,
        "author": {
            "first_name": "Paula",
            "second_name": "Hawkins"
        },
        "genres": ["Thriller"]
    },
    {
        "isbn": "7975826218",
        "isbn13": "9783954038300",
        "title": "Kod Leonarda da Vinci",
        "description": "Thriller o tajemniczym morderstwie, które prowadzi do odkrycia sekretów Kościoła.",
        "publication_date": "2003-01-01",
        "rating": 3.5,
        "author": {
            "first_name": "Dan",
            "second_name": "Brown"
        },
        "genres": ["Thriller"]
    },
    {
        "isbn": "5400372221",
        "isbn13": "9786014152617",
        "title": "Nieodnaleziona",
        "description": "Kryminał o zaginionej dziewczynie i dziennikarzu, który próbuje ją odnaleźć.",
        "publication_date": "2018-01-01",
        "rating": 3,
        "author": {
            "first_name": "Remigiusz",
            "second_name": "Mróz"
        },
        "genres": ["Crime Fiction"]
    },
    {
        "isbn": "4730185804",
        "isbn13": "9785455390140",
        "title": "Outsider",
        "description": "Mroczna opowieść o morderstwie i tajemniczej sile, która stoi za zbrodnią.",
        "publication_date": "2018-01-01",
        "rating": 3.5,
        "author": {
            "first_name": "Stephen",
            "second_name": "King"
        },
        "genres": ["Horror"]
    },
    {
        "isbn": "9499447731",
        "isbn13": "9785774315112",
        "title": "Kroniki Jakuba Wędrowycza",
        "description": "Seria opowiadań o czarodzieju Jakubie Wędrowyczu, który walczy z demonami i innymi nadprzyrodzonymi istotami.",
        "publication_date": "2001-01-01",
        "rating": 3.5,
        "author": {
            "first_name": "Andrzej",
            "second_name": "Pilipiuk"
        },
        "genres": ["Humoristic Fantasy"]
    },
    {
        "isbn": "4488985662",
        "isbn13": "9786392906418",
        "title": "Gra o tron",
        "description": "Pierwsza książka z serii 'Pieśń Lodu i Ognia', opowiadająca o politycznych i wojennych zmaganiach w fikcyjnym świecie.",
        "publication_date": "1996-01-01",
        "rating": 4.5,
        "author": {
            "first_name": "George",
            "second_name": "R. R. Martin"
        },
        "genres": ["Fantasy"]
    },
    {
        "isbn": "1366046764",
        "isbn13": "9781925320744",
        "title": "Zbrodnia i kara",
        "description": "Powieść psychologiczna o młodym studencie, który próbuje usprawiedliwić morderstwo na bazie teorii.",
        "publication_date": "1866-01-01",
        "rating": 5,
        "author": {
            "first_name": "Fiodor",
            "second_name": "Dostojewski"
        },
        "genres": ["Philosophical Novel"]
    },
    {
        "isbn": "3886597589",
        "isbn13": "9788803745536",
        "title": "Dżuma",
        "description": "Powieść przedstawiająca wybuch dżumy w algierskim mieście Oran jako metaforę izolacji i niesprawiedliwości.",
        "publication_date": "1947-01-01",
        "rating": 4,
        "author": {
            "first_name": "Albert",
            "second_name": "Camus"
        },
        "genres": ["Existential Fiction"]
    },
    {
        "isbn": "7935403554",
        "isbn13": "9786664242309",
        "title": "Szachinszach",
        "description": "Biograficzna opowieść o upadku ostatniego Szacha Iranu.",
        "publication_date": "1982-01-01",
        "rating": 1.5,
        "author": {
            "first_name": "Ryszard",
            "second_name": "Kapuściński"
        },
        "genres": ["Biographical Novel"]
    },
    {
        "isbn": "8641461582",
        "isbn13": "9783757495961",
        "title": "Dracula",
        "description": "Klasyczna opowieść o wampirze hrabim Drakula i jego próbach przetrwania w nowoczesnym świecie.",
        "publication_date": "1897-01-01",
        "rating": 2,
        "author": {
            "first_name": "Bram",
            "second_name": "Stoker"
        },
        "genres": ["Gothic Horror"]
    },
    {
        "isbn": "8779396323",
        "isbn13": "9782581916998",
        "title": "Zamek",
        "description": "Alegoria biurokracji i nieustannej walki jednostki z systemem.",
        "publication_date": "1926-01-01",
        "rating": 4,
        "author": {
            "first_name": "Franz",
            "second_name": "Kafka"
        },
        "genres": ["Philosophical Novel"]
    },
    {
        "isbn": "4991647186",
        "isbn13": "9785591305501",
        "title": "Anna Karenina",
        "description": "Historia tragicznej miłości rosyjskiej arystokratki i jej dążeń do znalezienia prawdy o sobie.",
        "publication_date": "1877-01-01",
        "rating": 4,
        "author": {
            "first_name": "Leo",
            "second_name": "Tolstoy"
        },
        "genres": ["Literary Fiction"]
    },
    {
        "isbn": "5800028701",
        "isbn13": "9783287033438",
        "title": "Gra Endera",
        "description": "Młody chłopiec zostaje wciągnięty w intergalaktyczną grę wojenną, mającą na celu obronę Ziemi przed obcymi.",
        "publication_date": "1985-01-01",
        "rating": 4.,
        "author": {
            "first_name": "Orson",
            "second_name": "Scott Card"
        },
        "genres": ["Science Fiction"]
    },
    {
        "isbn": "9566278395",
        "isbn13": "9781311565457",
        "title": "Ślepowidzenie",
        "description": "Badanie natury świadomości i pierwszy kontakt z obcą cywilizacją, które zakwestionuje ludzkie rozumienie rzeczywistości.",
        "publication_date": "2006-01-01",
        "rating": 3,
        "author": {
            "first_name": "Peter",
            "second_name": "Watts"
        },
        "genres": ["Hard Science Fiction"]
    },
    {
        "isbn": "8588952087",
        "isbn13": "9784104556430",
        "title": "Zegarmistrz z Filigree Street",
        "description": "Historia o zegarmistrzu, który otrzymuje tajemniczy zegar, który może przewidzieć przyszłość.",
        "publication_date": "2015-01-01",
        "rating": 2,
        "author": {
            "first_name": "Natasha",
            "second_name": "Pulley"
        },
        "genres": ["Historical Fantasy"]
    },
    {
        "isbn": "8406401213",
        "isbn13": "9787483661530",
        "title": "Podziemny krąg",
        "description": "Powieść o grupie mężczyzn, którzy zakładają klub walki, aby uciec od rutyny życia.",
        "publication_date": "1996-01-01",
        "rating": 5,
        "author": {
            "first_name": "Chuck",
            "second_name": "Palahniuk"
        },
        "genres": ["Contemporary Fiction"]
    },
    {
        "isbn": "8508009993",
        "isbn13": "9782891770781",
        "title": "Rebeka",
        "description": "Młoda kobieta wchodzi w małżeństwo z wdowcem, odkrywając mroczne tajemnice jego poprzedniego życia.",
        "publication_date": "1938-01-01",
        "rating": 2.5,
        "author": {
            "first_name": "Daphne",
            "second_name": "du Maurier"
        },
        "genres": ["Gothic Fiction"]
    },
    {
        "isbn": "1567569458",
        "isbn13": "9784368042743",
        "title": "Miasto złodziei",
        "description": "Podczas oblężenia Leningradu dwóch młodych mężczyzn wyrusza na desperacką misję zdobycia jaj, ryzykując życie.",
        "publication_date": "2008-01-01",
        "rating": 4.5,
        "author": {
            "first_name": "David",
            "second_name": "Benioff"
        },
        "genres": ["Historical Fiction"]
    },
    {
        "isbn": "4989544996",
        "isbn13": "9781649841720",
        "title": "Żelazny Rycerz",
        "description": "Przygoda w świecie pełnym wróżek, potworów i magicznych istot, gdzie główny bohater musi uratować swoją miłość.",
        "publication_date": "2010-01-01",
        "rating": 3.5,
        "author": {
            "first_name": "Julie",
            "second_name": "Kagawa"
        },
        "genres": ["Young Adult Fantasy"]
    }
]