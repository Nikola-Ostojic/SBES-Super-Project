from sqlalchemy import create_engine, select, MetaData, Table
from sqlalchemy.orm import Session, sessionmaker
from db_models import Result, Base, Factor, CheckedItem, SelectedItem
from models import Answer
import os
from logging import info, error
import hashlib
import copy


def get_db_engine():
    engine = create_engine('mysql+mysqlconnector://{}:{}@db:3306/{}'
                           .format(os.getenv('MYSQL_USER'),
                                   os.getenv('MYSQL_PASSWORD'),
                                   os.getenv('MYSQL_DATABASE')))
    return engine


def init_tables(engine):
    Base.metadata.create_all(engine)


def write_to_database(engine, result: Result, factor:Factor, all_answers:list[Answer], selected_answers:list[Answer]):
    result.Factor = factor

    session = sessionmaker(engine)

    with session.begin() as s:
        all_anw = convert_answers_to_chkim(all_answers)
        for anw in all_anw:
            print("WRITING TO DATABASE 4", flush=True)
            chk_item = check_if_checked_item_exists_in_db(s, anw.Id)

            if not chk_item:
                print("WRITING TO DATABASE 6", flush=True)
                s.add(anw)


        print("WRITING TO DATABASE", flush=True)

    session = sessionmaker(engine)

    with session.begin() as s:
        s.add(result)
        print("PART TWO ", flush=True)
        all_checked = get_all_checked_items(s)
        for sl_anw in selected_answers:
            item = find_item_with_hash(all_checked, sl_anw)
            if item:
                si = SelectedItem()
                si.CheckedItemId = item.Id
                si.Result = result
                s.add(si)


def hash_text(text:str):
    h = hashlib.sha256()
    h.update(bytes(text, 'UTF-8'))
    return h.hexdigest()


def convert_answers_to_chkim(answers: list[Answer]) -> list[CheckedItem]:
    res = []
    for anw in answers:
        print("ANSWER : " + anw.text, flush=True)
        chk = CheckedItem()
        chk.Text = anw.text
        chk.Id = hash_text(anw.text)
        res.append(chk)

    return res


def find_item_with_hash(all_checked_items: list[CheckedItem], sel_answer: Answer) -> CheckedItem|None:
    sel_hash = hash_text(sel_answer.text)
    print("FINDING ITEM WITH HASH: " + str(sel_hash), flush=True)
    for anw in all_checked_items:
        print("ANW ID " + str(anw.Id), flush=True)
        if anw.Id == sel_hash:
            return anw

    return None

def check_if_checked_item_exists_in_db(session, id) -> CheckedItem|None:
    check_item = session.query(CheckedItem).filter(CheckedItem.Id == id).first()
    return check_item


def get_all_checked_items(session) -> list[CheckedItem]:
    checked_list = session.query(CheckedItem).all()
    return checked_list



