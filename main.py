import psycopg2
import configparser
import database as db


def test_bd(f_database, f_user, f_password):
    conn = psycopg2.connect(database=f_database, user=f_user, password=f_password)
    test_data = {'f_name': 'Дамир', 'l_name': 'Идиятулин', 'email': 'damiraсer@supra.a80'}

    # Создать таблицы
    db.create_db(conn)

    # Добавить данные клиента
    db.insert_client(conn, **test_data)

    # Получить id клиента
    id_new_client = db.get_client_id(conn, **test_data)

    # Добавить телефон клиента.
    db.insert_phone(conn, id_new_client, phone='8-800-000-00-00')
    db.insert_phone(conn, id_new_client, phone='8-999-999-99-99')

    # Поиск клиента по его данным (имени, фамилии, email или телефону). Пример поиска по телефону.
    res1 = db.find_client(conn, number='8-999-999-99-99')[0]
    assert res1 == ('Дамир', 'Идиятулин', 'damiraсer@supra.a80', '8-999-999-99-99')
    print(f'Имя, фамилия: {res1[0]} {res1[1]}', f'Email: {res1[2]}', f'Телефон: {res1[3]}', sep='\n')

    # Изменить данные клиента
    db.change_client(conn, id_new_client, email='damir@racer.a80')
    test_data['email'] = 'damir@racer.a80'

    # Получить id клиента с учётом обновлённых данных.
    id_client = db.get_client_id(conn, **test_data)

    # Поиск клиента по его данным (имени, фамилии, email или телефону). Пример поиска по фамилии.
    res2 = db.find_client(conn, l_name='Идиятулин')
    correct_res = [
        ('Дамир', 'Идиятулин', 'damir@racer.a80', '8-800-000-00-00'),
        ('Дамир', 'Идиятулин', 'damir@racer.a80', '8-999-999-99-99')
    ]
    for res_find_client_item, correct_res_item in zip(
            res2, correct_res
    ):
        assert res_find_client_item == correct_res_item

    # Удалить телефон клиента.
    db.delete_phone(conn, id_client,'8-800-000-00-00')
    db.delete_phone(conn, id_client, '8-999-999-99-99')

    # Удалить все данные клиента из таблиц.
    result = db.delete_client(conn, id_client)
    assert result == None
    conn.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    database = config['Settings']['database']
    user = config['Settings']['user']
    password = config['Settings']['password']
    test_bd(database, user, password)





