import json
from data import CDS_DATA_PATH
import random

with open(CDS_DATA_PATH, 'r') as f:
    CDS_DATA = json.load(f)

AGE_INTERNAL_TO_DISPLAY_MAPPING = {'birth': 'Birth',
                                   '6_weeks': '6 weeks',
                                   '3_months': '3 months',
                                   '6_months': '6 months',
                                   '9_months': '9 months',
                                   '12_months': '12 months',
                                   '18_months': '18 months',
                                   '2_years': '2 years',
                                   '3_years': '3 years',
                                   '4_years': '4 years',
                                   '5_years': '5 years'}

DOMAIN_INTERNAL_TO_DISPLAY_MAPPING = {'gross_motor': 'Gross Motor',
                                      'vision_fine_motor': 'Vision/Fine Motor',
                                      'hearing_speech_recep': 'Hearing/Speech and Language (Receptive ability)',
                                      'hearing_speech_expressive': 'Hearing/Speech and Language (Expressive ability)',
                                      'socio_emotional': 'Socio Emotional'}


def get_wrong_answers(correct_age: str, domain: str, cds_data: dict[str, dict[str, list[str]]]) -> list[str]:
    ages = list(cds_data.keys())
    ages_to_take = [age for age in ages if age != correct_age]
    wrong_answers = []
    for age in ages_to_take:
        wrong_answers.extend(cds_data[age][domain])
    return random.sample(wrong_answers, 3)


def build_dev_milestone_question(correct_ans: str, wrong_answers: list[str], age: str, domain: str) -> dict[str, str]:
    question_data = {'age': age, 'domain': domain, 'type': 'dev_milestone'}
    correct_choice = random.randint(1, 4)
    available_wrong_answers = wrong_answers.copy()
    for i in range(1, 5):
        if i == correct_choice:
            question_data[str(i)] = correct_ans
            question_data['correct'] = str(i)
        else:
            wrong_answer = random.choice(available_wrong_answers)
            available_wrong_answers.remove(wrong_answer)
            question_data[str(i)] = wrong_answer
    return question_data


def display_dev_milestone_question(question_data: dict[str, str]) -> None:
    display_age = AGE_INTERNAL_TO_DISPLAY_MAPPING[question_data['age']]
    display_domain = DOMAIN_INTERNAL_TO_DISPLAY_MAPPING[question_data['domain']]
    print(f'Child\'s age: {display_age}')
    print(f'Pick the correct developmental milestone for the domain: {display_domain}')
    for i in range(1, 5):
        print(f'{i}. {question_data[str(i)]}')
    print('\ne: Exit exercise')


def test_question(question_data: dict[str, str]) -> bool:
    if question_data['type'] == 'dev_milestone':
        display_dev_milestone_question(question_data)
    while True:
        player_input = input().strip()
        if player_input == question_data['correct']:
            print('Correct!')
            return False
        elif player_input in [str(i) for i in range(1, 5)]:
            print(f'Sorry, the correct answer was {question_data[question_data["correct"]]}')
            return False
        elif player_input.lower() == 'e':
            print('Exercise terminated.')
            return True
        else:
            print('Unrecognized input. Try again.')