// catch-error.interceptor.ts
import { inject } from '@angular/core';
import { HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { TuiAlertService } from '@taiga-ui/core';

import { ApiErrorModel } from '../../models/api-response.model';

export const catchErrorInterceptor: HttpInterceptorFn = (request, next) => {
    const alertService = inject(TuiAlertService);

    return next(request).pipe(
        catchError((err: ApiErrorModel) => {
            const { error, status } = err;

            alertService
                .open(error ? error.message : err.message, {
                    label: `Ошибка ${status}`,
                    appearance: 'warning',
                })
                .subscribe();

            return throwError(() => err);
        }),
    );
};
