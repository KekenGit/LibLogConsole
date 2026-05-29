from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Person:
    """Base class for people recorded by the system."""

    def __init__(self, name, address):
        self._name = name
        self._address = address

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    def matches_name(self, name):
        return self._name.lower() == name.lower()


class VisitorRecord(Person):
    """Encapsulates one visitor check-in and check-out transaction."""

    def __init__(
        self,
        date,
        name,
        reason,
        address,
        school,
        signature,
        time_in,
        time_out="",
        duration="",
    ):
        super().__init__(name, address)
        self._date = date
        self._reason = reason
        self._school = school
        self._signature = signature
        self._time_in = time_in
        self._time_out = time_out
        self._duration = duration

    @property
    def date(self):
        return self._date

    @property
    def reason(self):
        return self._reason

    @property
    def school(self):
        return self._school

    @property
    def signature(self):
        return self._signature

    @property
    def time_in(self):
        return self._time_in

    @property
    def time_out(self):
        return self._time_out

    @property
    def duration(self):
        return self._duration

    @classmethod
    def create(cls, name, reason, address, school, signature, now=None):
        now = now or datetime.now()

        return cls(
            date=now.strftime("%Y-%m-%d"),
            name=name,
            reason=reason,
            address=address,
            school=school,
            signature=signature,
            time_in=now.strftime(DATETIME_FORMAT),
        )

    @classmethod
    def from_dict(cls, row):
        time_in = row.get("time_in", "")
        date = row.get("date", "") or time_in[:10]

        return cls(
            date=date,
            name=row.get("name", ""),
            reason=row.get("reason", ""),
            address=row.get("address", ""),
            school=row.get("school", ""),
            signature=row.get("signature", ""),
            time_in=time_in,
            time_out=row.get("time_out", ""),
            duration=row.get("duration", ""),
        )

    def to_dict(self):
        return {
            "date": self._date,
            "name": self._name,
            "reason": self._reason,
            "address": self._address,
            "school": self._school,
            "signature": self._signature,
            "time_in": self._time_in,
            "time_out": self._time_out,
            "duration": self._duration,
        }

    def is_for_date(self, date):
        return self._date == date

    def is_active_on(self, date):
        return self.is_for_date(date) and self._time_out == ""

    def check_out(self, time_out=None):
        time_out = time_out or datetime.now()
        time_in = datetime.strptime(self._time_in, DATETIME_FORMAT)
        duration = time_out - time_in

        self._time_out = time_out.strftime(DATETIME_FORMAT)
        self._duration = str(duration)

        return duration
