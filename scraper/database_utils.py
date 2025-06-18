from people.models import Person

def save_to_database(parsed_data):
    person = Person(
        name=parsed_data['name'],
        url=parsed_data['url'],
        date_of_birth=parsed_data.get('date_of_birth'),
        date_of_death=parsed_data.get('date_of_death'),
        ethnicity=parsed_data.get('ethnicity'),
        hometown=parsed_data['details'].get('hometown'),
        date_entered_party=parsed_data.get('date_entered_party'),
        date_entered_party_official=parsed_data.get('date_entered_party_official'),
        expertise=parsed_data.get('expertise'),
        degree_education=parsed_data['details'].get('degree_education'),
        political_theory=parsed_data['details'].get('political_theory'),
        foreign_language=parsed_data['details'].get('foreign_language'),
        position=parsed_data['details'].get('position'),
        position_process=parsed_data['details'].get('position_process')
    )
    person.save()
