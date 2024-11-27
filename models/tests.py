from pydantic import BaseModel, Field, conint, field_validator
from enum import Enum
from typing import List, Optional
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
    @classmethod
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
    possible_answers: List[str] = Field(..., min_items=1)
    correct_answers: List[str] = Field(..., min_items=1)


class QuestionSchema(BaseModel):
    id: UUID
    test_id: UUID
    question_number: int
    question_text: str
    possible_answers: List[str] = Field(..., min_items=1)
    correct_answers: List[str] = Field(..., min_items=1)


class AnswerCreateSchema(BaseModel):
    question_id: UUID
    answer_choice: List[str] = []


class AnswerSchema(BaseModel):
    id: UUID
    question_id: UUID
    answer_choice: List[str] = []


class TestSchema(BaseModel):
    id: UUID
    user_id: UUID
    position: str
    level: Level
    skills_or_tools: Optional[List[str]] = None
    is_solved: bool = False
    questions: List[QuestionSchema] = Field(..., min_items=1)
    answers: List[AnswerSchema] = []
    result: Optional[float] = None
