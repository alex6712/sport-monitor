import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { baseUrlInterceptor } from './core/interceptors/base-url.interceptor';

import { provideAnimations } from '@angular/platform-browser/animations';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { catchErrorInterceptor } from './core/interceptors/catch-error.interceptor';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';
import { AuthService } from './state/auth/auth.service';
// import { provideEventPlugins } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
    providers: [
        // provideEventPlugins(),
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes),
        provideHttpClient(
            withInterceptors([
                baseUrlInterceptor,
                authInterceptor,
                catchErrorInterceptor,
            ]),
        ),
        AuthService,
        JwtHelperService,
        {
            provide: JWT_OPTIONS,
            useValue: {
                tokenGetter: () => localStorage.getItem('access_token'), // Например, берём токен из localStorage
            },
        },
        provideAnimations(),
    ],
};
