import random
from asyncio import Future, Queue
from enum import Enum
from typing import Optional, Tuple, Type, Union


class TimeMoment:
    def __init__(self):
        self._moment = "night"

    @property
    def is_day(self) -> bool:
        return self._moment == "day"

    def switch_day_night(self):
        self._moment = "night" if self.is_day else "day"


class Event:
    """Base event"""


class CandyPileEmpty(Event):
    """Indicates that candy pile became empty"""


class NutCrackerSaved(Event):
    """Indicates that NutCracker is safe"""


class MiceKingWhistled(Event):
    """Indicates that Mice King whistled"""


class MiceKingEyesSparked(Event):
    """Indicates that Mice King's eyes sparked"""


class NutCrackerIsRipped(Future):
    """Future for ripping NutCracker"""


class GiveMeDolls(Future):
    """Future for order to give out dolls"""


class CandyType(Enum):
    marzipan = "marzipan"
    some_candy = "some_candy"


class Candy:
    def __init__(self, type_: CandyType) -> None:
        self._type = type_
        self._is_eaten = False
        self._is_good_to_eat = True

    def be_eaten(self):
        self._is_eaten = True
        self._is_good_to_eat = False

    def get_bites(self):
        self._is_good_to_eat = False

    @property
    def type(self) -> CandyType:
        return self._type

    @property
    def is_good_to_eat(self) -> bool:
        return self._is_good_to_eat

    @property
    def is_eaten(self) -> bool:
        return self._is_eaten


def candy_pile():
    size = random.randint(10, 20)
    for i in range(size):
        if i % 5 == 0:
            yield Candy(type_=CandyType.marzipan)
        else:
            yield Candy(type_=CandyType.some_candy)


class Feature(Enum):
    greedy = "greedy"
    kind = "kind"


class Emotion(Enum):
    fear = "fear"
    anger = "anger"
    joy = "joy"
    distress = "distress"
    calm = "calm"
    sorrow = "sorrow"
    undefined = "undefined"
    disgust = "disgust"


class DollType(Enum):
    sugar = "sugar"
    gingerbread = "gingerbread"


class Color(Enum):
    snow_white = "snow-white"
    ruddy_cheeked = "ruddy-cheeked"


class Position(Enum):
    undefined = 0
    near_mary_pillow = 1
    mary_bed = 2
    on_table = 3
    under_table = 4
    near_closet = 5


class DollAction(Enum):
    russian_dance = 0
    jump_around = 1
    stand = 2


class DollDress:
    def __init__(self, is_beautiful: bool):
        self.is_beautiful = is_beautiful


class Doll:
    def __init__(
        self,
        name: str,
        action: DollAction = DollAction.stand,
        type_: Optional[DollType] = None,
        color: Optional[Color] = None,
        is_loved: bool = True,
        dress: Optional[DollDress] = None
    ):
        self.name = name
        self.action = action
        self.is_loved = is_loved
        self.dress = dress
        if type_ is not None:
            self._type = type_
        else:
            self._type = random.choice(tuple(DollType))

        if color is not None:
            self._color = color
        else:
            self._color = random.choice(tuple(Color))


class Herd(Doll):
    def __init__(self, lamps: list[Doll]):
        super().__init__(name="Herd", action=DollAction.stand)
        self._lamps = lamps


class Dog(Doll):
    def __init__(self, herd_to_jump_around: Herd):
        super().__init__(name="Dog", action=DollAction.jump_around)
        self.connected_to = herd_to_jump_around


class PostMan(Doll):
    def __init__(self):
        super().__init__(name="Dog", action=DollAction.stand, dress=DollDress(is_beautiful=False))
        self.letters = ["letter", "letter", "letter"]


class Closet:
    def __init__(self):
        herd = Herd(
            lamps=[
                Doll(name="Lamp", color=Color.snow_white) for _ in range(10)
            ]
        )
        self.dolls: list[Doll] = [
            Doll(name="Shepherd", dress=DollDress(is_beautiful=False)),
            Doll(name="Shepherd Kid", dress=DollDress(is_beautiful=False)),
            herd,
            Dog(herd_to_jump_around=herd),
            PostMan(),
            PostMan(),

            Doll(name="Girl1", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),
            Doll(name="Boy1", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),

            Doll(name="Girl2", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),
            Doll(name="Boy2", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),

            Doll(name="Girl3", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),
            Doll(name="Boy3", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),

            Doll(name="Girl4", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),
            Doll(name="Boy4", action=DollAction.russian_dance, dress=DollDress(is_beautiful=True)),

            Doll(name="Pachter Feldkümmel", is_loved=False),
            Doll(name="Virgin of Orleans", is_loved=False),
            Doll(name="Child", color=Color.ruddy_cheeked)
        ]


class Actor:
    """"""

    def __init__(self):
        self.perception = Queue[Union[Event, Future]]()
        self.emotion: Emotion = Emotion.undefined
        self._event_reactions: dict[Type, Emotion] = {}

        self._future_threat_reactions: dict[Type, Emotion] = {}

        self._done_threat_reactions: dict[Type, Emotion] = {}
        self.position: Position = Position.undefined

    @property
    def features(self) -> Tuple[Feature]:
        return Tuple[Feature]()

    def see_and_hear(self, event: [Union[Event, Future]]):
        if isinstance(event, Future):
            self.react_on_future(future=event)
        elif isinstance(event, Event):
            self.react_on_events(event=event)

    def react_on_future(self, future: Future):
        if future.done():
            self.emotion = self._done_threat_reactions.get(
                future.__class__,
                Emotion.undefined
            )
        else:
            self.emotion = self._future_threat_reactions.get(
                future.__class__,
                Emotion.undefined
            )

    def react_on_events(self, event: Event):
        emotion = self._event_reactions.get(
            event.__class__,
            Emotion.undefined
        )
        self.emotion = emotion


class MiceKing(Actor):
    """"""

    def __init(self):
        super().__init__()
        self._event_reactions: dict[Type, Emotion] = {
            CandyPileEmpty: Emotion.joy,
            NutCrackerSaved: Emotion.anger,
        }

        self._future_threat_reactions: dict[Type, Emotion] = {
            NutCrackerIsRipped: Emotion.joy,
        }

        self._done_threat_reactions: dict[Type, Emotion] = {
            NutCrackerIsRipped: Emotion.joy,
        }

    @property
    def features(self) -> Tuple[Feature]:
        return Feature.greedy,

    @staticmethod
    def eat_candy(candy: Candy):
        if candy.type == CandyType.marzipan:
            candy.get_bites()
        else:
            candy.be_eaten()

    def whistle(self, actor: Actor):
        actor.see_and_hear(MiceKingWhistled())

    def spark_with_eyes_to(self, actor: Actor):
        actor.see_and_hear(MiceKingEyesSparked())

    def squeak(self, actor: Actor, threat: Future):
        actor.see_and_hear(threat)


class Mary(Actor):
    """"""

    def __init__(self):
        super().__init__()
        self.full_name = "Marie Stahlbaum"
        self._event_reactions: dict[Type, Emotion] = {
            CandyPileEmpty: Emotion.calm,
            NutCrackerSaved: Emotion.joy,
            MiceKingWhistled: Emotion.fear,
            MiceKingEyesSparked: Emotion.disgust,
        }

        self._future_threat_reactions: dict[Type, Emotion] = {
            NutCrackerIsRipped: Emotion.fear,
        }

        self._done_threat_reactions: dict[Type, Emotion] = {
            NutCrackerIsRipped: Emotion.sorrow,
        }

    @property
    def features(self) -> Tuple[Feature]:
        return Feature.kind,

    def peek_most_loved(self, dolls: list[Doll]) -> Optional[Doll]:
        for doll in dolls:
            if doll.name == "Child":
                return doll


def nutcracker_fragment():
    mice_king = MiceKing()
    mary = Mary()

    moment = TimeMoment()
    assert not moment.is_day

    for candy in candy_pile():
        mice_king.eat_candy(candy)
        if candy.type == CandyType.marzipan:
            assert not candy.is_eaten and not candy.is_good_to_eat
        else:
            assert candy.is_eaten

    moment.switch_day_night()
    assert moment.is_day

    mary.see_and_hear(CandyPileEmpty())
    assert mary.emotion == Emotion.calm

    mary.see_and_hear(NutCrackerSaved())
    assert mary.emotion == Emotion.joy

    moment.switch_day_night()
    assert not moment.is_day
    mary.position = Position.mary_bed
    mice_king.position = Position.near_mary_pillow

    mice_king.whistle(mary)
    assert mary.emotion == Emotion.fear

    mice_king.position = Position.on_table
    mice_king.spark_with_eyes_to(mary)
    assert mary.emotion == Emotion.disgust

    mice_king_request = GiveMeDolls()
    mice_king_threat = NutCrackerIsRipped()
    mice_king.squeak(mary, mice_king_request)
    mice_king.squeak(mary, mice_king_threat)
    if not mice_king_request.done():
        mice_king_threat.set_result(True)

    mice_king.position = Position.under_table

    moment.switch_day_night()
    assert moment.is_day

    closet = Closet()
    mary.position = Position.near_closet
    mary.emotion = Emotion.sorrow
    assert mary.peek_most_loved(dolls=closet.dolls).name == "Child"


if __name__ == "__main__":
    nutcracker_fragment()
