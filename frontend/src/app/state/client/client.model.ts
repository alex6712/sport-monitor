import { SafeUrl } from '@angular/platform-browser';
import { User } from '../user/user.model';

export interface Client {
    id: string;
    name: string;
    surname: string;
    patronymic: string;
    email: string;
    photo_url: SafeUrl;
    connections: Connection[];
    membership: Membership[];
    comments: Comment[];
}

export interface Connection {
    id: string;
    thisClient: Client;
    otherClient: Client;
}

export interface Membership {
    id: string;
    active: boolean;
    created: number;
}

export interface Attendance {
    id: string;
    client: Client;
    start: number;
    end: number;
    drawer: number;
}

export interface Comment {
    id: string;
    user_id: User;
    client_id: string;
    comment: string;
}
