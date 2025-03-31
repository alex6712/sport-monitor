from pydantic import Field, EmailStr

from .standard import StandardResponse


class AppInfoResponse(StandardResponse):
    """Application information request response model.

    See ``StandardResponse`` for information about inherited attributes.

    See Also
    --------
    .standard.StandardResponse

    Attributes
    ----------
    app_name : str
        The name of the application.
    app_version : str
        The current version of the application.
    app_description : str
        Full description of the application.
    app_summary : str
        Brief description of the application.
    admin_name : str
        Name of the person responsible.
    admin_email : str
        Email address to contact the person in charge.
    """

    app_name: str = Field(examples=["Fast API"])
    app_version: str = Field(examples=["0.0.0"])
    app_description: str = Field(examples=["REST API using FastAPI Python 3.11"])
    app_summary: str = Field(examples=["The best web-application."])
    admin_name: str = Field(examples=["John Doe"])
    admin_email: EmailStr = Field(examples=["john.doe@gmail.com"])
