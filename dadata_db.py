import sqlite3


def create_db():
    try:
        dadata_db = sqlite3.connect('dadata_settings.db')
        cursor = dadata_db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Settings(
        [base_url] text NOT NULL,
        [api_key] text NOT NULL,
        [language] text DEFAULT 'ru' NOT NULL
        );
        """)
        dadata_db.commit()
        cursor.close()
    except sqlite3.Error as ex:
        print('Ошибка при подключении к sqlite: ', ex)
    finally:
        if(dadata_db):
            dadata_db.close()


def add_table_values(api_key, language):
    try: 
        dadata_db = sqlite3.connect('dadata_settings.db')
        cursor = dadata_db.cursor()
        settings = """
        INSERT INTO Settings VALUES(
        'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/%s',
        :api_key,
        :language
        );
        """
        cursor.execute(settings, {'api_key': api_key, 'language': language})
        settings = cursor.execute('SELECT * FROM Settings').fetchone()
        return settings
    except sqlite3.Error as ex:
        print('Ошибка при подключении к sqlite: ', ex)
    finally:
        if(dadata_db):
            cursor.close()
            dadata_db.close()
