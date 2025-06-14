import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, interval, of, switchMap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MonitoringService {
    constructor(private http: HttpClient) {}

    // getAllMonitorings(): Observable<ChartDataResponse[]> {
    //     // return this.http.get<MonitoringData[]>('/api/monitoring');
    // }

    // getLiveUpdates() {
    //     return interval(60000).pipe(switchMap(() => this.getAllMonitorings()));
    // }
}
