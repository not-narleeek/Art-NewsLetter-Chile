export enum EventStatus {
    DRAFT = "draft",
    PUBLISHED = "published",
    ARCHIVED = "archived"
}

export enum EventCategory {
    ART = "art",
    MUSIC = "music",
    THEATER = "theater",
    LITERATURE = "literature",
    CINEMA = "cinema",
    DANCE = "dance",
    OTHER = "other"
}

export enum EventRegion {
    METROPOLITANA = "metropolitana",
    VALPARAISO = "valparaiso",
    BIOBIO = "biobio",
    ONLINE = "online"
}

export interface Event {
    id: string;
    title: string;
    slug: string;
    description?: string;
    start_date: string;
    end_date?: string;
    category: EventCategory;
    region: EventRegion;
    external_url?: string;
    image_url?: string;
    status: EventStatus;
    created_at: string;
}

export interface EventCreate {
    title: string;
    description?: string;
    start_date: string;
    end_date?: string;
    category: EventCategory;
    region: EventRegion;
    external_url?: string;
    status: EventStatus;
    image?: File;
}
