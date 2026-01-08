from enum import Enum

class EventStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class EventCategory(str, Enum):
    ART = "art"
    MUSIC = "music"
    THEATER = "theater"
    LITERATURE = "literature"
    CINEMA = "cinema"
    DANCE = "dance"
    OTHER = "other"

class EventRegion(str, Enum):
    METROPOLITANA = "metropolitana"
    VALPARAISO = "valparaiso"
    BIOBIO = "biobio"
    # Can be extended
    ONLINE = "online"

class NewsletterStatus(str, Enum):
    DRAFT = "draft"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
