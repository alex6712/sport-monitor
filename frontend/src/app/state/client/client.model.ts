import { SafeUrl } from '@angular/platform-browser';
import { User } from '../user/user.model';
import { TuiDay } from '@taiga-ui/cdk';

export interface ClientCreate {
    name: string;
    surname: string;
    patronymic: string;
    sex: boolean;
    email?: string | null;
    phone: string;
    photo_url: SafeUrl;
    season_ticket: SeasonTicket;
    is_violator: boolean;

    relationships: Relationship[];
    comments: Comment[];
    last_visit: number;
    last_visit_day: TuiDay;
    created?: number;
}

export interface Client extends ClientCreate {
    id: string;
    season_tickets: SeasonTicket[];
    season_ticket_type: string;
}

export interface SeasonTicket {
    id?: string;
    client_id?: string;
    type: string;
    expires_at: string; //date-time
}

///

export interface Relationship {
    id: string;
    thisClient: Client;
    otherClient: Client;
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
