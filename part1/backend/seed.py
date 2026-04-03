from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_default_database()

# ---------------------------------------------------------------------------
# Wipe all five collections so the script produces a clean state every run.
# ---------------------------------------------------------------------------

print("Dropping existing collections...")
db.authors.drop()
db.books.drop()
db.members.drop()
db.library_cards.drop()
db.borrows.drop()

# ---------------------------------------------------------------------------
# Authors and their data
# ---------------------------------------------------------------------------

authors_result = db.authors.insert_many([
    {
        "name": "Chimamanda Ngozi Adichie",
        "birth_year": 1977,
        "nationality": "Nigerian",
        "bio": (
            "Adichie was born in Enugu, Nigeria, and grew up in Nsukka. She studied "
            "medicine and pharmacy before leaving for the United States, where she "
            "completed degrees in communication and political science at Eastern "
            "Connecticut State University. Her 2006 novel Half of a Yellow Sun won "
            "the Orange Prize for Fiction. Her 2013 TED talk 'We Should All Be "
            "Feminists' was adapted into a book of the same name and has been widely "
            "distributed in schools across Sweden."
        ),
    },
    {
        "name": "Kazuo Ishiguro",
        "birth_year": 1954,
        "nationality": "British-Japanese",
        "bio": (
            "Ishiguro was born in Nagasaki and moved to the United Kingdom at the age "
            "of five. He studied English and philosophy at the University of Kent and "
            "completed an MA in creative writing at the University of East Anglia. "
            "He was awarded the Nobel Prize in Literature in 2017. The Swedish Academy "
            "described his novels as having 'uncovered the abyss beneath our illusory "
            "sense of connection with the world.' The Remains of the Day won the "
            "Booker Prize in 1989."
        ),
    },
    {
        "name": "John le Carré",
        "birth_year": 1931,
        "nationality": "British",
        "bio": (
            "Born David John Moore Cornwell in Poole, Dorset, le Carré worked for "
            "both MI5 and MI6 before his third novel, The Spy Who Came in from the "
            "Cold, became an international sensation in 1963. He resigned from the "
            "intelligence services to write full time. Graham Greene called the book "
            "'the best spy story I have ever read.' Le Carré published twenty-five "
            "novels over six decades before his death in December 2020."
        ),
    },
    {
        "name": "Haruki Murakami",
        "birth_year": 1949,
        "nationality": "Japanese",
        "bio": (
            "Murakami was born in Kyoto and studied drama at Waseda University in "
            "Tokyo, where he ran a jazz bar for several years before writing his "
            "first novel. His work blends the mundane with the surreal and draws "
            "heavily on Western music and culture. He has been a perennial favourite "
            "for the Nobel Prize in Literature. Norwegian Wood, published in 1987, "
            "sold over four million copies in Japan within its first year."
        ),
    },
    {
        "name": "Hilary Mantel",
        "birth_year": 1952,
        "nationality": "British",
        "bio": (
            "Mantel grew up in Derbyshire and studied law at the London School of "
            "Economics before switching to Sheffield University. She worked as a "
            "social worker in Africa before returning to Britain to write. She is "
            "the only author to have won the Booker Prize twice with the same "
            "series of novels: Wolf Hall in 2009 and Bring Up the Bodies in 2012. "
            "The final volume of the Thomas Cromwell trilogy, The Mirror and the "
            "Light, was published in 2020. She died in September 2022."
        ),
    },
    {
        "name": "Zadie Smith",
        "birth_year": 1975,
        "nationality": "British",
        "bio": (
            "Smith was born in Brent, London, to an English father and a Jamaican "
            "mother. She studied English literature at King's College, Cambridge, "
            "and sold her debut novel White Teeth to Hamish Hamilton while still "
            "a student. The novel won the Whitbread First Novel Award and the "
            "Guardian First Book Award in 2000. She is also a prolific essayist "
            "and has been a professor of creative writing at New York University "
            "since 2010."
        ),
    },
    {
        "name": "Gabriel García Márquez",
        "birth_year": 1927,
        "nationality": "Colombian",
        "bio": (
            "García Márquez was born in Aracataca, Colombia, and studied law at "
            "the National University of Colombia before dropping out to work as a "
            "journalist. He is the central figure of the Latin American literary "
            "boom and the principal practitioner of magical realism. He was awarded "
            "the Nobel Prize in Literature in 1982. One Hundred Years of Solitude "
            "has sold more than fifty million copies and has been translated into "
            "forty-six languages. He died in Mexico City in April 2014."
        ),
    },
])

author_ids = authors_result.inserted_ids
print(f"  Inserted {len(author_ids)} authors.")

# ---------------------------------------------------------------------------
# Books — sixteen real titles across the seven authors.
#
# copies_available reflects actual shelf stock: total copies minus however
# many are currently out on active (unreturned) loans in the borrow records
# below. The comment on each entry shows the arithmetic.
#
# Author index:
#   0 Adichie  |  1 Ishiguro  |  2 le Carré  |  3 Murakami
#   4 Mantel   |  5 Smith     |  6 García Márquez
#
# Five books have never been borrowed and serve as realistic catalog depth:
#   book[2]  Americanah
#   book[5]  Klara and the Sun
#   book[8]  The Constant Gardener
#   book[12] Bring Up the Bodies
#   book[15] Chronicle of a Death Foretold
# ---------------------------------------------------------------------------

books_result = db.books.insert_many([
    # --- Chimamanda Ngozi Adichie ---
    # index 0
    {
        "title": "Purple Hibiscus",
        "author_id": author_ids[0],
        "genre": "Literary Fiction",
        "published_year": 2003,
        "isbn": "978-1-61695-015-5",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # index 1
    {
        "title": "Half of a Yellow Sun",
        "author_id": author_ids[0],
        "genre": "Historical Fiction",
        "published_year": 2006,
        "isbn": "978-1-40009-294-3",
        "copies_available": 1,   # 2 total − 1 active loan
    },
    # index 2 — never borrowed
    {
        "title": "Americanah",
        "author_id": author_ids[0],
        "genre": "Contemporary Fiction",
        "published_year": 2013,
        "isbn": "978-0-30745-592-5",
        "copies_available": 3,   # 3 total − 0 active loans
    },
    # --- Kazuo Ishiguro ---
    # index 3
    {
        "title": "The Remains of the Day",
        "author_id": author_ids[1],
        "genre": "Literary Fiction",
        "published_year": 1989,
        "isbn": "978-0-67973-172-6",
        "copies_available": 2,   # 4 total − 2 active loans
    },
    # index 4
    {
        "title": "Never Let Me Go",
        "author_id": author_ids[1],
        "genre": "Speculative Fiction",
        "published_year": 2005,
        "isbn": "978-1-40004-339-5",
        "copies_available": 1,   # 2 total − 1 active loan
    },
    # index 5 — never borrowed
    {
        "title": "Klara and the Sun",
        "author_id": author_ids[1],
        "genre": "Speculative Fiction",
        "published_year": 2021,
        "isbn": "978-0-59331-817-1",
        "copies_available": 2,   # 2 total − 0 active loans
    },
    # --- John le Carré ---
    # index 6
    {
        "title": "The Spy Who Came in from the Cold",
        "author_id": author_ids[2],
        "genre": "Thriller",
        "published_year": 1963,
        "isbn": "978-0-14331-296-6",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # index 7
    {
        "title": "Tinker Tailor Soldier Spy",
        "author_id": author_ids[2],
        "genre": "Thriller",
        "published_year": 1974,
        "isbn": "978-0-14311-974-5",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # index 8 — never borrowed
    {
        "title": "The Constant Gardener",
        "author_id": author_ids[2],
        "genre": "Thriller",
        "published_year": 2001,
        "isbn": "978-0-74343-120-6",
        "copies_available": 2,   # 2 total − 0 active loans
    },
    # --- Haruki Murakami ---
    # index 9
    {
        "title": "Norwegian Wood",
        "author_id": author_ids[3],
        "genre": "Literary Fiction",
        "published_year": 1987,
        "isbn": "978-0-37570-402-0",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # index 10
    {
        "title": "Kafka on the Shore",
        "author_id": author_ids[3],
        "genre": "Speculative Fiction",
        "published_year": 2002,
        "isbn": "978-1-40007-927-5",
        "copies_available": 1,   # 2 total − 1 active loan
    },
    # --- Hilary Mantel ---
    # index 11
    {
        "title": "Wolf Hall",
        "author_id": author_ids[4],
        "genre": "Historical Fiction",
        "published_year": 2009,
        "isbn": "978-0-31242-998-9",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # index 12 — never borrowed
    {
        "title": "Bring Up the Bodies",
        "author_id": author_ids[4],
        "genre": "Historical Fiction",
        "published_year": 2012,
        "isbn": "978-0-31262-987-1",
        "copies_available": 2,   # 2 total − 0 active loans
    },
    # --- Zadie Smith ---
    # index 13
    {
        "title": "White Teeth",
        "author_id": author_ids[5],
        "genre": "Contemporary Fiction",
        "published_year": 2000,
        "isbn": "978-0-37570-384-9",
        "copies_available": 2,   # 3 total − 1 active loan
    },
    # --- Gabriel García Márquez ---
    # index 14
    {
        "title": "One Hundred Years of Solitude",
        "author_id": author_ids[6],
        "genre": "Magical Realism",
        "published_year": 1967,
        "isbn": "978-0-06088-328-7",
        "copies_available": 3,   # 4 total − 1 active loan
    },
    # index 15 — never borrowed
    {
        "title": "Chronicle of a Death Foretold",
        "author_id": author_ids[6],
        "genre": "Magical Realism",
        "published_year": 1981,
        "isbn": "978-1-40003-471-3",
        "copies_available": 2,   # 2 total − 0 active loans
    },
])

book_ids = books_result.inserted_ids
print(f"  Inserted {len(book_ids)} books.")

# ---------------------------------------------------------------------------
# Members — ten patrons who joined at different points between 2019 and 2024.
# ---------------------------------------------------------------------------

members_result = db.members.insert_many([
    # index 0 — heavy reader, 6 loans across the full history
    {
        "name": "Justin Shen",
        "email": "justinshen@berkeley.edu",
        "joined": datetime(2019, 4, 8),
    },
    # index 1 — moderate reader, 3 loans
    {
        "name": "Sydney Dinh",
        "email": "sydneydinh@berkeley.edu",
        "joined": datetime(2020, 9, 1),
    },
    # index 2 — active reader, currently has 3 books out simultaneously
    {
        "name": "Serena Hu",
        "email": "serenahu@berkeley.edu",
        "joined": datetime(2021, 2, 17),
    },
    # index 3
    {
        "name": "Ariel Shen",
        "email": "arielxshen@berkeley.edu",
        "joined": datetime(2021, 11, 30),
    },
    # index 4 — has borrowed the same book twice
    {
        "name": "Tejas Mundhe",
        "email": "tejas_mundhe@berkeley.edu",
        "joined": datetime(2022, 3, 14),
    },
    # index 5 — suspended card, one overdue loan outstanding
    {
        "name": "Jolin Wang",
        "email": "Jolinwang@berkeley.edu",
        "joined": datetime(2022, 8, 5),
    },
    # index 6
    {
        "name": "Jessie Wang",
        "email": "jessiee_wang@berkeley.edu",
        "joined": datetime(2023, 5, 22),
    },
    # index 7 — newest member, only one loan so far
    {
        "name": "Rishabh Abhishetty",
        "email": "rishabh_abhishetty@berkeley.edu",
        "joined": datetime(2024, 1, 9),
    },
    # index 8 — recently joined, no loans yet
    {
        "name": "Stella Zhao",
        "email": "stellazhao@berkeley.edu",
        "joined": datetime(2024, 6, 3),
    },
    # index 9 — recently joined, no loans yet
    {
        "name": "Caleb Deng",
        "email": "calebdeng@berkeley.edu",
        "joined": datetime(2024, 11, 12),
    },
])

member_ids = members_result.inserted_ids
print(f"  Inserted {len(member_ids)} members.")

# ---------------------------------------------------------------------------
# Library Cards — one per member.
#
# Card numbers are non-sequential as they would be in a real system where
# some numbers belong to lapsed or cancelled accounts. Two cards have
# non-active statuses: Sydney's five-year card has expired, and Jolin's card
# is suspended pending resolution of an overdue loan.
# ---------------------------------------------------------------------------

cards_result = db.library_cards.insert_many([
    {
        "member_id": member_ids[0],
        "card_number": "LIB-00312",
        "issued":  datetime(2019, 4, 8),
        "expires": datetime(2029, 4, 8),
        "status": "active",
    },
    {
        "member_id": member_ids[1],
        "card_number": "LIB-00341",
        "issued":  datetime(2020, 9, 1),
        "expires": datetime(2025, 9, 1),
        "status": "expired",
    },
    {
        "member_id": member_ids[2],
        "card_number": "LIB-00389",
        "issued":  datetime(2021, 2, 17),
        "expires": datetime(2031, 2, 17),
        "status": "active",
    },
    {
        "member_id": member_ids[3],
        "card_number": "LIB-00401",
        "issued":  datetime(2021, 11, 30),
        "expires": datetime(2031, 11, 30),
        "status": "active",
    },
    {
        "member_id": member_ids[4],
        "card_number": "LIB-00418",
        "issued":  datetime(2022, 3, 14),
        "expires": datetime(2032, 3, 14),
        "status": "active",
    },
    {
        "member_id": member_ids[5],
        "card_number": "LIB-00447",
        "issued":  datetime(2022, 8, 5),
        "expires": datetime(2032, 8, 5),
        "status": "suspended",
    },
    {
        "member_id": member_ids[6],
        "card_number": "LIB-00491",
        "issued":  datetime(2023, 5, 22),
        "expires": datetime(2033, 5, 22),
        "status": "active",
    },
    {
        "member_id": member_ids[7],
        "card_number": "LIB-00534",
        "issued":  datetime(2024, 1, 9),
        "expires": datetime(2034, 1, 9),
        "status": "active",
    },
    {
        "member_id": member_ids[8],
        "card_number": "LIB-00561",
        "issued":  datetime(2024, 6, 3),
        "expires": datetime(2034, 6, 3),
        "status": "active",
    },
    {
        "member_id": member_ids[9],
        "card_number": "LIB-00578",
        "issued":  datetime(2024, 11, 12),
        "expires": datetime(2034, 11, 12),
        "status": "active",
    },
])

print(f"  Inserted {len(cards_result.inserted_ids)} library cards.")

# ---------------------------------------------------------------------------
# Borrow records — twenty-six loans written in chronological order.
#
# Patterns visible in this data:
#   - The Spy Who Came in from the Cold is the most-borrowed book (4 loans total)
#   - Justin is the most active reader (6 loans over 3 years)
#   - Rishabh has borrowed only once — he just joined
#   - Jolin has one loan from March 2024 with no return date. This is
#     the overdue record that triggered her card suspension.
#   - Tejas borrowed The Spy Who Came in from the Cold, returned it, then borrowed it
#     again — a realistic repeat-borrow pattern
#   - Serena currently has three books out simultaneously (books 0, 11, 10)
#
# Active loans by book (must match copies_available in the books list above):
#   book[0]  Purple Hibiscus                    → Serena (Jan 2025)          = 1 active
#   book[1]  Half of a Yellow Sun               → Ariel (Feb 2025)           = 1 active
#   book[3]  The Remains of the Day             → Jolin (Mar 2024, overdue)
#                                                  Rishabh (Feb 2025)        = 2 active
#   book[4]  Never Let Me Go                    → Justin (Mar 2025)          = 1 active
#   book[6]  The Spy Who Came in from the Cold  → Tejas (Feb 2025)           = 1 active
#   book[7]  Tinker Tailor Soldier Spy          → Sydney (Mar 2025)          = 1 active
#   book[9]  Norwegian Wood                     → Tejas (Mar 2025)           = 1 active
#   book[10] Kafka on the Shore                 → Serena (Mar 2025)          = 1 active
#   book[11] Wolf Hall                          → Serena (Mar 2025)          = 1 active
#   book[13] White Teeth                        → Jessie (Mar 2025)          = 1 active
#   book[14] One Hundred Years of Solitude      → Jessie (Jan 2025)          = 1 active
# ---------------------------------------------------------------------------

borrows_result = db.borrows.insert_many([

    # --- 2022 ---

    {
        "member_id": member_ids[0],   # Justin — The Spy Who Came in from the Cold
        "book_id":   book_ids[6],
        "borrow_date": datetime(2022, 2, 3),
        "return_date": datetime(2022, 2, 24),
    },
    {
        "member_id": member_ids[1],   # Sydney — The Remains of the Day
        "book_id":   book_ids[3],
        "borrow_date": datetime(2022, 5, 11),
        "return_date": datetime(2022, 6, 1),
    },
    {
        "member_id": member_ids[2],   # Serena — Purple Hibiscus (first borrow)
        "book_id":   book_ids[0],
        "borrow_date": datetime(2022, 9, 7),
        "return_date": datetime(2022, 9, 28),
    },

    # --- 2023 ---

    {
        "member_id": member_ids[0],   # Justin — Tinker Tailor Soldier Spy
        "book_id":   book_ids[7],
        "borrow_date": datetime(2023, 1, 15),
        "return_date": datetime(2023, 2, 5),
    },
    {
        "member_id": member_ids[3],   # Ariel — The Spy Who Came in from the Cold
        "book_id":   book_ids[6],
        "borrow_date": datetime(2023, 3, 22),
        "return_date": datetime(2023, 4, 12),
    },
    {
        "member_id": member_ids[4],   # Tejas — The Remains of the Day
        "book_id":   book_ids[3],
        "borrow_date": datetime(2023, 6, 8),
        "return_date": datetime(2023, 6, 30),
    },
    {
        "member_id": member_ids[0],   # Justin — One Hundred Years of Solitude
        "book_id":   book_ids[14],
        "borrow_date": datetime(2023, 8, 14),
        "return_date": datetime(2023, 9, 4),
    },
    {
        "member_id": member_ids[2],   # Serena — Norwegian Wood
        "book_id":   book_ids[9],
        "borrow_date": datetime(2023, 10, 3),
        "return_date": datetime(2023, 10, 31),
    },
    {
        "member_id": member_ids[6],   # Jessie — White Teeth (first borrow)
        "book_id":   book_ids[13],
        "borrow_date": datetime(2023, 11, 18),
        "return_date": datetime(2023, 12, 9),
    },

    # --- 2024 ---

    {
        "member_id": member_ids[5],   # Jolin — The Remains of the Day (overdue, never returned)
        "book_id":   book_ids[3],
        "borrow_date": datetime(2024, 3, 5),
        "return_date": None,
    },
    {
        "member_id": member_ids[0],   # Justin — Never Let Me Go (first borrow, returned)
        "book_id":   book_ids[4],
        "borrow_date": datetime(2024, 4, 22),
        "return_date": datetime(2024, 5, 13),
    },
    {
        "member_id": member_ids[3],   # Ariel — Wolf Hall
        "book_id":   book_ids[11],
        "borrow_date": datetime(2024, 5, 30),
        "return_date": datetime(2024, 6, 20),
    },
    {
        "member_id": member_ids[4],   # Tejas — The Spy Who Came in from the Cold (first borrow, returned)
        "book_id":   book_ids[6],
        "borrow_date": datetime(2024, 7, 14),
        "return_date": datetime(2024, 8, 4),
    },
    {
        "member_id": member_ids[1],   # Sydney — White Teeth
        "book_id":   book_ids[13],
        "borrow_date": datetime(2024, 9, 3),
        "return_date": datetime(2024, 9, 24),
    },
    {
        "member_id": member_ids[0],   # Justin — Kafka on the Shore
        "book_id":   book_ids[10],
        "borrow_date": datetime(2024, 10, 8),
        "return_date": datetime(2024, 10, 29),
    },

    # --- 2025 (all currently active) ---

    {
        "member_id": member_ids[2],   # Serena — Purple Hibiscus (second borrow)
        "book_id":   book_ids[0],
        "borrow_date": datetime(2025, 1, 6),
        "return_date": None,
    },
    {
        "member_id": member_ids[6],   # Jessie — One Hundred Years of Solitude
        "book_id":   book_ids[14],
        "borrow_date": datetime(2025, 1, 20),
        "return_date": None,
    },
    {
        "member_id": member_ids[3],   # Ariel — Half of a Yellow Sun
        "book_id":   book_ids[1],
        "borrow_date": datetime(2025, 2, 3),
        "return_date": None,
    },
    {
        "member_id": member_ids[4],   # Tejas — The Spy Who Came in from the Cold (second borrow)
        "book_id":   book_ids[6],
        "borrow_date": datetime(2025, 2, 17),
        "return_date": None,
    },
    {
        "member_id": member_ids[7],   # Rishabh — The Remains of the Day
        "book_id":   book_ids[3],
        "borrow_date": datetime(2025, 2, 28),
        "return_date": None,
    },
    {
        "member_id": member_ids[1],   # Sydney — Tinker Tailor Soldier Spy
        "book_id":   book_ids[7],
        "borrow_date": datetime(2025, 3, 10),
        "return_date": None,
    },
    {
        "member_id": member_ids[6],   # Jessie — White Teeth (second borrow)
        "book_id":   book_ids[13],
        "borrow_date": datetime(2025, 3, 15),
        "return_date": None,
    },
    {
        "member_id": member_ids[4],   # Tejas — Norwegian Wood
        "book_id":   book_ids[9],
        "borrow_date": datetime(2025, 3, 18),
        "return_date": None,
    },
    {
        "member_id": member_ids[2],   # Serena — Wolf Hall
        "book_id":   book_ids[11],
        "borrow_date": datetime(2025, 3, 20),
        "return_date": None,
    },
    {
        "member_id": member_ids[0],   # Justin — Never Let Me Go (second borrow)
        "book_id":   book_ids[4],
        "borrow_date": datetime(2025, 3, 21),
        "return_date": None,
    },
    {
        "member_id": member_ids[2],   # Serena — Kafka on the Shore
        "book_id":   book_ids[10],
        "borrow_date": datetime(2025, 3, 22),
        "return_date": None,
    },
])

print(f"  Inserted {len(borrows_result.inserted_ids)} borrow records.")
print("\nSeed complete. All five collections are ready.")
