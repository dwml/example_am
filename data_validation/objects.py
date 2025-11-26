from pydantic import BaseModel, field_validator, Field
import pandera.pandas as pa
from pandera.engines.pandas_engine import PydanticModel

_final_class_mapping = {
    "resillient": 0,
    "delayed": 1,
    "recovery": 2,
    "chronic": 3,
}

_amnesia_mapping = {
    "nee": 0,
    "ja": 1,
}

class _Subject(BaseModel):
    # identification number
    id: int | float = Field(validation_alias="PIN")
    age: int = Field(validation_alias="D_age")
    sex: int
    final_class: int = Field(validation_alias="Finalclass")
    caps5_total: int = Field(validation_alias="CAPS5_Totalscore")
    overall_stress: int = Field(validation_alias="overall.stress")
    stressors: int
    impact_of_prior_traumatic_events: int = Field(validation_alias="impact.of.prior.traumatic.events")
    age_at_admission_to_emergency_department: int = Field(validation_alias="Age.at.ED")
    amnesia: int
    prior_traumatic_events: int = Field(validation_alias="prior.traumatic.events")
    LEC5_total: int

    # Use field validator to validate the entries in certain fields
    # Due to time constraints I just validate a few entries and remove
    # any entries that are not within bound or are empty
    @field_validator("age")
    def must_be_over_eighteen(cls, value: int) -> int:
        if 130 < value < 18:
            raise ValueError("Number must be over 18 and lower than 130.")
        return value
    
    @field_validator("sex")
    def must_be_one_or_two(cls, value: int) -> int:
        if value not in [1, 2]:
            raise ValueError("Number must be 1 or 2.")
        return value
    
    @field_validator("age_at_admission_to_emergency_department", mode="before")
    def must_be_over_eighteen_and_round(cls, value: int | float) -> int:
        if 130 < value < 18:
            raise ValueError("Number must be over 18 and lower than 130.")
        return int(round(value))

    
    @field_validator("final_class", mode="before")
    def must_be_in_final_class_mapping(cls, value: str) -> int:
        if value not in _final_class_mapping.keys():
            return ValueError(f"Must be one of: {_final_class_mapping.keys()}")
        return _final_class_mapping[value]
    
    @field_validator("amnesia", mode="before")
    def must_be_in_amnesia_mapping(cls, value: str) -> int:
        if value not in _amnesia_mapping.keys():
            return ValueError(f"Must be one of: {_amnesia_mapping.keys()}")
        return _amnesia_mapping[value]

class SubjectSchema(pa.DataFrameModel):
    """Schema"""

    class Config:
        """Config"""

        dtype=PydanticModel(_Subject)
        coerce=True