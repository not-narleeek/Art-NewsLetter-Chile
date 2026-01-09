export interface Subscriber {
    id: string;
    email: string;
    is_active: boolean;
    confirmation_token?: string;
    created_at?: string;
}
