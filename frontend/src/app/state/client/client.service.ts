import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, EMPTY, Observable, of, switchMap, tap, throwError } from 'rxjs';
import { Client, ClientCreate } from './client.model';
import { ApiResMessageModel } from '../../models/api-response.model';
import { SeasonTicketsService } from '../season-tickets/season-tickets.service';

export interface ReturnedClients {
    code: number;
    message: string;
    id?: string;
    clients?: Client[];
    client?: Client;
}

@Injectable({ providedIn: 'root' })
export class ClientService {
    constructor(private http: HttpClient, private seasonTicketsService: SeasonTicketsService) {}

    getClients(): Observable<ReturnedClients> {
        return this.http.get<ReturnedClients>('clients/all').pipe(
            tap((clients: ReturnedClients) => {
                return clients;
            }),
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }

    getClient(id: string): Observable<ReturnedClients> {
        return this.http.get<ReturnedClients>(`clients/${id}`).pipe(
            tap((client: ReturnedClients) => {
                return client;
            }),
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }

    createClient(data: ClientCreate): Observable<ReturnedClients> {
        console.log(data);
        return this.http.post<ReturnedClients>('clients/', data).pipe(
            switchMap((res) => {
                if (!data.season_ticket.type) return EMPTY;
                console.log(1, res);
                return of(res);
            }),
            switchMap((res) => {
                console.log(2, res);
                return this.seasonTicketsService.createSeasonTicket(res.id!, data.season_ticket);
            }),
            switchMap(() => this.getClients()),
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }

    deleteClient(id: string): Observable<ApiResMessageModel> {
        return this.http.delete<ApiResMessageModel>(`clients/${id}`).pipe(
            tap((res) => {
                return res;
            }),
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }

    editClient(id: string, data: ClientCreate): Observable<ApiResMessageModel> {
        return this.http.put<ApiResMessageModel>(`clients/${id}`, data).pipe(
            tap((res) => {
                return res;
            }),
            catchError((err: Error) => {
                return throwError(() => err);
            }),
        );
    }
}
