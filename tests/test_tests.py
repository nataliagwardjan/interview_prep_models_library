import unittest
from uuid import uuid4
from pydantic import ValidationError
from models import (TestCreateSchema,
                    QuestionCreateSchema,
                    QuestionSchema,
                    AnswerCreateSchema,
                    AnswerSchema,
                    TestSchema,
                    Level,
                    QuestionType)


class TestTestWithUnitTest(unittest.TestCase):

    def test_test_create_schema_valid(self):
        """Test for valid TestCreateSchema"""
        test_create = TestCreateSchema(
            user_id='3f97fc69-9253-40c2-94c7-f8307ff70309',
            position='Software Developer',
            level=Level.JUNIOR,
            number_of_question=20,
            type_of_question=[QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE],
            skills_or_tools=['Python', 'Django']
        )
        self.assertEqual(str(test_create.user_id), '3f97fc69-9253-40c2-94c7-f8307ff70309')
        self.assertEqual(test_create.position, 'Software Developer')
        self.assertEqual(test_create.level, Level.JUNIOR)
        self.assertEqual(len(test_create.type_of_question), 2)
        self.assertIn(QuestionType.TRUE_FALSE, test_create.type_of_question)
        self.assertIn(QuestionType.SINGLE_CHOICE, test_create.type_of_question)
        self.assertEqual(test_create.skills_or_tools, ['Python', 'Django'])

    def test_test_create_schema_invalid_type_of_question(self):
        """Test for TestCreateSchema with non-unique type_of_question"""
        with self.assertRaises(ValidationError) as context:
            TestCreateSchema(
                user_id='3f97fc69-9253-40c2-94c7-f8307ff70309',
                position='Software Developer',
                level=Level.JUNIOR,
                number_of_question=20,
                type_of_question=[QuestionType.TRUE_FALSE, QuestionType.TRUE_FALSE],
                skills_or_tools=['Python', 'Django']
            )
        self.assertIn('Question types must contain unique elements.', str(context.exception))

    def test_test_create_schema_with_missing_field(self):
        """Test for TestCreateSchema with missing field"""
        test_cases = [(
            {
                'position': 'Software Developer',
                'level': Level.JUNIOR,
                'number_of_question': 20,
                'type_of_question': [QuestionType.TRUE_FALSE,
                                     QuestionType.SINGLE_CHOICE],
                'skills_or_tools': ['Python', 'Django']
            },
            'user_id'),
            (
                {
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'level': Level.JUNIOR,
                    'number_of_question': 20,
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'skills_or_tools': ['Python', 'Django']
                },
                'position'),
            (
                {
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'position': 'Software Developer',
                    'number_of_question': 20,
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'skills_or_tools': ['Python', 'Django']
                },
                'level'),
            (
                {
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'position': 'Software Developer',
                    'level': Level.JUNIOR,
                    'number_of_question': 20,
                    'skills_or_tools': ['Python', 'Django']
                },
                'type_of_question')
        ]
        for test_case in test_cases:
            data = test_case[0]
            missing_field = test_case[1]
            with self.assertRaises(ValidationError) as context:
                TestCreateSchema(**data)
            self.assertEqual((context.exception.errors()[0]['loc'][0]), missing_field)
            self.assertEqual((context.exception.errors()[0]['type']), 'missing')

    def test_test_schema_valid(self):
        """Test for valid TestSchema"""
        question = QuestionSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70301',
            test_id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            question_number=1,
            question_text='Example question text',
            question_type=QuestionType.TRUE_FALSE,
            possible_answers={
                'A': 'TRUE',
                'B': 'FALSE'
            },
            correct_answers=['B']
        )
        test1 = TestSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            user_id='3f97fc69-9253-40c2-94c7-f8307ff70309',
            position='Software Developer',
            type_of_question=[QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE],
            level=Level.JUNIOR,
            is_solved=False,
            questions=[question],
            answers=[],
            skills_or_tools=['Python', 'Django']
        )
        test2 = TestSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            user_id='3f97fc69-9253-40c2-94c7-f8307ff70309',
            position='Software Developer',
            type_of_question=[QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE],
            level=Level.JUNIOR,
            questions=[question]
        )
        self.assertEqual(str(test1.user_id), '3f97fc69-9253-40c2-94c7-f8307ff70309')
        self.assertEqual(str(test1.id), '3f97fc69-9253-40c2-94c7-f8307ff70302')
        self.assertEqual(test1.position, 'Software Developer')
        self.assertEqual(len(test1.questions), 1)
        self.assertEqual(test1.skills_or_tools, ['Python', 'Django'])
        self.assertEqual(test1.level, Level.JUNIOR)
        self.assertEqual(str(test2.user_id), '3f97fc69-9253-40c2-94c7-f8307ff70309')
        self.assertEqual(str(test2.id), '3f97fc69-9253-40c2-94c7-f8307ff70302')
        self.assertEqual(test2.position, 'Software Developer')
        self.assertEqual(len(test2.questions), 1)
        self.assertEqual(test1.level, Level.JUNIOR)

    def test_test_schema_with_missing_field(self):
        """Test for TestSchema without all required fields"""
        question = QuestionSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70301',
            test_id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            question_number=1,
            question_text='Example question text',
            question_type=QuestionType.TRUE_FALSE,
            possible_answers={
                'A': 'TRUE',
                'B': 'FALSE'
            },
            correct_answers=['B']
        )
        test_cases = [(
            {
                'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                'position': 'Software Developer',
                'type_of_question': [QuestionType.TRUE_FALSE,
                                     QuestionType.SINGLE_CHOICE],
                'level': Level.JUNIOR,
                'is_solved': False,
                'questions': [question],
                'answers': [],
                'skills_or_tools': ['Python', 'Django']
            },
            'id'),
            (
                {
                    'id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
                    'position': 'Software Developer',
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'level': Level.JUNIOR,
                    'is_solved': False,
                    'questions': [question],
                    'answers': [],
                    'skills_or_tools': ['Python', 'Django']
                },
                'user_id'),
            (
                {
                    'id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'position': 'Software Developer',
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'is_solved': False,
                    'questions': [question],
                    'answers': [],
                    'skills_or_tools': ['Python', 'Django']
                },
                'level'),
            (
                {
                    'id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'level': Level.JUNIOR,
                    'is_solved': False,
                    'questions': [question],
                    'answers': [],
                    'skills_or_tools': ['Python', 'Django']
                },
                'position'),
            (
                {
                    'id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'position': 'Software Developer',
                    'type_of_question': [QuestionType.TRUE_FALSE,
                                         QuestionType.SINGLE_CHOICE],
                    'level': Level.JUNIOR,
                    'is_solved': False,
                    'answers': [],
                    'skills_or_tools': ['Python', 'Django']
                },
                'questions'),
            (
                {
                    'id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
                    'user_id': '3f97fc69-9253-40c2-94c7-f8307ff70309',
                    'position': 'Software Developer',
                    'questions': [question],
                    'level': Level.JUNIOR,
                    'is_solved': False,
                    'answers': [],
                    'skills_or_tools': ['Python', 'Django']
                },
                'type_of_question')
        ]
        for test_case in test_cases:
            data = test_case[0]
            missing_field = test_case[1]
            with self.assertRaises(ValidationError) as context:
                TestSchema(**data)
            self.assertEqual((context.exception.errors()[0]['loc'][0]), missing_field)
            self.assertEqual((context.exception.errors()[0]['type']), 'missing')

    def test_question_create_schema_valid(self):
        """Test for valid QuestionCreateSchema"""
        create_question = {
            'test_id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
            'question_number': 1,
            'question_text': 'What is Python?',
            'question_type': QuestionType.SINGLE_CHOICE,
            'possible_answers': {'A': 'Dog',
                                 'B': 'Programing Language',
                                 'C': 'Snake'},
            'correct_answers': ['B']
        }
        schema = QuestionCreateSchema(**create_question)
        self.assertEqual(schema.question_text, 'What is Python?')
        self.assertEqual(schema.question_type, QuestionType.SINGLE_CHOICE)
        self.assertEqual(schema.question_number, 1)
        self.assertEqual(len(schema.correct_answers), 1)
        self.assertEqual(len(schema.possible_answers), 3)

    def test_answer_create_schema_valid(self):
        """Test for valid AnswerCreateSchema"""
        data = {
            'question_id': '3f97fc69-9253-40c2-94c7-f8307ff70302',
            'answer_choice': ['A', 'B']
        }
        schema = AnswerCreateSchema(**data)
        self.assertEqual(len(schema.answer_choice), 2)

    def test_test_schema_with_questions_and_answers(self):
        """Test for valid TestSchema with questions and answers"""
        question = QuestionSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70301',
            test_id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            question_number=1,
            question_text='Example question text',
            question_type=QuestionType.TRUE_FALSE,
            possible_answers={
                'A': 'TRUE',
                'B': 'FALSE'
            },
            correct_answers=['B']
        )
        answer = AnswerSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70301',
            question_id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            answer_choice=['A']
        )
        schema = TestSchema(
            id='3f97fc69-9253-40c2-94c7-f8307ff70302',
            user_id='3f97fc69-9253-40c2-94c7-f8307ff70309',
            position='Software Developer',
            type_of_question=[QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE],
            level=Level.JUNIOR,
            is_solved=False,
            questions=[question],
            answers=[answer],
            skills_or_tools=['Python', 'Django']
        )
        self.assertEqual(len(schema.questions), 1)
        self.assertEqual(len(schema.answers), 1)
        self.assertEqual(schema.position, 'Software Developer')
        self.assertEqual(schema.level, Level.JUNIOR)


if __name__ == '__main__':
    unittest.main()
