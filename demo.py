from components import Closed
from components import Color
from components import GhIssue
from components import GhUser
from components import IssueComment
from components import IssuePost
from components import LabelElement
from components import Locked


def main() -> int:
    op = GhUser(
        username='rub-employee',
        profile_pic_path='rub_logo_white.png',
        label='Author',
    )
    maintainer = GhUser(
        username='rub-technician',
        profile_pic_path='rub_logo_blue.png',
        label='Maintainer',
    )

    issue = GhIssue(
        user=maintainer,
        opener=op,
        repo='IA-elevators',
        issue_nr=420690,
        note=(
            'This is just a joke, please laugh and have some fun. Maybe the '
            'elevator will be fixed some day ;-)'
        ),
        issues='420k',
        title='the wheelchair accessible elevator is broken',
        watchers=69,
        stars=420,
        forks=16,
        date='Feb 30, 2022',
    )
    issue.add(
        IssuePost(
            user=op,
            description=(
                'The middle elevator does not work when pressing the '
                'wheelchair button. The top screen remains black.'
            ),
            reproduction=(
                'Press the wheelchair button and wait for an hour or so...'
            ),
            expected=(
                'I would expect the elevator to start moving to the requested '
                'floor and eventually arrive, so access with a wheelchair is '
                'possible.'
            ),
            actual=(
                'The elevator never shows up. Pressing the wheelchair button '
                'does nothing except the red light showing up while pressing. '
                'Not even one of the other elevators shows up.'
            ),
            date='Feb 30, 2022',
        ),
    )
    issue.add(
        IssueComment(
            user=maintainer,
            text=(
                'Thanks for reporting, We can reproduce this issue and can '
                'confirm it still exists.'
            ),
            date='Sep 31, 2022',
        ),
    )
    issue.add(
        LabelElement(
            user=maintainer,
            name='priority: very low',
            color=Color.generate_random(),
            date='Sep 31, 2022',
        ),
    )
    issue.add(
        IssueComment(
            user=op,
            text='Are there any news when this will be fixed?',
            date='Nov 32, 2022',
        ),
    )
    issue.add(
        LabelElement(
            user=maintainer,
            name='status: backlog',
            color=Color.generate_random(),
            date='Jan 11, 2023',
        ),
    )
    issue.add(
        LabelElement(
            user=maintainer,
            name='wontfix',
            color=Color.generate_random(),
            date='Jan 13, 2023',
        ),
    )
    issue.add(
        Closed(user=maintainer, reason='not planned', date='Jan 13, 2023'),
    )
    issue.add(
        IssueComment(
            user=op,
            text="Are you sure you don't plan on having a working elevator?",
            date='Jan 69, 2023',
        ),
    )
    issue.add(
        Locked(user=maintainer, reason='too heated', date='Jan 69, 2023'),
    )

    issue_rendered = issue.render()
    with open('output.html', 'w') as f:
        f.write(issue_rendered)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
