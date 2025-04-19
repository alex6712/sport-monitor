import { inject } from '@angular/core';
import {
    HttpInterceptorFn,
    HttpRequest,
    HttpHandlerFn,
    HttpEvent,
    HttpStatusCode,
} from '@angular/common/http';
import {
    catchError,
    throwError,
    switchMap,
    finalize,
    Subject,
    tap,
    filter,
    Observable,
} from 'rxjs';

import { AuthService } from '../../state/auth/auth.service';
import { ApiErrorModel } from '../../models/api-response.model';

let isTokenRefreshInProgress = false;
const tokenRefreshedSubject = new Subject<string>();
const tokenRefreshed$ = tokenRefreshedSubject.asObservable();

export const authInterceptor: HttpInterceptorFn = (
    initialRequest: HttpRequest<unknown>,
    next: HttpHandlerFn,
): Observable<HttpEvent<unknown>> => {
    const authService = inject(AuthService);

    const accessToken = localStorage.getItem('access_token');

    const request = initialRequest.clone({
        setHeaders: {
            ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
        },
    });

    return next(request).pipe(
        catchError((response: ApiErrorModel) => {
            const { status, error, url } = response;
            console.log(response);
            if (
                status === HttpStatusCode.Unauthorized &&
                !url?.includes('sign_in')
            ) {
                return handleUnauthorizedError(request, next, authService);
            }

            // ЕСЛИ ОТПРАВЛЯЕМ НЕ ПРАВИЛЬНЫЙ ТОКЕН ТО ЧТО ПОЛУЧАЕМ?????
            if (
                status === HttpStatusCode.BadRequest
                // && error?.status === 'User_IncorrectToken'
            ) {
                authService.logout();
            }

            return throwError(() => response);
        }),
    );
};

function handleUnauthorizedError(
    request: HttpRequest<unknown>,
    next: HttpHandlerFn,
    authService: AuthService,
): Observable<HttpEvent<unknown>> {
    if (isTokenRefreshInProgress) {
        return tokenRefreshed$.pipe(
            filter(Boolean),
            switchMap(() => {
                const newAccessToken = localStorage.getItem('access_token');

                const updatedRequest = request.clone({
                    setHeaders: {
                        ...(newAccessToken && {
                            Authorization: `Bearer ${newAccessToken}`,
                        }),
                    },
                });

                return next(updatedRequest);
            }),
        );
    }

    isTokenRefreshInProgress = true;

    return authService.refreshToken().pipe(
        tap(({ access_token }) => {
            tokenRefreshedSubject.next(access_token);
        }),
        switchMap(() => {
            const newAccessToken = localStorage.getItem('access_token');

            const updatedRequest = request.clone({
                setHeaders: {
                    ...(newAccessToken && {
                        Authorization: `Bearer ${newAccessToken}`,
                    }),
                },
            });

            return next(updatedRequest);
        }),
        catchError(() => {
            authService.logout();
            return throwError(() => new Error('Unauthorized'));
        }),
        finalize(() => {
            isTokenRefreshInProgress = false;
        }),
    );
}
