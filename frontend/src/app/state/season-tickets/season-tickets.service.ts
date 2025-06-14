import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { SeasonTicket } from '../client/client.model';

export interface SeasonTicketResponse {
    code: number;
    message: string;
}

@Injectable({ providedIn: 'root' })
export class SeasonTicketsService {
    constructor(private http: HttpClient) {}

    createSeasonTicket(client_id: string, data: SeasonTicket): Observable<SeasonTicketResponse> {
        data = {
            ...data,
            client_id,
        };
        console.log(data);
        return this.http.post<SeasonTicketResponse>('season_tickets/', data).pipe(
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }
}
