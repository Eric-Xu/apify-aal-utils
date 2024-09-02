from dataclasses import dataclass

from google.maps.addressvalidation_v1.types.address_validation_service import (
    ValidationResult,
)

ADDRESS_CONFIRMATION_THRESHOLD = 2
STREET_NUMBER_KEY = "street_number"
ROUTE_KEY = "route"


@dataclass
class GoogleMapsUspsAddress:
    """
    USPS representation of a US address.

    https://developers.google.com/maps/documentation/address-validation/reference/rest/v1/TopLevel/validateAddress#uspsaddress
    """

    validation_result: ValidationResult

    def __post_init__(self):
        self.first_address_line: str = (
            self.validation_result.usps_data.standardized_address.first_address_line.title()
        )
        self.second_address_line: str = (
            self.validation_result.usps_data.standardized_address.second_address_line.title()
        )
        self.city: str = (
            self.validation_result.usps_data.standardized_address.city.title()
        )
        self.county: str = self.validation_result.usps_data.county.title()
        self.state_code: str = (
            self.validation_result.usps_data.standardized_address.state
        )
        self.zip_code: str = (
            self.validation_result.usps_data.standardized_address.zip_code
        )
        self.zip_code_extension: str = (
            self.validation_result.usps_data.standardized_address.zip_code_extension
        )
        self.country_code: str = "USA"
        self.latitude: float = self.validation_result.geocode.location.latitude
        self.longitude: float = self.validation_result.geocode.location.longitude
        self.long_address: str = self._get_long_address()
        self.short_address: str = self._get_short_address()
        self.unconfirmed_components = (
            self.validation_result.address.unconfirmed_component_types
        )

    def _get_long_address(self) -> str:
        address_lines = ", ".join(
            [l for l in [self.first_address_line, self.second_address_line] if l]
        )
        zip_code_w_extension = "-".join(
            [c for c in [self.zip_code, self.zip_code_extension] if c]
        )
        address = f"{address_lines}, {self.city}, {self.state_code} {zip_code_w_extension}, {self.country_code}"
        return address

    def _get_short_address(self) -> str:
        address_lines = ", ".join(
            [l for l in [self.first_address_line, self.second_address_line] if l]
        )
        address = f"{address_lines}, {self.city}, {self.state_code} {self.zip_code}"
        return address

    def _raise_if_missing(self, component_key: str) -> None:
        exists = False
        for component in self.validation_result.address.address_components:
            if component.component_type == component_key:
                exists = True
        if not exists:
            raise ValueError(f"Missing Address Component Key: '{component_key}'")

    def is_unconfirmed(self) -> bool:
        self._raise_if_missing(ROUTE_KEY)
        self._raise_if_missing(STREET_NUMBER_KEY)
        is_unconfirmed = (
            STREET_NUMBER_KEY in self.unconfirmed_components
            or ROUTE_KEY in self.unconfirmed_components
        )
        if is_unconfirmed:
            print(
                f"The address '{self.short_address}' has unconfirmed components {self.unconfirmed_components}"
            )
        return is_unconfirmed
