from pydantic import BaseModel, Field, conint, field_validator, model_validator
from enum import Enum
from typing import List, Optional, Dict
from uuid import UUID


class Level(str, Enum):
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"
    EXPERT = "EXPERT"


class QuestionType(str, Enum):
    TRUE_FALSE = "TRUE FALSE"
    SINGLE_CHOICE = "SINGLE CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE CHOICE"


class TestCreateSchema(BaseModel):
    user_id: UUID
    position: str = Field(..., max_length=100)
    level: Level
    number_of_question: conint(ge=1, le=50) = 20
    type_of_question: List[QuestionType] = Field(..., min_items=1)
    skills_or_tools: Optional[List[str]] = None

    @field_validator("type_of_question")
    def unique_question_types(cls, value: List[QuestionType]) -> List[QuestionType]:
        """
        Check if elements are unique
        """
        if len(value) != len(set(value)):
            raise ValueError("Question types must contain unique elements.")
        return value


class QuestionCreateSchema(BaseModel):
    test_id: UUID
    question_number: int
    question_text: str
    question_type: QuestionType
    possible_answers: Dict[str, str] = Field(..., min_items=2)
    correct_answers: List[str] = Field(..., min_items=1)

    @model_validator(mode="after")
    def validate_answers(self):
        """
        Checks the validity of the relationship between possible_answers and correct_answers.
        """
        invalid_keys = [key for key in self.correct_answers if key not in self.possible_answers]
        if invalid_keys:
            raise ValueError(f"Invalid keys in correct_answers: {invalid_keys}")

        if self.question_type == QuestionType.TRUE_FALSE and len(self.possible_answers) != 2:
            raise ValueError("For TRUE_FALSE question, possible answers have only two options: TRUE or FALSE")

        if self.question_type in {QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE}:
            if len(self.correct_answers) != 1:
                raise ValueError(f"For question_type '{self.question_type}' requires exactly one correct answer.")

        return self


class QuestionSchema(QuestionCreateSchema):
    id: UUID


class AnswerCreateSchema(BaseModel):
    question_id: UUID
    answer_choice: List[str] = []


class AnswerSchema(AnswerCreateSchema):
    id: UUID


class TestSchema(TestCreateSchema):
    id: UUID
    is_solved: bool = False
    questions: List[QuestionSchema] = Field(..., min_items=1)
    answers: List[AnswerSchema] = []
    result: Optional[float] = None
