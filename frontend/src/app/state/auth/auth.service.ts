import {
    HttpClient,
    HttpErrorResponse,
    HttpHeaders,
    HttpParams,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { catchError, Observable, Subject, take, tap, throwError } from 'rxjs';
import {
    AuthState,
    RefreshTokenData,
    RegisterStatus,
    UserCreate,
    UserLogin,
} from '../auth/auth.model';
import { ApiResMessageModel } from '../../models/api-response.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
    private registerSubject = new Subject<string>();
    loginSubject = new Subject<void>();

    registerDone$: Observable<string> = this.registerSubject.asObservable();

    constructor(
        private http: HttpClient,
        private jwtHelper: JwtHelperService,
        private router: Router,
    ) {}

    postLogin(loginData: UserLogin): Observable<AuthState> {
        const body = new HttpParams()
            .set('username', loginData.username)
            .set('password', loginData.password);

        return this.http
            .post<AuthState>('auth/sign_in', body.toString(), {
                headers: new HttpHeaders({
                    'Content-Type': 'application/x-www-form-urlencoded',
                }),
            })
            .pipe(
                tap((info) => {
                    localStorage.setItem('user_id', info.id);
                    localStorage.setItem('user_name', info.username);
                    localStorage.setItem('access_token', info.access_token);
                    localStorage.setItem('refresh_token', info.refresh_token);
                    console.log(info);
                }),
                catchError((err: Error) => {
                    return throwError(() => err);
                }),
            );
    }

    postRegister(registerData: UserCreate): Observable<ApiResMessageModel> {
        return this.http
            .post<ApiResMessageModel>('auth/sign_up', registerData)
            .pipe(
                tap((info) => {
                    console.log(info);
                    return info;
                }),
                catchError((err: Error) => {
                    return throwError(() => err);
                }),
            );
    }

    getToken(refreshTokenData: RefreshTokenData): Observable<AuthState> {
        return this.http
            .get<AuthState>('auth/refresh', {
                headers: { refresh_token: refreshTokenData.token },
            })
            .pipe(
                tap((info) => {
                    localStorage.setItem('user_id', info.id);
                    localStorage.setItem('user_name', info.username);
                    localStorage.setItem('access_token', info.access_token);
                    localStorage.setItem('refresh_token', info.refresh_token);
                }),
                catchError((err: Error) => {
                    return throwError(() => err);
                }),
            );
    }

    login(FormData: UserLogin): void {
        this.postLogin(FormData)
            .pipe(take(1))
            .subscribe({
                next: () => {
                    console.log(123);
                    void this.router.navigate(['']);
                    this.loginSubject.next();
                },
                error: () => {
                    this.loginSubject.next();
                },
            });
    }

    register(FormData: UserCreate): void {
        console.log(FormData);
        this.postRegister(FormData)
            .pipe(take(1))
            .subscribe({
                next: (res) => {
                    console.log(res);
                    res.code && this.registerSubject.next(RegisterStatus.Login);
                },
                error: (error: HttpErrorResponse) => {
                    const errorResponse = error.error as { status?: string };
                    if (errorResponse && errorResponse.status) {
                        this.registerSubject.next(errorResponse.status);
                    }
                },
            });
    }

    logout(): void {
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_name');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        void this.router.navigate(['login']);
    }

    refreshToken(): Observable<AuthState> {
        const refreshKey = localStorage.getItem('refresh_token');
        const userName = localStorage.getItem('user_name');
        const id = localStorage.getItem('user_id');

        if (refreshKey && userName && id) {
            return this.getToken({
                id,
                name: userName,
                token: refreshKey,
            });
        }

        this.logout();

        return throwError(() => new Error('No Auth data in store'));
    }

    isAuthenticated(): boolean {
        const accessToken = localStorage.getItem('access_token');

        if (accessToken) {
            try {
                return this.jwtHelper.decodeToken(accessToken)!;
            } catch {
                return false;
            }
        }
        return false;
    }
}
