from dataclasses import dataclass

from google.maps.addressvalidation_v1.types.address_validation_service import (
    ValidationResult,
)


ADDRESS_CONFIRMATION_THRESHOLD = 2

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
    def is_suspicious(self) -> bool:
        suspicious_components = dict()
        for component in self.validation_result.address.address_components:
            component_text: str = component.component_name.text
            confirmation_level_numeric: int = component.confirmation_level.value
            confirmation_level_text = str(component.confirmation_level)
            if confirmation_level_numeric > ADDRESS_CONFIRMATION_THRESHOLD:
                print(component)
                suspicious_components[confirmation_level_text] = component_text
        is_suspicious = bool(suspicious_components)
        if is_suspicious:
            print(f"Suspicious Address Components: {suspicious_components}")
        return is_suspicious
