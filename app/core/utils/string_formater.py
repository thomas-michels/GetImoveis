from pydantic import BeforeValidator
from typing_extensions import Annotated
from unidecode import unidecode


MyStr = Annotated[str, BeforeValidator(lambda v: unidecode(v).title())]
