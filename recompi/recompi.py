import requests
from hashlib import sha256


class RecomPIException(Exception):
    """
    General exception class for RecomPI errors.
    """

    def __init__(self, *args):
        """
        Initialize RecomPIException with custom arguments.

        Args:
            *args: Variable length argument list.
        """
        super(RecomPIException, self).__init__(*args)


class RecomPIFieldTypeError(RecomPIException):
    """
    Exception raised for errors in the input field type.

    Attributes:
        op (str): The operation where the error occurred.
        field (str): The name of the field with the error.
        value (object): The value that caused the error.
        target_class (type): The expected type of the value.
    """

    def __init__(self, op, field, value, target_class):
        """
        Initialize RecomPIFieldTypeError with operation details and type information.

        Args:
            op (str): Operation where the error occurred.
            field (str): Field name causing the error.
            value (object): The value causing the error.
            target_class (type): The expected type of the value.
        """
        super(RecomPIFieldTypeError, self).__init__(
            "In `%s` operation expecting the `%s` to be an instance of `%s`; but got an instance of `%s`"
            % (op, field, target_class, value.__class__)
        )

    @classmethod
    def if_not_validated(cls, op, name, value, as_, is_array=False):
        """
        Validate the type of the input field.

        Args:
            op (str): Operation name.
            name (str): Field name.
            value (object): Value to validate.
            as_ (type): Expected type of the value.
            is_array (bool, optional): Whether the value is expected to be a list of `as_`.

        Raises:
            RecomPIFieldTypeError: If value is not of expected type.
        """
        if not isinstance(value, list if is_array else as_):
            raise RecomPIFieldTypeError(op, name, value, list if is_array else as_)

        if is_array:
            for index, val in enumerate(value):
                if not isinstance(val, as_):
                    raise RecomPIFieldTypeError(
                        "push", "%s[%d]" % (name, index), val, as_
                    )


class Tag(object):
    """
    Represents a tag with id, name, and description attributes.

    Attributes:
        id (int or None): ID of the tag.
        name (str or None): Name of the tag.
        desc (str or None): Description of the tag, defaults to `name` if not provided.

    Methods:
        __init__(id, name, desc=None):
            Initializes a Tag instance with required `id` and `name`, and optional `desc`.

        to_json():
            Convert the Tag instance to a JSON-compatible dictionary.

        __str__():
            Returns a JSON string representation of the Tag instance.
    """

    id = None
    name = None
    desc = None

    def __init__(self, id, name, desc=None):
        """
        Initialize the Tag with required ID and name, and optional description.

        Args:
            id (str): ID of the tag.
            name (str): Name of the tag.
            desc (str, optional): Description of the tag (default: same as `name`).

        Raises:
            RecomPIException: If `id` or `name` is not provided.
            RecomPIFieldTypeError: If any of the parameters (id, name, desc) are not of the expected type.

        """
        self.id = id
        self.name = name
        self.desc = desc if desc is not None else name

        RecomPIFieldTypeError.if_not_validated("Tag.__init__", "id", self.id, str)
        RecomPIFieldTypeError.if_not_validated("Tag.__init__", "name", self.name, str)
        RecomPIFieldTypeError.if_not_validated("Tag.__init__", "desc", self.desc, str)

        if not self.id or not self.name:
            raise RecomPIException(
                "Both `id` and `name` are required for initializing a Tag."
            )

    def to_json(self):
        """
        Convert the Tag instance to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary representation of the Tag instance.
        """
        return {"id": self.id, "name": self.name, "desc": self.desc}

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Return a JSON string representation of the Tag instance.

        Returns:
            str: JSON string representation of the Tag instance.
        """
        return str(self.to_json())


class Profile(object):
    """
    Represents a profile with id and name attributes.

    Attributes:
        id (int or None): ID of the profile.
        name (str or None): Name of the profile.

    Methods:
        __init__(id, name):
            Initializes a Profile instance with required `id` and `name`.

        to_json():
            Convert the Profile instance to a JSON-compatible dictionary.

        __str__():
            Returns a JSON string representation of the Profile instance.
    """

    id = None
    name = None

    def __init__(self, name, id):
        """
        Initialize the Profile with required ID and name.

        Args:
            name (str): Name of the profile.
            id (int): ID of the profile.

        Raises:
            RecomPIException: If any of the profile fields are not provided.
            RecomPIFieldTypeError: If any of the parameters (id, name) are not of the expected type.
        """
        self.id = id
        self.name = name

        RecomPIFieldTypeError.if_not_validated("Profile.__init__", "id", self.id, str)
        RecomPIFieldTypeError.if_not_validated(
            "Profile.__init__", "name", self.name, str
        )

        if not self.id or not self.name:
            raise RecomPIException(
                "Both `id` and `name` are required for initializing a Profile."
            )

    def to_json(self):
        """
        Convert the Profile instance to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary representation of the Profile instance.
        """
        return {
            self.name: self.id,
        }

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Return a JSON string representation of the Profile instance.

        Returns:
            str: JSON string representation of the Profile instance.
        """
        return str(self.to_json())


class SecureProfile(Profile):
    """
    Represents a secure profile with secure id (hashed) and name attributes.

    Attributes:
        id (int or None): ID of the profile.
        name (str or None): Name of the profile.

    Methods:
        __init__(id, name):
            Initializes a Profile instance with required `id` and `name`.

        to_json():
            Convert the Profile instance to a JSON-compatible dictionary.

        __str__():
            Returns a JSON string representation of the Profile instance.
    """

    id = None
    name = None

    def __init__(self, name, id):
        """
        Initialize the Profile with required ID and name.

        Args:
            name (str): Name of the profile.
            id (int): ID of the profile.

        Raises:
            RecomPIException: If any of the profile fields are not provided.
            RecomPIFieldTypeError: If any of the parameters (id, name) are not of the expected type.
        """
        super(SecureProfile, self).__init__(name, id)

    def to_json(self, hash_salt=None):
        """
        Convert the Profile instance to a secure JSON-compatible dictionary.

        Args:
            hash_salt (str, optional): A hash salt string used for securing the profile's ID -- In development environment you can ignore this.

        Returns:
            dict: Dictionary representation of the Profile instance.
        """
        return {
            n: sha256((v + (hash_salt if hash_salt else "")).encode()).hexdigest()
            for n, v in super(SecureProfile, self).to_json().items()
        }


class Location(object):
    """
    Represents a location with attributes such as IP, URL, referer, and user-agent.

    Attributes:
        ip (str or None): IP address of the location.
        url (str or None): URL associated with the location.
        referer (str or None): Referring URL.
        useragent (str or None): User agent string.

    Methods:
        __init__(ip=None, url=None, referer=None, useragent=None):
            Initializes a Location instance with optional attributes.

        to_json():
            Convert the Location instance to a JSON-compatible dictionary.

        __str__():
            Returns a JSON string representation of the Location instance.
    """

    ip = None
    url = None
    referer = None
    useragent = None

    def __init__(self, ip=None, url=None, referer=None, useragent=None):
        """
        Initialize the Location with optional attributes.

        Args:
            ip (str or None): IP address of the location.
            url (str or None): URL associated with the location.
            referer (str or None): Referring URL.
            useragent (str or None): User agent string.

        Raises:
            RecomPIException: If none of the location fields are provided.
            RecomPIFieldTypeError: If any of the parameters (ip, url, referer, useragent) are not of the expected type.
        """
        self.ip = ip
        self.url = url
        self.referer = referer
        self.useragent = useragent

        if not self.ip and not self.url and not self.referer and not self.useragent:
            raise RecomPIException(
                "At least one of the location fields must be provided."
            )

        if self.ip:
            RecomPIFieldTypeError.if_not_validated(
                "Location.__init__", "ip", self.ip, str
            )
        if self.url:
            RecomPIFieldTypeError.if_not_validated(
                "Location.__init__", "url", self.url, str
            )
        if self.referer:
            RecomPIFieldTypeError.if_not_validated(
                "Location.__init__", "referer", self.referer, str
            )
        if self.useragent:
            RecomPIFieldTypeError.if_not_validated(
                "Location.__init__", "useragent", self.useragent, str
            )

    def to_json(self):
        """
        Convert the Location instance to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary representation of the Location.
        """
        data = {}
        if self.ip:
            data["ip"] = self.ip

        if self.url:
            data["url"] = self.url

        if self.referer:
            data["referer"] = self.referer

        if self.useragent:
            data["useragent"] = self.useragent

        return data

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Return a JSON string representation of the Location instance.

        Returns:
            str: JSON string representation of the Location instance.
        """
        return str(self.to_json())


class Geo(object):
    """
    Represents geographical information with country and province attributes.

    Attributes:
        country (str or None): Country associated with the geographical information.
        province (str or None): Province associated with the geographical information.

    Methods:
        __init__(country=None, province=None):
            Initializes a Geo instance with optional attributes.

        to_json():
            Convert the Geo instance to a JSON-compatible dictionary.

        __str__():
            Returns a JSON string representation of the Geo instance.
    """

    country = None
    province = None

    def __init__(self, country=None, province=None):
        """
        Initialize the Geo with optional attributes.

        Args:
            country (str or None): Country associated with the geographical information.
            province (str or None): Province associated with the geographical information.

        Raises:
            RecomPIException: If none of the geo fields are provided.
            RecomPIFieldTypeError: If any of the parameters (country, province) are not of the expected type.
        """
        self.country = country
        self.province = province
        RecomPIFieldTypeError.if_not_validated(
            "Geo.__init__", "country", self.country, str
        )
        RecomPIFieldTypeError.if_not_validated(
            "Geo.__init__", "province", self.province, str
        )

        if not self.country and not self.province:
            raise RecomPIException("At least one of the geo fields must be provided.")

    def to_json(self):
        """
        Convert the Geo instance to a JSON-compatible dictionary.

        Returns:
            dict: Dictionary representation of the Geo instance.
        """
        data = {}

        if self.country:
            data["country"] = self.country

        if self.province:
            data["province"] = self.province

        return data

    def __repr__(self):
        return str(self)

    def __str__(self):
        """
        Return a JSON string representation of the Geo instance.

        Returns:
            str: JSON string representation of the Geo instance.
        """
        return str(self.to_json())


class RecomPIResponse(object):
    """
    Represents a response from the RecomPI API.

    Attributes:
        version (int): API version.
        body (str or dict): Response body.
        status (int): HTTP status code.
        response (requests.Response): The original HTTP response object.
    """

    version = None
    body = None
    status = None
    response = None

    def __init__(self, version, response):
        """
        Initialize RecomPIResponse with API version and HTTP response.

        Args:
            version (int): API version.
            response (requests.Response): HTTP response from the API.

        Raises:
            RecomPIFieldTypeError: If response is not of type requests.Response.
        """
        RecomPIFieldTypeError.if_not_validated(
            "RecomPIResponse", "response", response, requests.Response
        )

        self.version = version
        self.response = response
        self.body = response.text
        self.status = response.status_code

        try:
            self.body = response.json()
        except:
            pass

    def is_success(self):
        """
        Check if the response status code indicates success.

        Returns:
            bool: True if status code is 2xx, False otherwise.
        """
        return isinstance(self.status, int) and self.status >= 200 and self.status < 300

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[success: %s]%s" % (
            "true" if self.is_success() else "false",
            (" %s" % self.body) if self.body else "",
        )


class RecomPI(object):
    """
    Client class for interacting with the RecomPI API.

    Attributes:
        BASE_URL (str): Base URL for the API.
        api_key (str): API key for authentication.
        version (int): API version.
    """

    BASE_URL = "https://api.recompi.com"

    def __init__(self, api_key, version=2, secure_url=True, hash_salt=None):
        """
        Initialize RecomPI client with API key and version.

        Args:
            api_key (str): API key for authentication.
            version (int, optional): API version. Default is 2.
            secure_url (bool, optional): Use HTTPS if True, HTTP if False. Default is True.
            hash_salt (str, optional): A hash salt string used for SecureProfile -- If it's not intented to use SecureProfile or in development environment you can ignore this.
        """
        self.api_key = api_key
        self.version = version
        self.hash_salt = hash_salt

        RecomPIFieldTypeError.if_not_validated(
            "RecomPI.__init__", "api_key", api_key, str
        )

        RecomPIFieldTypeError.if_not_validated(
            "RecomPI.__init__", "version", version, int
        )

        RecomPIFieldTypeError.if_not_validated(
            "RecomPI.__init__", "secure_url", secure_url, bool
        )

        if version <= 0:
            raise RecomPIException("Version must be greater than 0.")

        if hash_salt is not None:
            RecomPIFieldTypeError.if_not_validated(
                "RecomPI.__init__", "hash_salt", hash_salt, str
            )

        if not secure_url:
            self.BASE_URL = "http://api.recompi.com"

    def _request(self, method, endpoint, data, headers={}):
        """
        Send an HTTP request to the API.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint.
            data (dict): Query data or request body.
            headers (dict, optional): HTTP headers.

        Returns:
            RecomPIResponse: Response from the API.
        """
        if not isinstance(headers, dict):
            headers = {}

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        response = requests.request(
            method, "%s/%s" % (self.BASE_URL, endpoint), headers=headers, json=data
        )

        return RecomPIResponse(self.version, response)

    @staticmethod
    def _list2dict(arr):
        """
        Merge a list of dictionaries into a single dictionary.

        Args:
            arr (list[dict]): List of dictionaries to merge.

        Returns:
            dict: Merged dictionary.
        """
        merged_dict = {}
        for d in arr:
            merged_dict.update(d)
        return merged_dict

    def _validate_profiles(self, profiles):
        if not isinstance(profiles, list):
            raise RecomPIException(
                "profiles must be a list of Profile or SecureProfile instances."
            )

        if not profiles:
            raise RecomPIException(
                "At least one profile must be provided for personalized recommendations."
            )

        for index, profile in enumerate(profiles):
            if isinstance(profile, Profile):
                RecomPIFieldTypeError.if_not_validated(
                    "push", "profiles[%s]" % index, profile, Profile
                )
            elif isinstance(profile, Profile):
                RecomPIFieldTypeError.if_not_validated(
                    "push", "profiles[%s]" % index, profile, SecureProfile
                )
            else:
                raise RecomPIException(
                    "All profiles must be either Profile or SecureProfile instances."
                )

    def push(self, label, tags, profiles, location, geo=None):
        """
        Push data to the RecomPI API.

        Args:
            label (str): Label for the data.
            tags (list[Tag]): List of Tag objects associated with the data.
            profiles (Profile|SecureProfile or list[Profile|SecureProfile]): User profiles for personalized recommendations.
            location (Location, optional): Location object associated with the data.
            geo (Geo, optional): Geographic data for location-based recommendations.

        Returns:
            RecomPIResponse: Response from the API.

        Raises:
            RecomPIFieldTypeError: If parameters do not match expected types.
        """
        RecomPIFieldTypeError.if_not_validated("push", "label", label, str)

        if isinstance(tags, Tag):
            tags = [tags]
        RecomPIFieldTypeError.if_not_validated("push", "tags", tags, Tag, True)

        if isinstance(profiles, Profile):
            profiles = [profiles]

        if isinstance(profiles, SecureProfile):
            profiles = [profiles]

        self._validate_profiles(profiles)

        RecomPIFieldTypeError.if_not_validated("push", "location", location, Location)

        if geo:
            RecomPIFieldTypeError.if_not_validated("push", "geo", geo, Geo)

        data = {
            "label": label,
            "tags": [tag.to_json() for tag in tags],
            "profiles": RecomPI._list2dict([profile.to_json() for profile in profiles]),
        }

        if location:
            data["location"] = location.to_json()

        if geo:
            data["geo"] = geo.to_json()

        return self._request("post", "push/v%d/%s" % (self.version, self.api_key), data)

    def recom(self, labels, profiles=None, geo=None):
        """
        Recommend data based on labels and optional profiles or geo information.

        Args:
            labels (list[str]): List of labels.
            profiles (Profile|SecureProfile or list[Profile|SecureProfile], optional): User profiles for personalized recommendations.
            geo (Geo, optional): Geographic data for location-based recommendations.

        Returns:
            RecomPIResponse: Response from the API.

        Raises:
            RecomPIFieldTypeError: If any of the parameters (labels, profiles, geo) are not of the expected type.
            RecomPIException: If neither profiles nor geo is provided.
        """
        if isinstance(labels, str):
            labels = [labels]
        RecomPIFieldTypeError.if_not_validated("push", "labels", labels, str, True)

        if profiles:
            if isinstance(profiles, Profile):
                profiles = [profiles]

            self._validate_profiles(profiles)

        if geo:
            RecomPIFieldTypeError.if_not_validated("push", "geo", geo, Geo)

        if not profiles and not geo:
            raise RecomPIException("At least one of profiles or geo must be provided!")

        data = {
            "labels": labels,
        }

        if profiles:
            data["profiles"] = RecomPI._list2dict(
                [profile.to_json() for profile in profiles]
            )

        if geo:
            data["geo"] = geo.to_json()

        return self._request(
            "post", "recom/v%d/%s" % (self.version, self.api_key), data
        )

    def verify(self):
        """
        Sends a verification request to check API connectivity.

        Returns:
            RecomPIResponse: Response object containing the API verification response.
        """
        return self._request(
            "get", "verify/v%d/%s" % (self.version, self.api_key), None
        )
