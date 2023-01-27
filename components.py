from __future__ import annotations

import random
from datetime import datetime
from datetime import timezone
from typing import NamedTuple

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape,
)


class Color(NamedTuple):
    r: int
    g: int
    b: int
    h: int
    s: int
    l: int

    @classmethod
    def generate_random(cls) -> Color:
        return cls(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )


class GhUser:
    def __init__(
            self, username: str,
            profile_pic_path: str | None = None,
            label: str | None = None,
    ) -> None:
        self. username = username
        self._profile_pic_path = profile_pic_path
        self.label = label

        profile_pic_urls = (
            'https://i.fluffy.cc/vD2Kkj8NwFbQhCp122s88dS3vFJF2zX5.png',
            'https://i.fluffy.cc/W0jBLKC2GCxb07fb6ThqqP9qDrvvh1zQ.png',
            'https://i.fluffy.cc/WqxJNGNbZT4d4cxPp2m6jwN6Cq4TwHdk.png',
        )

        if self._profile_pic_path is None:
            pic_id = random.randint(0, len(profile_pic_urls) - 1)
            self.profile_pic = profile_pic_urls[pic_id]
        else:
            self.profile_pic = self._profile_pic_path


class TimeLineElement:
    def __init__(
            self,
            user: GhUser,
            date: datetime | str | None = None,
    ) -> None:
        self.user = user
        self.date = date

    @property
    def post_date(self) -> str:
        if self.date is None:
            return f'{datetime.now(tz=timezone.utc):%b %-d, %Y}'

        if isinstance(self.date, datetime):
            if self.date is not None:
                return f'{self.date:%b %-d, %Y}'
        elif isinstance(self.date, str):
            return self.date
        else:
            raise TypeError('invalid data type must be str, None or datetime')


class IssuePost(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            description: str,
            reproduction: str,
            expected: str,
            actual: str,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.description = description
        self.reproduction = reproduction
        self.expected = expected
        self.actual = actual

    def render(self) -> str:
        template = env.get_template('issue_post.html')
        return template.render(user=self.user, klass=self)


class LabelElement(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            name: str,
            color: Color,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.name = name
        self.color = color

    def render(self) -> str:
        template = env.get_template('label_add.html')
        return template.render(klass=self)


class IssueComment(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            text: str,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.text = text

    def render(self) -> str:
        template = env.get_template('issue_comment.html')
        return template.render(user=self.user, klass=self)


class Closed(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            reason: str,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.reason = reason

    def render(self) -> str:
        template = env.get_template('closed.html')
        return template.render(klass=self)


class Locked(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            reason: str,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.reason = reason

    def render(self) -> str:
        template = env.get_template('locked.html')
        return template.render(klass=self)


class GhIssue(TimeLineElement):
    def __init__(
            self,
            user: GhUser,
            opener: GhUser,
            title: str,
            repo: str,
            note: str = 'Leave a comment',
            issues: int | str = 1,
            issue_nr: int = 1,
            watchers: int = 1,
            forks: int = 0,
            stars: int = 0,
            date: datetime | str | None = None,
    ) -> None:
        super().__init__(user, date)
        self.title = title
        self.repo = repo
        self.note = note
        self.issues = issues
        self.issue_nr = issue_nr
        self.watchers = watchers
        self.forks = forks
        self.stars = stars
        self.opener = opener
        self._elements: list[TimeLineElement] = []

    def add(self, element: TimeLineElement) -> None:
        self._elements.append(element)

    def render(self) -> str:
        template = env.get_template('final.html')
        return template.render(elements=self._elements, klass=self)

    @property
    def nr_comments(self) -> int:
        return len([i for i in self._elements if isinstance(i, IssueComment)])
