// base-url.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../../env/environment';

export const baseUrlInterceptor: HttpInterceptorFn = (request, next) => {
    const urlRegexp = /https?:\/\/\S+\/api/;

    const url = request.url.startsWith('http')
        ? request.url.replace(urlRegexp, environment.baseUrl)
        : `${environment.baseUrl}/${request.url}`;

    const updatedRequest = request.clone({ url });
    return next(updatedRequest);
};
